from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from ...domain.models.user import User
from ..dependencies import get_current_active_user, get_current_admin_user
from ...services import (
    get_data_sap,
    df_matrices_merge,
    process_dataframe_columns,
    upload_dataframe_to_db
)
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
from datetime import datetime
import io
import json
from pydantic import BaseModel

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


        # 4. Guardar el DataFrame procesado como archivo Excel para su uso posterior
        excel_file = f"temp_risk_data_{current_user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        temp_dir = os.environ.get("TEMP_DIR")
        os.makedirs(temp_dir, exist_ok=True)
        excel_path = os.path.join(temp_dir, excel_file)
        df_final_combined.to_excel(excel_path, index=False)
        
        # 5. Devolver estadísticas básicas
        result = {
            "success": True,
            "message": "Proceso ejecutado correctamente",
            "rows_processed": len(df_final_combined),
            "columns": df_final_combined.columns.tolist(),
            "excel_file": excel_file,
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

        # Limitar a primeras 25 columnas
        df = df.iloc[:, :25] if df.shape[1] >= 25 else df

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


# --- ENDPOINTS SOLO PARA ADMINISTRADORES --- 

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
@router.put("/matrices-save", response_model=Dict[str, Any])
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

# Endpoint para eliminar archivo temporal
@router.delete("/delete-temp-file")
async def delete_temp_file(
    filename: str = None,
    current_user: User = Depends(get_current_active_user)
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
