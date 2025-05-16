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
    Configura los datos de conexión utilizando variables de entorno definidas en el archivo .env.
    
    Las variables de entorno requeridas son:
    - DB_USER: Usuario de la base de datos
    - DB_PASSWORD: Contraseña del usuario
    - DB_SERVER: Dirección del servidor SQL
    - DATABASE: Nombre de la base de datos
    
    Returns:
        sqlalchemy.engine.Engine: Objeto engine de SQLAlchemy configurado para la conexión a SQL Server.
        
    Raises:
        Exception: Si ocurre un error durante la conexión a la base de datos.
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
    Gestiona automáticamente la conexión y desconexión a la base de datos.
    
    Args:
        query (str): Consulta SQL a ejecutar en la base de datos.
        
    Returns:
        pandas.DataFrame: DataFrame con los resultados de la consulta.
        En caso de error, retorna un DataFrame vacío.
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
    Obtiene los campos id_politica_base_riesgo, subsegmento, negocio, estado y cobertura.
    
    Returns:
        pandas.DataFrame: DataFrame con todos los registros de la tabla InventarioMatriz.
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
    Obtiene los campos id_politica_base_riesgo, concatenado, segmento, permanencia,
    factor_prov, clasificacion y tipo_matriz.
    
    Returns:
        pandas.DataFrame: DataFrame con todos los registros de la tabla MatrizBaseRiesgo.
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
    
    Realiza una unión interna (inner join) entre las tablas InventarioMatriz y MatrizBaseRiesgo
    utilizando la columna 'id_politica_base_riesgo' como clave de unión.
    
    Returns:
        pandas.DataFrame: DataFrame unificado con los datos originales sin modificar.
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
    los campos de texto a mayúsculas de forma vectorizada y normaliza el factor_prov.
    
    Realiza las siguientes operaciones:
    1. Extrae datos de las tablas InventarioMatriz y MatrizBaseRiesgo
    2. Realiza una unión interna (inner join) utilizando 'id_politica_base_riesgo'
    3. Convierte todos los campos de texto a mayúsculas
    4. Normaliza el campo 'factor_prov' dividiéndolo por 100 (convierte de porcentaje a decimal)
    
    Returns:
        pandas.DataFrame: DataFrame unificado con los textos en mayúsculas y factor_prov normalizado.
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

def df_matrices_avon_natura():
    """
    Extrae los datos de ambas tablas, las unifica utilizando pd.merge(),
    convierte todos los campos de texto a mayúsculas de forma vectorizada,
    normaliza el factor provisional y, finalmente, filtra solo las filas
    donde 'tipo_matriz' == 'MATRIZ NATURACO'.
    
    Realiza las siguientes operaciones:
    1. Extrae datos de las tablas InventarioMatriz y MatrizBaseRiesgo
    2. Realiza una unión interna (inner join) utilizando 'id_politica_base_riesgo'
    3. Convierte todos los campos de texto a mayúsculas
    4. Normaliza el campo 'factor_prov' dividiéndolo por 100
    5. Filtra solo las filas donde tipo_matriz es 'MATRIZ NATURACO'
    
    Returns:
        pandas.DataFrame: DataFrame filtrado que contiene solo los registros de tipo 'MATRIZ NATURACO'.
    """
    # 1. Extraer los DataFrames base
    df_inventario = get_inventario_matriz()
    df_matrices   = get_matrices_base_riesgo()
    
    # 2. Unirlos por la clave foránea
    df = pd.merge(
        df_inventario,
        df_matrices,
        on="id_politica_base_riesgo",
        how="inner"  # o 'left' / 'outer' según necesidad
    )
    
    # 3. Pasar a mayúsculas todas las columnas de texto
    text_cols = df.select_dtypes(include="object").columns
    for c in text_cols:
        df[c] = df[c].str.upper()
    
    # 4. Normalizar el factor provisional (de porcentaje a [0–1])
    df["factor_prov"] = df["factor_prov"].astype(float) / 100.0
    
    # 5. Filtrar solo las filas de 'Matriz NaturaCo'
    #    (ten en cuenta que ya convertimos todo a mayúsculas)
    df = df[df["tipo_matriz"] == "MATRIZ NATURACO"].reset_index(drop=True)
    
    return df

def df_matrices_otros_tipos():
    """
    Devuelve solo las filas de df_merge donde 'tipo_matriz' sea distinto de 'Matriz NaturaCo'.
    Útil para aislar todas las demás matrices.
    
    Realiza las siguientes operaciones:
    1. Extrae datos de las tablas InventarioMatriz y MatrizBaseRiesgo
    2. Realiza una unión interna (inner join) utilizando 'id_politica_base_riesgo'
    3. Convierte todos los campos de texto a mayúsculas
    4. Normaliza el campo 'factor_prov' dividiéndolo por 100
    5. Filtra solo las filas donde tipo_matriz NO es 'MATRIZ NATURACO'
    
    Returns:
        pandas.DataFrame: DataFrame filtrado que contiene solo los registros que NO son de tipo 'MATRIZ NATURACO'.
    """
    # 1. Extraer los DataFrames base
    df_inventario = get_inventario_matriz()
    df_matrices   = get_matrices_base_riesgo()
    
    # 2. Unirlos por la clave foránea
    df = pd.merge(
        df_inventario,
        df_matrices,
        on="id_politica_base_riesgo",
        how="inner"  # o 'left' / 'outer' según necesidad
    )
    
    # 3. Pasar a mayúsculas todas las columnas de texto
    text_cols = df.select_dtypes(include="object").columns
    for c in text_cols:
        df[c] = df[c].str.upper()
    
    # 4. Normalizar el factor provisional (de porcentaje a [0–1])
    df["factor_prov"] = df["factor_prov"].astype(float) / 100.0
    
    # Filtramos aquellas filas cuyo tipo de matriz NO sea 'MATRIZ NATURACO'
    mask = df["tipo_matriz"] != "MATRIZ NATURACO"
    
    return df[mask].reset_index(drop=True)

def upload_dataframe_to_db(df_final_combined: pd.DataFrame) -> None:
    """
    Sube el DataFrame 'df_final_combined' a la base de datos en la tabla 'InventarioBaseRiesgo'.
    Se utiliza SQLAlchemy para establecer la conexión y el método to_sql de pandas para insertar
    todos los registros (append). Se asume que la tabla ya existe y que los nombres de columnas en 
    el DataFrame coinciden exactamente con los de la tabla en la base de datos.
    
    La función realiza las siguientes operaciones:
    1. Establece una conexión a la base de datos SQL Server utilizando variables de entorno
    2. Crea un engine de SQLAlchemy con fast_executemany habilitado para mejorar el rendimiento
    3. Inserta los datos del DataFrame en la tabla 'InventarioBaseRiesgo' en modo 'append'
    4. Utiliza un tamaño de chunk de 1000 registros para optimizar las inserciones masivas
    
    Args:
        df_final_combined (pd.DataFrame): DataFrame con las columnas y el orden requeridos.
            Los nombres de las columnas deben coincidir exactamente con los de la tabla en la base de datos.
    
    Returns:
        None
        
    Note:
        Esta función requiere que las variables de entorno DB_USER, DB_PASSWORD, DB_SERVER y DATABASE
        estén correctamente configuradas en el archivo .env.
        
    Raises:
        Exception: Si ocurre un error durante la subida de datos a la base de datos.
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
    Si no se especifica un nombre de archivo, genera uno automáticamente con la fecha actual.
    Crea el directorio de destino si no existe.

    Args:
        df (pd.DataFrame): DataFrame que se desea exportar a Excel.
        filename (str, opcional): Nombre personalizado para el archivo Excel. 
            Si no se proporciona, se genera automáticamente con formato "Análisis_BaseRiesgo_Final_DD-MM-YYYY.xlsx".
        output_dir (str, opcional): Ruta del directorio donde se guardará el archivo. 
            Si no se proporciona, se usa el directorio de trabajo actual.

    Returns:
        str: Ruta completa del archivo Excel creado.
        
    Raises:
        Exception: Si ocurre un error durante la exportación a Excel.
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
    Consulta la tabla InventarioBaseRiesgo filtrando por mes y año de registro.
    Obtiene todos los campos de la tabla y realiza conversiones de tipos de datos para
    columnas numéricas y fechas.
    
    Args:
        mes (int): Número del mes a consultar (1-12).
        anio (int): Año a consultar (formato de 4 dígitos, ej: 2023).
        
    Returns:
        pandas.DataFrame: DataFrame con los registros filtrados por mes y año.
        Las columnas numéricas y de fechas son convertidas a sus tipos de datos correspondientes.
    
    Note:
        Las columnas numéricas se convierten usando pd.to_numeric con errors='coerce'.
        Las columnas de fechas se convierten usando pd.to_datetime con errors='coerce'.
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
            [TIEMPO BLOQUEADO],
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