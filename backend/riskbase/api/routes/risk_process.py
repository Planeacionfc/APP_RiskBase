from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, Dict, Any
from ...domain.models.user import User
from ..dependencies import get_current_active_user, get_current_admin_user
from ...services import (
    get_data_sap,
    df_matrices_merge,
    df_matrices_avon_natura,
    df_matrices_otros_tipos,
    df_matrices_merge_raw,
    filter_avon_natura,
    filter_marca_otros,
    upload_dataframe_to_db,
    get_inventory_by_month_year,
    process_dataframe_avon_natura,
    process_dataframe_otras_marcas,
    combine_final_dataframes
)
import pandas as pd
import numpy as np
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, DECIMAL,
    select, insert, update as sqlalchemy_update
)
import os
from datetime import datetime
from pydantic import BaseModel
import traceback

router = APIRouter(prefix="/risk", tags=["risk"])

@router.post("/process", response_model=Dict[str, Any])
async def process_riskbase(
    current_user: User = Depends(get_current_admin_user)
):
    """
    Ejecuta el proceso completo de extracción, transformación y carga de datos de riesgo.
    Solo accesible para administradores.
    """
    try:
        matrices_avon_natura = df_matrices_avon_natura()
        matrices_otros_tipos = df_matrices_otros_tipos()
        
        df_sap = get_data_sap()

        if df_sap is None or df_sap.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudieron obtener datos de SAP"
            )
            
        # 2. Filtro para obtener solo los datos de AVON y NATURA
        df_avon_natura = filter_avon_natura(df_sap)
        # 3. Filtro para obtener los datos de otras marcas
        df_otras_marcas = filter_marca_otros(df_sap)
        
        df_final_avon_natura = process_dataframe_avon_natura(df_avon_natura, matrices_avon_natura)
        
        df_final_otras_marcas= process_dataframe_otras_marcas(df_otras_marcas, matrices_otros_tipos)
        
        df_final_combined = combine_final_dataframes(df_final_avon_natura, df_final_otras_marcas)
        
        excel_file = f"temp_risk_data_{current_user.username}_{datetime.now().strftime('%Y%m%d')}.xlsx"
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
            }
        }
        return result
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al ejecutar el proceso: {str(e)}\n{tb}"
        )

@router.post("/consult-riskbase", response_model=Dict[str, Any])
async def consult_riskbase(
    mes: int = Query(..., ge=1, le=12),
    anio: int = Query(..., ge=2000),
    current_user: User = Depends(get_current_active_user)
):
    """
    Consulta la base de riesgo por mes y año, guarda el DataFrame como archivo Excel temporal y devuelve la info necesaria.
    Accesible para usuarios regulares y administradores.
    """
    try:
        df_final_combined = get_inventory_by_month_year(mes, anio)
        if df_final_combined is None or df_final_combined.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron datos para mes={mes} y año={anio}"
            )

        excel_file = f"temp_risk_data_{current_user.username}_{datetime.now().strftime('%Y%m%d')}.xlsx"
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
            }
        }
        return result
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar la base de riesgo: {str(e)}\n{tb}"
        )

# Endpoint para visualizar el dataframe (usuarios regulares y administradores)
@router.get("/data-view")
async def get_risk_data(
    temp_file: Optional[str] = None,
    limit: int = 25,
    offset: int = 0,
    current_user = Depends(get_current_active_user)
):
    try:
        if not temp_file:
            raise HTTPException(status_code=400, detail="No se proporcionó archivo temporal.")
        temp_dir = os.getenv(
            "TEMP_DIR",
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "temp")
        )
        file_path = os.path.join(temp_dir, temp_file)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Archivo temporal no encontrado.")
        df = pd.read_excel(file_path)

        # Mostar todas las columnas
        df = df.iloc[:, :52] if df.shape[1] >= 52 else df

        # Paginación y saneamiento: inf, -inf y nan → None
        df_paginated = (
            df
            .iloc[offset : offset + limit]
            .replace([np.inf, -np.inf, np.nan], None)
        )

        records = df_paginated.to_dict(orient="records")
        safe_records = jsonable_encoder(records)

        return JSONResponse({
            "data": safe_records,
            "total": len(df),
            "limit": limit,
            "offset": offset,
            "columns": df.columns.tolist()
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los datos: {e}")

# Endpoint para exportar a Excel (usuarios regulares y administradores)
@router.get("/export-excel")
async def export_to_excel(
    filename: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """
    Exporta los datos procesados a un archivo Excel (no elimina el archivo tras la descarga).
    Args:
        filename: Nombre del archivo Excel en la carpeta temp
    Returns:
        FileResponse: Archivo Excel para descargar
    """
    try:
        if filename:
            temp_dir = os.environ.get("TEMP_DIR")
            file_path = os.path.join(temp_dir, filename)
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Archivo temporal no encontrado. Ejecute el proceso primero."
                )
            return FileResponse(
                path=file_path,
                filename=os.path.basename(file_path),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionó el nombre del archivo."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al exportar a Excel: {str(e)}"
        )

# Modelo para recibir el nombre del archivo desde el body JSON
class FileNameRequest(BaseModel):
    filename: str

# Endpoint para guardar en la base de datos
@router.post("/save-to-db")
async def save_to_database(
    request: FileNameRequest,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Guarda los datos procesados en la base de datos (sube el archivo completo, sin filtros).
    Args:
        filename: Archivo temporal generado por el proceso
    Returns:
        Dict: Resultado de la operación
    """
    try:
        temp_dir = os.environ.get("TEMP_DIR")
        filename = request.filename
        file_path = os.path.join(temp_dir, filename)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Archivo temporal no encontrado. Ejecute el proceso primero."
            )
        df = pd.read_excel(file_path)
        upload_dataframe_to_db(df)
        return {
            "success": True,
            "message": "Datos guardados correctamente en la base de datos",
            "rows_saved": len(df)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar en la base de datos: {str(e)}"
        )
    
# Endpoint para obtener todas las matrices de la base de datos (solo administradores)
@router.get("/matrices-view", response_model=Dict[str, Any])
async def get_matrices(
    current_user: User = Depends(get_current_admin_user)
):
    """
    Obtiene todas las matrices almacenadas en la base de datos.
    Solo accesible para administradores.
    
    Returns:
        Dict: Datos de las matrices
    """
    try:
        # Obtener datos de la base de datos
        matrices = df_matrices_merge_raw()
        
        if matrices is None or matrices.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron matrices en la base de datos"
            )
            
        # Convertir a diccionario para la respuesta JSON
        matrices_dict = matrices.to_dict(orient="records")
        
        return {
            "matrices": matrices_dict,
            "total": len(matrices_dict),
            "columns": matrices.columns.tolist()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las matrices: {str(e)}"
        )

# Endpoint para modificar campos de las matrices (solo administradores)
@router.put("/matrices-save", response_model=Dict[str, Any])
async def update_matrices(
    data: Dict[str, Any],
    current_user: User = Depends(get_current_admin_user)
):
    """
    Actualiza los campos factor_prov y clasificacion en MatrizBaseRiesgo,
    guardando previamente el estado antiguo en MatrizBaseRiesgoHist.
    Sólo administradores.
    """
    matrices = data.get("rows") or data.get("matrices") or []
    if not matrices:
        raise HTTPException(status_code=400, detail="No se enviaron filas para actualizar.")

    # Conexión
    usuario = os.getenv("DB_USER")
    pwd     = os.getenv("DB_PASSWORD")
    server  = os.getenv("DB_SERVER")
    db      = os.getenv("DATABASE")
    driver  = "ODBC Driver 17 for SQL Server"
    engine = create_engine(
        f"mssql+pyodbc://{usuario}:{pwd}@{server}/{db}?driver={driver}",
        connect_args={"fast_executemany": True}
    )

    metadata = MetaData()
    # Tabla principal
    matriz_table = Table(
        "MatrizBaseRiesgo", metadata,
        Column("id_politica_base_riesgo", Integer, primary_key=True),
        Column("concatenado",           String(255)),
        Column("segmento",              String(255)),
        Column("permanencia",           String(255)),
        Column("factor_prov",           DECIMAL(10, 2)),
        Column("clasificacion",         String(255)),
        Column("tipo_matriz",           String(255)),
        schema=None  # añade tu schema si aplica
    )

    inventario_table = Table(
        "InventarioMatriz", metadata,
        Column("id_inventario_matriz", Integer, primary_key=True),
        Column("id_politica_base_riesgo", Integer),
        Column("subsegmento", String(255)),
        Column("estado", String(255)),
        Column("cobertura", String(255)),
        Column("negocio", String(255)),
    )

    # Tabla histórica
    hist_table = Table(
        "MatrizBaseRiesgoHist", metadata,
        Column("hist_id",                 Integer, primary_key=True),
        Column("id_politica_base_riesgo", Integer),
        Column("concatenado",             String(255)),
        Column("segmento",                String(255)),
        Column("permanencia",             String(255)),
        Column("factor_prov",             DECIMAL(10, 2)),
        Column("clasificacion",           String(255)),
        Column("tipo_matriz",             String(255)),
        Column("subsegmento",             String(255)),
        Column("estado",                  String(255)),
        Column("cobertura",               String(255)),
        Column("negocio",                 String(255)),
        # fecha_registro se llena con el DEFAULT GETDATE()
        schema=None
    )

    errors = []
    updated = 0

    with engine.begin() as conn:
        # 0) SNAPSHOT COMPLETO: Guardar todos los registros actuales en el histórico antes de cualquier update
        try:
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
                inventario_table.c.negocio
            ).select_from(
                matriz_table.outerjoin(
                    inventario_table,
                    matriz_table.c.id_politica_base_riesgo == inventario_table.c.id_politica_base_riesgo
                )
            )
            snapshot_rows = conn.execute(snapshot_stmt).fetchall()
            if snapshot_rows:
                conn.execute(
                    insert(hist_table),
                    [dict(r._mapping) for r in snapshot_rows]
                )
        except Exception as ex:
            pass

        for row in matrices:
            id_ = row.get("id_politica_base_riesgo")
            if id_ is None:
                errors.append({"id": None, "error": "Falta id_politica_base_riesgo"})
                continue

            # 1) Recuperar estado actual (JOIN para snapshot)
            try:
                join_stmt = select(
                    matriz_table,
                    inventario_table.c.subsegmento,
                    inventario_table.c.estado,
                    inventario_table.c.cobertura,
                    inventario_table.c.negocio
                ).select_from(
                    matriz_table.outerjoin(
                        inventario_table,
                        matriz_table.c.id_politica_base_riesgo == inventario_table.c.id_politica_base_riesgo
                    )
                ).where(matriz_table.c.id_politica_base_riesgo == id_)
                current = conn.execute(join_stmt).first()
            except Exception as ex:
                errors.append({"id": id_, "error": f"Consulta fallida: {ex}"})
                continue
            if not current:
                errors.append({"id": id_, "error": "ID no encontrado"})
                continue

            # 2) Insertar snapshot en el histórico
            try:
                conn.execute(
                    insert(hist_table).values(
                        id_politica_base_riesgo = current.id_politica_base_riesgo,
                        concatenado             = current.concatenado,
                        segmento                = current.segmento,
                        permanencia             = current.permanencia,
                        factor_prov             = current.factor_prov,
                        clasificacion           = current.clasificacion,
                        tipo_matriz             = current.tipo_matriz,
                        subsegmento             = current.subsegmento,
                        estado                  = current.estado,
                        cobertura               = current.cobertura,
                        negocio                 = current.negocio
                    )
                )
            except Exception as ex:
                errors.append({"id": id_, "error": f"Histórico fallido: {ex}"})
                continue

            # 3) Actualizar ambas tablas según corresponda
            matriz_fields = [
                "concatenado", "segmento", "permanencia", "factor_prov", "clasificacion", "tipo_matriz"
            ]
            inventario_fields = ["subsegmento", "estado", "cobertura", "negocio"]
            update_dict_matriz = {field: row[field] for field in matriz_fields if field in row and row[field] is not None}
            update_dict_inventario = {field: row[field] for field in inventario_fields if field in row and row[field] is not None}

            if not update_dict_matriz and not update_dict_inventario:
                errors.append({"id": id_, "error": "Nada para actualizar"})
                continue
            # Update MatrizBaseRiesgo
            if update_dict_matriz:
                stmt = sqlalchemy_update(matriz_table).where(
                    matriz_table.c.id_politica_base_riesgo == id_
                )
                try:
                    result = conn.execute(stmt.values(**update_dict_matriz))
                    updated += result.rowcount
                except Exception as ex:
                    errors.append({"id": id_, "error": str(ex)})
            # Update InventarioMatriz
            if update_dict_inventario:
                stmt_inv = sqlalchemy_update(inventario_table).where(
                    inventario_table.c.id_politica_base_riesgo == id_
                )
                try:
                    result_inv = conn.execute(stmt_inv.values(**update_dict_inventario))
                    updated += result_inv.rowcount
                except Exception as ex:
                    errors.append({"id": id_, "error": str(ex)})
    return {
        "success": len(errors) == 0,
        "message": f"{updated} filas actualizadas. {len(errors)} errores.",
        "rows_updated": updated,
        "errorRows": [e["id"] for e in errors],
        "errors": errors
    }


# Endpoint para eliminar archivo temporal
@router.delete("/delete-temp-file")
async def delete_temp_file(
    filename: str = None,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Elimina un archivo temporal Excel de la carpeta temp.
    Args:
        filename: Nombre del archivo Excel a eliminar
    Returns:
        Dict: Resultado de la operación
    """
    try:
        if not filename:
            raise HTTPException(status_code=400, detail="No se proporcionó el nombre del archivo.")
        temp_dir = os.environ.get("TEMP_DIR")
        file_path = os.path.join(temp_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"success": True, "message": "Archivo eliminado."}
        else:
            return {"success": False, "message": "El archivo no existe."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar archivo: {str(e)}")
