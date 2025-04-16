import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

def get_sql_engine():
    """
    Establece la conexión a SQL Server mediante SQLAlchemy.
    Configura los datos de conexión utilizando variables de entorno.
    """
    try:
        connection_string = (
            "mssql+pyodbc://{user}:{pwd}@{server}/{db}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
        ).format(
            user=os.getenv("DB_USER"),
            pwd=os.getenv("DB_PASSWORD"),
            server=os.getenv("DB_SERVER"),
            db=os.getenv("DATABASE")
        )
        engine = create_engine(connection_string)
        print("Conexión exitosa a la base de datos.")
        return engine
    except Exception as e:
        print(f"Error al conectar a la base de datos: {str(e)}")
        raise

def execute_query(query):
    """
    Ejecuta el query en la base de datos y retorna un DataFrame utilizando SQLAlchemy.
    """
    engine = get_sql_engine()
    try:
        df = pd.read_sql(query, engine)
    except Exception as e:
        print(f"Error al ejecutar el query: {str(e)}")
        df = pd.DataFrame()  # Retorna un DataFrame vacío en caso de error
    finally:
        engine.dispose()  # Cierra la conexión
    return df

def get_inventario_matriz():
    """
    Extrae todos los registros de la tabla InventarioMatriz.
    """
    query = """
    SELECT 
        id_politica_base_riesgo,
        subsegmento,
        negocio,
        estado,
        cobertura
    FROM InventarioMatriz
    """
    return execute_query(query)

def get_matrices_base_riesgo():
    """
    Extrae todos los registros de la tabla MatrizBaseRiesgo.
    """
    query = """
    SELECT
        id_politica_base_riesgo,
        concatenado,
        segmento,
        permanencia,
        factor_prov,
        clasificacion,
        tipo_matriz
    FROM MatrizBaseRiesgo
    """
    return execute_query(query)

def df_matrices_merge():
    """
    Extrae los datos de ambas tablas, los unifica utilizando pd.merge() y convierte
    todos los campos de texto a mayúsculas de forma vectorizada.
    """
    df_inventario = get_inventario_matriz()
    df_matrices = get_matrices_base_riesgo()
    
    # Unificación utilizando la columna en común 'id_politica_base_riesgo'
    df_matrices_merge = pd.merge(df_inventario, df_matrices, 
                        on="id_politica_base_riesgo", 
                        how="inner")  # Cambia 'inner' por 'left' o 'outer' según lo requieras
    
    # Convertir los campos de tipo string a mayúsculas de forma vectorizada
    for col in df_matrices_merge.select_dtypes(include=["object"]).columns:
        df_matrices_merge[col] = df_matrices_merge[col].str.upper()
    
    # Convertir 'factor_prov' a float y normalizarlo
    df_matrices_merge["factor_prov"] = df_matrices_merge["factor_prov"].astype(float) / 100.0
    
    return df_matrices_merge

def upload_dataframe_to_db(df_final_combined: pd.DataFrame) -> None:
    """
    Sube el DataFrame 'df_final_combined' a la base de datos en la tabla 'InventarioBaseRiesgo'.
    Se utiliza SQLAlchemy para establecer la conexión y el método to_sql de pandas para insertar
    todos los registros (append). Se asume que la tabla ya existe y que los nombres de columnas en 
    el DataFrame coinciden exactamente con los de la tabla en la base de datos.
    
    Args:
        df_final_combined (pd.DataFrame): DataFrame con las columnas y el orden requeridos.
    
    Returns:
        None
    """
    connection_string = (
            "mssql+pyodbc://{user}:{pwd}@{server}/{db}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
        ).format(
            user=os.getenv("DB_USER"),
            pwd=os.getenv("DB_PASSWORD"),
            server=os.getenv("DB_SERVER"),
            db=os.getenv("DATABASE")
        )
    
    # Crear el engine de SQLAlchemy con fast_executemany habilitado
    engine = create_engine(connection_string, fast_executemany=True)
    
    try:
        # Insertar datos en la tabla InventarioBaseRiesgo. 
        # if_exists='append' se utiliza para agregar los datos sin reemplazar la tabla.
        df_final_combined.to_sql(
            name='InventarioBaseRiesgo',
            con=engine,
            if_exists='append',
            index=False,
            chunksize=1000  # Tamaño del chunk para inserciones masivas
        )
        print("Datos subidos correctamente a InventarioBaseRiesgo.")
    except Exception as e:
        print("Error al subir el DataFrame a la base de datos:", e)
    finally:
        engine.dispose()

def export_dataframe_to_excel(df: pd.DataFrame, filename: str = None) -> str:
    """
    Exporta un DataFrame a un archivo Excel con la fecha actual y lo guarda en una ruta específica.

    Args:
        df: DataFrame a exportar
        filename: Nombre base del archivo (opcional)

    Returns:
        str: Ruta del archivo Excel creado
    """
    # Definir la ruta de destino
    output_dir = r"C:\Users\prac.planeacionfi\OneDrive - Prebel S.A BIC\Escritorio\PRUEBAS BASE RIESGO"

    # Crear el nombre del archivo con la fecha actual
    current_date = datetime.now().strftime("%d-%m-%Y")
    if not filename:
        filename = f"Análisis_BaseRiesgo_Final_{current_date}.xlsx"

    # Crear la ruta completa
    file_path = os.path.join(output_dir, filename)

    # Asegurar que el directorio existe
    os.makedirs(output_dir, exist_ok=True)

    # Exportar a Excel
    try:
        df.to_excel(file_path, index=False, sheet_name="Base de Riesgo")
        print(f"Archivo Excel creado exitosamente: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error al exportar a Excel: {str(e)}")
        return None
