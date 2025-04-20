from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from typing import List, Optional, Dict, Any
from ...domain.models.user import User
from ..dependencies import get_current_active_user, get_current_admin_user
from ...services import (
    get_data_sap,
    df_matrices_merge,
    process_dataframe_columns,
    export_dataframe_to_excel,
    upload_dataframe_to_db
)
import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime
import io
import json

router = APIRouter(prefix="/risk", tags=["risk"])

# Endpoint para ejecutar el proceso completo (usuarios regulares y administradores)
@router.post("/process", response_model=Dict[str, Any])
async def execute_risk_process(
    current_user: User = Depends(get_current_active_user)
):
    """
    Ejecuta el proceso completo de extracción, transformación y carga de datos de riesgo.
    
    Returns:
        Dict: Resumen del proceso con estadísticas básicas
    """
    try:
        # 1. Obtener datos de las matrices de la base de datos
        matrices = df_matrices_merge()
        
        # 2. Extraer datos de SAP
        df_sap = get_data_sap()
        if df_sap is None or df_sap.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudieron obtener datos de SAP"
            )
            
        # 3. Procesar los datos aplicando todas las reglas de negocio
        df_final_combined = process_dataframe_columns(df_sap, matrices)


        # 4. Guardar el DataFrame procesado para su uso posterior
        temp_file = f"temp_risk_data_{current_user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pkl"
        temp_dir = os.environ.get("TEMP_DIR", ".")
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, temp_file)
        df_final_combined.to_pickle(file_path)
        
        # 5. Devolver estadísticas básicas
        result = {
            "success": True,
            "message": "Proceso ejecutado correctamente",
            "rows_processed": len(df_final_combined),
            "columns": df_final_combined.columns.tolist(),
            "temp_file": temp_file,
            "summary": {
                "total_records": len(df_final_combined),
                # Agregar más estadísticas relevantes según necesidad
            }
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al ejecutar el proceso: {str(e)}"
        )

# Endpoint para visualizar el dataframe (usuarios regulares y administradores)
@router.get("/data")
async def get_risk_data(
    temp_file: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene los datos procesados para visualización.
    
    Args:
        temp_file: Archivo temporal generado por el proceso
        limit: Número máximo de registros a devolver
        offset: Número de registros a saltar
        
    Returns:
        Dict: Datos paginados y metadatos
    """
    try:
        if temp_file:
            # Cargar desde archivo temporal
            temp_dir = os.environ.get("TEMP_DIR", ".")
            file_path = os.path.join(temp_dir, temp_file)
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Archivo temporal no encontrado. Ejecute el proceso primero."
                )
            df = pd.read_pickle(file_path)
        else:
            # Si no hay archivo temporal, intentar obtener los datos más recientes
            # Esto podría ser de una tabla de la base de datos donde se guardan los resultados
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay datos disponibles. Ejecute el proceso primero."
            )
        
        # Obtener el total de registros
        total_records = len(df)
        
        # Aplicar paginación
        df_paginated = df.iloc[offset:offset+limit]
        
        # Convertir a diccionario para la respuesta JSON
        records = df_paginated.to_dict(orient="records")
        
        return {
            "data": records,
            "total": total_records,
            "limit": limit,
            "offset": offset,
            "columns": df.columns.tolist()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los datos: {str(e)}"
        )

# Endpoint para exportar a Excel (usuarios regulares y administradores)
@router.get("/export-excel")
async def export_to_excel(
    temp_file: Optional[str] = None,
    filename: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """
    Exporta los datos procesados a un archivo Excel.
    
    Args:
        temp_file: Archivo temporal generado por el proceso
        filename: Nombre personalizado para el archivo Excel
        
    Returns:
        FileResponse: Archivo Excel para descargar
    """
    try:
        if temp_file:
            # Cargar desde archivo temporal
            temp_dir = os.environ.get("TEMP_DIR", ".")
            file_path = os.path.join(temp_dir, temp_file)
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Archivo temporal no encontrado. Ejecute el proceso primero."
                )
            df = pd.read_pickle(file_path)
        else:
            # Si no hay archivo temporal, intentar obtener los datos más recientes
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay datos disponibles. Ejecute el proceso primero."
            )
        
        # Exportar a Excel
        excel_path = export_dataframe_to_excel(df, filename)
        
        if not excel_path or not os.path.exists(excel_path):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al generar el archivo Excel"
            )
            
        return FileResponse(
            path=excel_path,
            filename=os.path.basename(excel_path),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al exportar a Excel: {str(e)}"
        )

# Endpoint para guardar en la base de datos (usuarios regulares y administradores)
@router.post("/save-to-db")
async def save_to_database(
    temp_file: str,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Guarda los datos procesados en la base de datos.
    
    Args:
        temp_file: Archivo temporal generado por el proceso
        
    Returns:
        Dict: Resultado de la operación
    """
    try:
        # Cargar desde archivo temporal
        temp_dir = os.environ.get("TEMP_DIR", ".")
        file_path = os.path.join(temp_dir, temp_file)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Archivo temporal no encontrado. Ejecute el proceso primero."
            )
        df = pd.read_pickle(file_path)
        
        # Guardar en la base de datos
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

# --- ENDPOINTS SOLO PARA ADMINISTRADORES ---

# Endpoint para obtener todas las matrices de la base de datos (solo administradores)
@router.get("/matrices", response_model=Dict[str, Any])
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
        matrices = df_matrices_merge()
        
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
@router.put("/matrices", response_model=Dict[str, Any])
async def update_matrices(
    data: Dict[str, Any],
    current_user: User = Depends(get_current_admin_user)
):
    """
    Actualiza los campos de las matrices en la base de datos.
    Solo accesible para administradores.
    
    Args:
        data: Datos actualizados de las matrices
        
    Returns:
        Dict: Resultado de la actualización
    """
    try:
        # Convertir los datos recibidos a un DataFrame
        df_updated = pd.DataFrame(data.get("matrices", []))
        
        if df_updated.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron datos para actualizar"
            )
            
        # Aquí implementar la lógica para actualizar la base de datos
        # Por ejemplo, usando SQLAlchemy para hacer un update masivo
        
        # Ejemplo simplificado (en una implementación real, esto sería más complejo)
        server = os.getenv("DB_SERVER")
        database = os.getenv("DATABASE")
        usuario = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        driver = "ODBC Driver 17 for SQL Server"
        
        engine = create_engine(
            f"mssql+pyodbc://{usuario}:{password}@{server}/{database}?driver={driver}"
        )
        
        # Guardar los cambios en la base de datos
        # Nota: Esto es un ejemplo simplificado, en una implementación real
        # se debería manejar con más cuidado las actualizaciones
        df_updated.to_sql("MatrizBaseRiesgo", con=engine, if_exists="replace", index=False)
        
        return {
            "success": True,
            "message": "Matrices actualizadas correctamente",
            "rows_updated": len(df_updated)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar las matrices: {str(e)}"
        )
