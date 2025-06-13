from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
    File,
    UploadFile,
    Query,
)
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, Dict, Any
from ...domain.models.user import User
from ..dependencies import get_current_active_user, get_current_admin_user
import pandas as pd
import numpy as np
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DECIMAL,
    select,
    insert,
    update as sqlalchemy_update,
)
import os
from datetime import datetime
from pydantic import BaseModel
import traceback
from ...services import (
    get_data_sap,
    df_matrices_avon_natura,
    df_matrices_otros_tipos,
    df_matrices_merge_raw,
    filter_avon_natura,
    filter_marca_otros,
    upload_dataframe_to_db,
    get_inventory_by_month_year,
    process_dataframe_avon_natura,
    process_dataframe_otras_marcas,
    combine_final_dataframes,
)
import logging

router = APIRouter(prefix="/risk", tags=["risk"])

# Configuración del logger para este módulo
logger = logging.getLogger(__name__)

# ============================================================================ #
#          ENDPOINTS PARA ADMINISTRADORES Y USUARIOS REGULARES                 #
# ============================================================================ #


# Endpoint para consultar la base de riesgo por mes y año específicos
@router.post("/consult-riskbase", response_model=Dict[str, Any])
async def consult_riskbase(
    mes: int = Query(..., ge=1, le=12, description="Mes a consultar (1-12)"),
    anio: int = Query(..., ge=2000, description="Año a consultar (desde 2000)"),
    current_user: User = Depends(get_current_active_user),
):
    """
    Consulta la base de riesgo por mes y año específicos.

    Este endpoint permite filtrar y obtener datos de la base de riesgo según el mes y año
    indicados. Genera un archivo Excel temporal con los resultados para su posterior
    visualización o descarga.

    Args:
        mes: Número de mes (1-12)
        anio: Año (desde 2000)
        current_user: Usuario autenticado que realiza la consulta

    Permisos: Administradores y usuarios regulares

    Returns:
        Dict[str, Any]: Resultado de la consulta con información sobre filas procesadas,
        columnas y nombre del archivo temporal generado

    Raises:
        HTTPException: Si no se encuentran datos para el mes y año especificados o si ocurre un error
    """
    logger.info(
        f"[consult-riskbase] Usuario: {current_user.username} consultando base de riesgo para mes={mes}, año={anio}"
    )
    try:
        df_final_combined = get_inventory_by_month_year(mes, anio)
        if df_final_combined is None or df_final_combined.empty:
            logger.warning(
                f"[consult-riskbase] No se encontraron datos para mes={mes}, año={anio}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron datos para mes={mes} y año={anio}",
            )

        excel_file = f"Archivo_temporal_{datetime.now().strftime('%d-%m-%y_%H-%M')}.xlsx"
        temp_dir = os.environ.get("TEMP_DIR")
        os.makedirs(temp_dir, exist_ok=True)
        excel_path = os.path.join(temp_dir, excel_file)
        df_final_combined.to_excel(excel_path, index=False)
        result = {
            "success": True,
            "message": "Consulta ejecutada correctamente",
            "rows_processed": len(df_final_combined),
            "columns": df_final_combined.columns.tolist(),
            "excel_file": excel_file,
            "summary": {
                "total_records": len(df_final_combined),
            },
        }
        logger.info(
            f"[consult-riskbase] Consulta exitosa de información de la base de datos"
        )
        return result
    except Exception as e:
        logger.error(f"[consult-riskbase] Error: {e}")
        tb = traceback.format_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar la base de riesgo: {str(e)}\n{tb}",
        )


# Endpoint para visualizar los datos de un archivo temporal previamente generado con paginación
@router.get("/data-view")
async def get_risk_data(
    temp_file: Optional[str] = None,
    limit: int = 25,
    offset: int = 0,
    current_user=Depends(get_current_active_user),
):
    """
    Visualiza los datos de un archivo temporal previamente generado con paginación.

    Este endpoint permite ver el contenido de un archivo Excel temporal generado por
    otros endpoints, aplicando paginación para facilitar la visualización de grandes
    conjuntos de datos.

    Args:
        temp_file: Nombre del archivo temporal a visualizar
        limit: Número máximo de registros a mostrar por página (por defecto 25)
        offset: Número de registros a saltar para la paginación
        current_user: Usuario autenticado que realiza la consulta

    Permisos: Administradores y usuarios regulares

    Returns:
        JSONResponse: Datos paginados del archivo, total de registros y metadatos

    Raises:
        HTTPException: Si no se proporciona archivo, no existe o hay error al procesarlo
    """
    logger.info(
        f"[data-view] Se incia el proceso de visualización del archivo temporal"
    )
    try:
        if not temp_file:
            logger.warning(f"[data-view] No se proporcionó archivo temporal")
            raise HTTPException(
                status_code=400, detail="No se proporcionó archivo temporal."
            )
        temp_dir = os.getenv(
            "TEMP_DIR",
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "..",
                "temp",
            ),
        )
        file_path = os.path.join(temp_dir, temp_file)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404, detail="Archivo temporal no encontrado."
            )
        df = pd.read_excel(file_path)

        # Mostar todas las columnas
        df = df.iloc[:, :52] if df.shape[1] >= 52 else df

        # Paginación y saneamiento: inf, -inf y nan → None
        df_paginated = df.iloc[offset : offset + limit].replace(
            [np.inf, -np.inf, np.nan], None
        )

        records = df_paginated.to_dict(orient="records")
        safe_records = jsonable_encoder(records)

        logger.info(f"[data-view] Visualización exitosa del archivo temporal")
        return JSONResponse(
            {
                "data": safe_records,
                "total": len(df),
                "limit": limit,
                "offset": offset,
                "columns": df.columns.tolist(),
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[data-view] Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener los datos: {e}")


# Endpoint para exportar los datos procesados a un archivo Excel para su descarga
@router.get("/export-excel")
async def export_to_excel(
    filename: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
):
    """
    Exporta los datos procesados a un archivo Excel para su descarga.

    Este endpoint permite descargar un archivo Excel previamente generado por
    otros endpoints. El archivo no se elimina después de la descarga.

    Args:
        filename: Nombre del archivo Excel en la carpeta temporal
        current_user: Usuario autenticado que realiza la descarga

    Permisos: Administradores y usuarios regulares

    Returns:
        FileResponse: Archivo Excel para descargar

    Raises:
        HTTPException: Si no se proporciona nombre de archivo, no existe o hay error al procesarlo
    """
    logger.info(f"[export-excel] Exportando archivo temporal: {filename}")
    try:
        if filename:
            temp_dir = os.environ.get("TEMP_DIR")
            file_path = os.path.join(temp_dir, filename)
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Archivo temporal no encontrado. Ejecute el proceso primero.",
                )
            logger.info(f"[export-excel] Archivo temporal exportado correctamente")
            return FileResponse(
                path=file_path,
                filename=os.path.basename(file_path),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            logger.warning(
                f"[export-excel] No se proporcionó el nombre del archivo temporal"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionó el nombre del archivo.",
            )
    except Exception as e:
        logger.error(f"[export-excel] Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al exportar a Excel: {str(e)}",
        )


# Modelo para recibir el nombre del archivo desde el body JSON
class FileNameRequest(BaseModel):
    filename: str


# ============================================================================ #
#             ENDPOINTS EXCLUSIVOS PARA ADMINISTRADORES                        #
# ============================================================================ #


# Endpoint para ejecutar el proceso completo de extracción, transformación y carga de datos de base riesgo
@router.post("/process", response_model=Dict[str, Any])
async def process_riskbase(current_user: User = Depends(get_current_active_user)):
    """
    Ejecuta el proceso completo de extracción, transformación y carga de datos de riesgo.

    Este endpoint realiza las siguientes operaciones:
    1. Obtiene las matrices de configuración para AVON/NATURA y otros marcas
    2. Extrae datos de SAP
    3. Filtra y procesa los datos según el tipo de marca
    4. Combina los resultados y genera un archivo Excel temporal

    Permisos: Solo administradores

    Returns:
        Dict[str, Any]: Resultado del proceso con información sobre filas procesadas,
        columnas y nombre del archivo temporal generado

    Raises:
        HTTPException: Si no se pueden obtener datos de SAP o si ocurre un error durante el proceso
    """
    logger.info(f"[process] Realizando el procesamiento de la base de riesgo")
    try:
        matrices_avon_natura = df_matrices_avon_natura()
        matrices_otros_tipos = df_matrices_otros_tipos()

        df_sap = get_data_sap()

        if df_sap is None or df_sap.empty:
            logger.error(f"[process] No se pudieron obtener los datos de SAP")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudieron obtener datos de SAP",
            )

        # 2. Filtro para obtener solo los datos de AVON y NATURA
        df_avon_natura = filter_avon_natura(df_sap)
        # 3. Filtro para obtener los datos de otras marcas
        df_otras_marcas = filter_marca_otros(df_sap)

        df_final_avon_natura = process_dataframe_avon_natura(
            df_avon_natura, matrices_avon_natura
        )

        df_final_otras_marcas = process_dataframe_otras_marcas(
            df_otras_marcas, matrices_otros_tipos
        )

        df_final_combined = combine_final_dataframes(
            df_final_avon_natura, df_final_otras_marcas
        )

        logger.info(f"[process] Generando archivo Excel temporal")
        excel_file = f"Archivo_temporal_{datetime.now().strftime('%d-%m-%y_%H-%M')}.xlsx"
        temp_dir = os.environ.get("TEMP_DIR")
        os.makedirs(temp_dir, exist_ok=True)
        excel_path = os.path.join(temp_dir, excel_file)
        df_final_combined.to_excel(excel_path, index=False)
        result = {
            "success": True,
            "message": "Proceso ejecutado correctamente",
            "rows_processed": len(df_final_combined),
            "columns": df_final_combined.columns.tolist(),
            "excel_file": excel_file,
            "summary": {
                "total_records": len(df_final_combined),
            },
        }
        logger.info(f"[process] Proceso de base de riesgo ejecutado correctamente")
        return result
    except Exception as e:
        logger.error(f"[process] Error: {e}")
        tb = traceback.format_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al ejecutar el proceso: {str(e)}\n{tb}",
        )


# Endpoint para guardar los datos procesados en la base de datos
@router.post("/save-to-db")
async def save_to_database(
    request: FileNameRequest, current_user: User = Depends(get_current_admin_user)
):
    """
    Guarda los datos procesados en la base de datos.

    Este endpoint permite cargar los datos de un archivo Excel temporal
    a la base de datos. El archivo debe haber sido generado previamente
    por el proceso de extracción y transformación.

    Args:
        request: Objeto con el nombre del archivo temporal
        current_user: Administrador autenticado que realiza la operación

    Permisos: Solo administradores

    Returns:
        Dict: Resultado de la operación con información sobre filas guardadas

    Raises:
        HTTPException: Si el archivo no existe o hay error al guardarlo en la base de datos
    """
    logger.info(
        f"[save-to-db] Usuario: {current_user.username} guardando la información en la base de datos"
    )
    try:
        temp_dir = os.environ.get("TEMP_DIR")
        filename = request.filename
        file_path = os.path.join(temp_dir, filename)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Archivo temporal no encontrado. Ejecute el proceso primero.",
            )
        df = pd.read_excel(file_path)
        upload_dataframe_to_db(df)
        logger.info(f"[save-to-db] Datos guardados correctamente en la base de datos")
        return {
            "success": True,
            "message": "Datos guardados correctamente en la base de datos",
            "rows_saved": len(df),
        }
    except Exception as e:
        logger.error(f"[save-to-db] Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar en la base de datos: {str(e)}",
        )


# Endpoint para obtener todas las matrices almacenadas en la base de datos
@router.get("/matrices-view", response_model=Dict[str, Any])
async def get_matrices(current_user: User = Depends(get_current_admin_user)):
    """
    Obtiene todas las matrices almacenadas en la base de datos.

    Este endpoint recupera todas las matrices de configuración utilizadas
    en el proceso de cálculo de riesgo, incluyendo las matrices para
    AVON/NATURA y otros tipos de marcas.

    Permisos: Solo administradores

    Returns:
        Dict[str, Any]: Datos de las matrices, total de registros y columnas disponibles

    Raises:
        HTTPException: Si no se encuentran matrices o hay error al consultarlas
    """
    logger.info(
        f"[matrices-view] Usuario: {current_user.username} consultando matrices de base de riesgo"
    )
    try:
        # Obtener datos de la base de datos
        matrices = df_matrices_merge_raw()

        if matrices is None or matrices.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron matrices en la base de datos",
            )

        # Convertir a diccionario para la respuesta JSON
        matrices_dict = matrices.to_dict(orient="records")

        logger.info(f"[matrices-view] Matrices consultadas correctamente")
        return {
            "matrices": matrices_dict,
            "total": len(matrices_dict),
            "columns": matrices.columns.tolist(),
        }

    except Exception as e:
        logger.error(f"[matrices-view] Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las matrices: {str(e)}",
        )


# Endpoint para actualizar las matrices de configuración de base riesgo
@router.put("/matrices-save", response_model=Dict[str, Any])
async def update_matrices(
    data: Dict[str, Any], current_user: User = Depends(get_current_admin_user)
):
    """
    Actualiza los campos de las matrices de la política de la base de riesgo.

    Este endpoint permite modificar los campos de las matrices de la política de la base de riesgo,
    incluyendo factor_prov y clasificacion en MatrizBaseRiesgo, así como campos
    relacionados en InventarioMatriz. Antes de realizar cualquier actualización,
    guarda el estado actual en la tabla histórica MatrizBaseRiesgoHist.

    Args:
        data: Diccionario con las filas a actualizar (debe contener "rows" o "matrices")
        current_user: Administrador autenticado que realiza la operación

    Permisos: Solo administradores

    Returns:
        Dict[str, Any]: Resultado de la operación con información sobre filas actualizadas
        y posibles errores

    Raises:
        HTTPException: Si no se envían filas para actualizar o hay error en el proceso
    """
    # Aquí simplemente registramos en los logs que el usuario va a actualizar matrices.
    logger.info(
        f"[matrices-save] Usuario: {current_user.username} actualizando matrices de base de riesgo"
    )
    # Obtenemos la lista de matrices que el usuario quiere actualizar.
    # Si no hay ninguna, avisamos y detenemos el proceso.
    matrices = data.get("rows") or data.get("matrices") or []
    if not matrices:
        logger.warning(f"[matrices-save] No se enviaron filas para actualizar")
        raise HTTPException(
            status_code=400, detail="No se enviaron filas para actualizar."
        )

    # --- CONEXIÓN A LA BASE DE DATOS ---
    # Aquí preparamos todo lo necesario para conectarnos a la base de datos.
    # Se obtienen los datos de acceso y se crea el motor de conexión.
    usuario = os.getenv("DB_USER")
    pwd = os.getenv("DB_PASSWORD")
    server = os.getenv("DB_SERVER")
    db = os.getenv("DATABASE")
    driver = "ODBC Driver 17 for SQL Server"
    engine = create_engine(
        f"mssql+pyodbc://{usuario}:{pwd}@{server}/{db}?driver={driver}",
        connect_args={"fast_executemany": True},
    )

    metadata = MetaData()
    # Definimos la tabla principal donde están las matrices base de riesgo.
    matriz_table = Table(
        "MatrizBaseRiesgo",
        metadata,
        Column("id_politica_base_riesgo", Integer, primary_key=True),
        Column("concatenado", String(255)),
        Column("segmento", String(255)),
        Column("permanencia", String(255)),
        Column("factor_prov", DECIMAL(10, 2)),
        Column("clasificacion", String(255)),
        Column("tipo_matriz", String(255)),
        schema=None,  # añade tu schema si aplica
    )

    # Definimos la tabla donde se guarda información adicional de las matrices.
    inventario_table = Table(
        "InventarioMatriz",
        metadata,
        Column("id_inventario_matriz", Integer, primary_key=True),
        Column("id_politica_base_riesgo", Integer),
        Column("subsegmento", String(255)),
        Column("estado", String(255)),
        Column("cobertura", String(255)),
        Column("negocio", String(255)),
    )

    # Definimos la tabla histórica, donde se guarda un registro de cómo estaban las matrices antes de cada cambio.
    hist_table = Table(
        "MatrizBaseRiesgoHist",
        metadata,
        Column("hist_id", Integer, primary_key=True),
        Column("id_politica_base_riesgo", Integer),
        Column("concatenado", String(255)),
        Column("segmento", String(255)),
        Column("permanencia", String(255)),
        Column("factor_prov", DECIMAL(10, 2)),
        Column("clasificacion", String(255)),
        Column("tipo_matriz", String(255)),
        Column("subsegmento", String(255)),
        Column("estado", String(255)),
        Column("cobertura", String(255)),
        Column("negocio", String(255)),
        # fecha_registro se llena con el DEFAULT GETDATE()
        schema=None,
    )

    errors = []
    updated = 0

    # Aquí empieza la parte principal donde se hacen los cambios.
    with engine.begin() as conn:
        """
        Antes de hacer cualquier cambio, guardamos una copia de cómo están todas las matrices en este momento.
        Así, si en el futuro necesitamos saber cómo estaban antes de una actualización, podemos consultarlo en la tabla histórica.
        """
        try:
            # Obtenemos todos los registros actuales de las matrices y su información relacionada.
            snapshot_stmt = select(
                matriz_table.c.id_politica_base_riesgo,
                matriz_table.c.concatenado,
                matriz_table.c.segmento,
                matriz_table.c.permanencia,
                matriz_table.c.factor_prov,
                matriz_table.c.clasificacion,
                matriz_table.c.tipo_matriz,
                inventario_table.c.subsegmento,
                inventario_table.c.estado,
                inventario_table.c.cobertura,
                inventario_table.c.negocio,
            ).select_from(
                matriz_table.outerjoin(
                    inventario_table,
                    matriz_table.c.id_politica_base_riesgo
                    == inventario_table.c.id_politica_base_riesgo,
                )
            )
            snapshot_rows = conn.execute(snapshot_stmt).fetchall()
            # Si hay registros, los guardamos en la tabla histórica.
            if snapshot_rows:
                conn.execute(
                    insert(hist_table), [dict(r._mapping) for r in snapshot_rows]
                )
        except Exception as ex:
            # Si algo falla aquí, simplemente seguimos, ya que esto es solo para respaldo.
            pass

        # Ahora vamos a procesar cada fila que el usuario quiere actualizar.
        for row in matrices:
            id_ = row.get("id_politica_base_riesgo")
            if id_ is None:
                # Si no viene el ID, no podemos hacer nada con esa fila.
                errors.append({"id": None, "error": "Falta id_politica_base_riesgo"})
                continue

            """
            Antes de actualizar, buscamos cómo está actualmente esa fila en la base de datos.
            Esto nos sirve para guardar un respaldo de ese registro específico antes de cambiarlo.
            """
            try:
                join_stmt = (
                    select(
                        matriz_table,
                        inventario_table.c.subsegmento,
                        inventario_table.c.estado,
                        inventario_table.c.cobertura,
                        inventario_table.c.negocio,
                    )
                    .select_from(
                        matriz_table.outerjoin(
                            inventario_table,
                            matriz_table.c.id_politica_base_riesgo
                            == inventario_table.c.id_politica_base_riesgo,
                        )
                    )
                    .where(matriz_table.c.id_politica_base_riesgo == id_)
                )
                current = conn.execute(join_stmt).first()
            except Exception as ex:
                errors.append({"id": id_, "error": f"Consulta fallida: {ex}"})
                continue
            if not current:
                # Si no encontramos el registro, lo reportamos como error.
                errors.append({"id": id_, "error": "ID no encontrado"})
                continue

            """
            Guardamos el estado actual de la fila en la tabla histórica, para tener un registro de cómo estaba antes del cambio.
            """
            try:
                conn.execute(
                    insert(hist_table).values(
                        id_politica_base_riesgo=current.id_politica_base_riesgo,
                        concatenado=current.concatenado,
                        segmento=current.segmento,
                        permanencia=current.permanencia,
                        factor_prov=current.factor_prov,
                        clasificacion=current.clasificacion,
                        tipo_matriz=current.tipo_matriz,
                        subsegmento=current.subsegmento,
                        estado=current.estado,
                        cobertura=current.cobertura,
                        negocio=current.negocio,
                    )
                )
            except Exception as ex:
                errors.append({"id": id_, "error": f"Histórico fallido: {ex}"})
                continue

            """
            Ahora sí, preparamos los datos que realmente se van a actualizar.
            Solo se actualizan los campos que vienen en la petición y que no son nulos.
            """
            matriz_fields = [
                "concatenado",
                "segmento",
                "permanencia",
                "factor_prov",
                "clasificacion",
                "tipo_matriz",
            ]
            inventario_fields = ["subsegmento", "estado", "cobertura", "negocio"]
            update_dict_matriz = {
                field: row[field]
                for field in matriz_fields
                if field in row and row[field] is not None
            }
            update_dict_inventario = {
                field: row[field]
                for field in inventario_fields
                if field in row and row[field] is not None
            }

            if not update_dict_matriz and not update_dict_inventario:
                # Si no hay nada para actualizar, lo reportamos.
                errors.append({"id": id_, "error": "Nada para actualizar"})
                continue
            # Actualizamos la tabla principal si hay cambios para ella.
            if update_dict_matriz:
                stmt = sqlalchemy_update(matriz_table).where(
                    matriz_table.c.id_politica_base_riesgo == id_
                )
                try:
                    result = conn.execute(stmt.values(**update_dict_matriz))
                    updated += result.rowcount
                except Exception as ex:
                    errors.append({"id": id_, "error": str(ex)})
            # Actualizamos la tabla de inventario si hay cambios para ella.
            if update_dict_inventario:
                stmt_inv = sqlalchemy_update(inventario_table).where(
                    inventario_table.c.id_politica_base_riesgo == id_
                )
                try:
                    result_inv = conn.execute(stmt_inv.values(**update_dict_inventario))
                    updated += result_inv.rowcount
                except Exception as ex:
                    errors.append({"id": id_, "error": str(ex)})
    # Al final, dejamos un registro en los logs de cuántas filas se actualizaron y cuántos errores hubo.
    logger.info(
        f"[matrices-save] Matrices actualizadas correctamente. Filas actualizadas: {updated}, Errores: {len(errors)}"
    )
    # Devolvemos un resumen de lo que pasó: si fue exitoso, cuántas filas se actualizaron y detalles de los errores si los hubo.
    return {
        "success": len(errors) == 0,
        "message": f"{updated} filas actualizadas. {len(errors)} errores.",
        "rows_updated": updated,
        "errorRows": [e["id"] for e in errors],
        "errors": errors,
    }


# Endpoint para eliminar un archivo temporal Excel
@router.delete("/delete-temp-file")
async def delete_temp_file(
    filename: str = None, current_user: User = Depends(get_current_admin_user)
):
    """
    Elimina un archivo temporal Excel de la carpeta temporal.

    Este endpoint permite a los administradores eliminar archivos Excel
    temporales que ya no son necesarios, liberando espacio en el servidor.

    Args:
        filename: Nombre del archivo Excel a eliminar
        current_user: Administrador autenticado que realiza la operación

    Permisos: Solo administradores

    Returns:
        Dict: Resultado de la operación indicando si se eliminó correctamente

    Raises:
        HTTPException: Si no se proporciona nombre de archivo o hay error al eliminarlo
    """
    logger.info(
        f"[delete-temp-file] Se inicia el proceso de eliminación del archivo temporal"
    )
    try:
        if not filename:
            logger.warning(
                f"[delete-temp-file] No se proporcionó el nombre del archivo"
            )
            raise HTTPException(
                status_code=400, detail="No se proporcionó el nombre del archivo."
            )
        temp_dir = os.environ.get("TEMP_DIR")
        file_path = os.path.join(temp_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"[delete-temp-file] Archivo temporal eliminado correctamente")
            return {"success": True, "message": "Archivo eliminado."}
        else:
            logger.warning(f"[delete-temp-file] El archivo temporal no existe")
            return {"success": False, "message": "El archivo temporal no existe."}
    except Exception as e:
        logger.error(f"[delete-temp-file] Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el archivo temporal"
        )
