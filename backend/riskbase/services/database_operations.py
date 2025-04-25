import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from typing import Dict, Any
from datetime import datetime

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

def df_matrices_merge_raw():
    """
    Extrae los datos de ambas tablas y los unifica utilizando pd.merge(),
    pero NO modifica los campos de texto ni normaliza factor_prov.
    Devuelve los datos exactamente como están en la base de datos.
    """
    df_inventario = get_inventario_matriz()
    df_matrices = get_matrices_base_riesgo()
    # Unificación utilizando la columna en común 'id_politica_base_riesgo'
    df_matrices_merge = pd.merge(
        df_inventario, df_matrices,
        on="id_politica_base_riesgo",
        how="inner"  # Cambia 'inner' por 'left' o 'outer' según lo requieras
    )
    # NO se modifica ningún campo
    return df_matrices_merge

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

def export_dataframe_to_excel(df: pd.DataFrame, filename: str = None, output_dir: str = None) -> str:
    """
    Exporta un DataFrame a un archivo Excel en la ruta especificada o en el directorio de trabajo actual.

    Args:
        df: DataFrame a exportar
        filename: Nombre base del archivo (opcional)
        output_dir: Ruta de destino (opcional)

    Returns:
        str: Ruta del archivo Excel creado
    """
    # Usar directorio de trabajo actual si no se especifica output_dir
    if output_dir is None:
        output_dir = os.getcwd()

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
        print(f"Error al exportar a Excel: {e}")
        raise

def get_inventory_by_month_year(mes: int, anio: int) -> pd.DataFrame:
    """
    Consulta InventarioBaseRiesgo filtrando mes y año de registro.
    """
    usuario = os.getenv("DB_USER")
    pwd     = os.getenv("DB_PASSWORD")
    server  = os.getenv("DB_SERVER")
    db      = os.getenv("DATABASE")
    driver  = "ODBC Driver 17 for SQL Server"

    engine = create_engine(
        f"mssql+pyodbc://{usuario}:{pwd}@{server}/{db}?driver={driver}",
        connect_args={"fast_executemany": True}
    )
    sql = text("""
        SELECT
            mes_registro,
            año_registro,
            [NEGOCIO INVENTARIOS],
            [AÑO NATURAL/MES],
            [TIPO MATERIAL INVENTARIO],
            [MARCA DE QM],
            [MATERIAL],
            [DESCRIPCIÓN],
            [UNIDAD MEDIDA],
            [CENTRO],
            [CODIGO ALMACEN CLIENTE],
            [INDICADOR STOCK ESPEC.],
            [NÚM.STOCK.ESP.],
            [LOTE],
            [CREADO EL],
            [FECH. FABRICACIÓN],
            [FECH, CADUCIDAD/FECH PREF. CONSUMO],
            [FECHA BLOQUEADO],
            [FECHA OBSOLETO],
            [FECHA ENTRADA],
            [RANGO OBSOLETO 2],
            [RANGO COBERTURA],
            [RANGO DE PERMANENCIA],
            [RANGO BLOQUEADO],
            [RANGO OBSOLETO],
            [RANGO VENCIDOS],
            [PRÓXIMO A VENCER],
            [RANGO PRÓX.VENCER MM],
            [RANGO PRÓXIMOS A VEN],
            [TIPO DE MATERIAL (I)],
            [COSTO UNITARIO REAL],
            [INVENTARIO DISPONIBL],
            [INVENTARIO NO DISPON],
            [VALOR OBSOLETO],
            [VALOR BLOQUEADO MM],
            [VALOR TOTAL MM],
            [PERMANENCIA],
            [MARCA CONCAT],
            [SEGMENTACION],
            [SUBSEGMENTACION],
            [RANGO DE PERMANENCIA 2],
            [STATUS CONS],
            [VALOR DEF],
            [RANGO OBSOLESCENCIA],
            [RANGO VENCIDO 2],
            [RANGO BLOQUEADO 2],
            [RANGO CONS],
            [TIEMPO BLOQUEO],
            [FACTOR PROV],
            [CLAS BASE RIESGO],
            [BASE RIESGO],
            [PROVISION]
          FROM InventarioBaseRiesgo
         WHERE mes_registro = :mes
           AND año_registro = :anio
    """)
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={"mes": mes, "anio": anio})

    # Convertir columnas numéricas
    columnas_numericas = [
        "COSTO UNITARIO REAL",
        "INVENTARIO DISPONIBL",
        "INVENTARIO NO DISPON",
        "VALOR OBSOLETO",
        "VALOR BLOQUEADO MM",
        "VALOR TOTAL MM",
        "PERMANENCIA",
        "FACTOR PROV",
        "VALOR DEF",
        "BASE RIESGO",
        "PROVISION"
    ]
    for col in columnas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convertir columnas de fechas
    columnas_fecha = [
        "FECHA ENTRADA",
        "CREADO EL",
        "FECHA BLOQUEADO",
        "FECHA OBSOLETO",
        "FECH. FABRICACIÓN",
        "FECH, CADUCIDAD/FECH PREF. CONSUMO"
    ]
    for col in columnas_fecha:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df