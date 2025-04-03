import pandas as pd, numpy as np
from sqlalchemy import create_engine
import os
from typing import List
from datetime import datetime
import win32com.client as win32
from pretty_html_table import build_table
from dotenv import load_dotenv
from pyrfc._cyrfc import (
    Connection,
    ABAPApplicationError,
    LogonError,
    CommunicationError,
)


load_dotenv()

# ----------- FUNCION PARA CONECTARSE A LA BASE DE DATOS DE LA BASE DE RIESGOS  --------- #


def get_data_riskbase():
    """
    Función para obtener datos de la tabla de la base de datos de RiskBase.

    Returns:
        pd.DataFrame: DataFrame con los datos de la consulta
    """
    try:
        # Datos de conexión
        server = os.getenv("DB_SERVER")
        database = os.getenv("DATABASE")
        usuario = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        driver = "ODBC Driver 17 for SQL Server"  # Driver de conexión a la base de datos de SQL Server

        # Crear el motor de conexión
        engine = create_engine(
            f"mssql+pyodbc://{usuario}:{password}@{server}/{database}?driver={driver}"
        )

        # Consulta SQL
        query = "SELECT concatenado, segmento_subsegmento_estado, permanencia, factor_prov, clasificacion FROM ObsoletosBloqueadosVencidos"

        # Leer los datos en un DataFrame
        df_database = pd.read_sql(query, con=engine)

        return df_database

    except Exception as e:
        print(f"Error al obtener datos: {str(e)}")
        return None

    finally:
        # Cerrar la conexión
        if "engine" in locals():
            engine.dispose()


# ----------- ESTRUCTURA PARA TRANSFORMAR Y CONSUMIR CUBO SAP  --------- #


class SAPConnection:
    def __init__(self, ashost, sysnr, client, user, passwd, lang):
        """
        Inicializa la conexión a SAP.
        """
        self.connection_params = {
            "ashost": ashost,
            "sysnr": sysnr,
            "client": client,
            "user": user,
            "passwd": passwd,
            "lang": lang,
        }
        self.connection = None

    def open_connection(self):
        """
        Abre una conexión a SAP con los parámetros especificados.
        """
        if self.connection is None:
            self.connection = Connection(**self.connection_params)
        return self.connection

    def close_connection(self):
        """
        Cierra la conexión a SAP.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query_name, view_id, parameters):
        """
        Ejecuta una consulta a SAP con parámetros dinámicos.

        Args:
            query_name (str): Nombre del query SAP.
            view_id (str): ID de la vista.
            parameters (list of tuples): Lista de parámetros en formato (nombre, valor).

        Returns:
            dict: Resultado de la consulta.
        """
        self.open_connection()
        # Construir la lista de parámetros dinámicamente
        formatted_parameters = [{"NAME": p[0], "VALUE": p[1]} for p in parameters]
        formatted_parameters += []

        print("🛠 Sending Parameters to SAP BW:")  ##DEBUGGING
        for param in formatted_parameters:
            print(f"{param['NAME']} = {param['VALUE']}")

        try:
            result = self.connection.call(
                "RRW3_GET_QUERY_VIEW_DATA",
                I_QUERY=query_name,
                I_VIEW_ID=view_id,
                I_T_PARAMETER=formatted_parameters,
            )
            print("✅ Query executed successfully!")  ##DEBUGGING
            return result
        except ABAPApplicationError as error:
            print("Error en SAP: " + error.message)
            return None
        finally:
            self.close_connection()

    def extract_axis_data(self, axis_data):
        """Extrae información de las columnas (metadatos) de los datos del eje.

        Args:
            axis_data (list): Lista de diccionarios que representa los datos de los ejes de la respuesta de SAP.

        Returns:
            pandas.DataFrame: DataFrame con la información de las columnas como CHANM y sus etiquetas CAPTION.
        """
        column_info = []
        # Iterar a través de todos los datos de los ejes
        for data in axis_data:
            for set_item in data["SET"]:
                # Agregar solo si el item es nuevo
                if not any(d["CHANM"] == set_item["CHANM"] for d in column_info):
                    column_info.append(
                        {"CHANM": set_item["CHANM"], "CAPTION": set_item["CAPTION"]}
                    )

        return pd.DataFrame(column_info)

    def extract_axis_info(self, axis_data):
        """
        Extrae y muestra información detallada sobre cada eje para ayudar a comprender la estructura del cubo.

        Args:
            axis_data (list): Lista de diccionarios que contienen información sobre los ejes.

        Returns:
            pd.DataFrame: Un DataFrame que contiene detalles sobre cada eje y sus características.
        """
        # Inicialización de la lista para almacenar la información de los ejes
        axis_info = []
        # Iteración a través de cada eje en los datos proporcionados
        for axis in axis_data:
            # Iteración a través de cada característica del eje
            for char in axis.get("CHARS", []):
                axis_info.append(
                    {
                        "AXIS": axis["AXIS"],
                        "CHANM": char["CHANM"],
                        "CAPTION": char["CAPTION"],
                        "CHATYP": char["CHATYP"],
                        "DETAILS": f"Presentaciones: {char['CHAPRSNT']}, Atributos: {len(char.get('ATTRINM', []))}",
                    }
                )
        # Creación de un DataFrame con la información recopilada
        return pd.DataFrame(axis_info)

    def clean_data(self, axis_data, cell_data):
        """
        Transforma los datos brutos de ejes y celdas del cubo SAP en un DataFrame estructurado.

        Args:
            axis_data (list): Lista que contiene detalles de los ejes (Columnas).
            cell_data (list): Lista que contiene los valores de las celdas relacionados con los ejes.

        Returns:
            pd.DataFrame: Un DataFrame estructurado que combina tanto los datos de los ejes como de las celdas.
        """
        # Extracción de detalles de los ejes
        data = []
        for entry in axis_data:
            if entry["AXIS"] == "001":  # ejemplo, ajustar basado en el caso de uso real
                for item in entry["SET"]:
                    data.append(
                        {
                            "TUPLE_ORDINAL": item["TUPLE_ORDINAL"],
                            "CHANM": item["CHANM"],
                            "CAPTION": item["CAPTION"],
                            "CHAVL": item["CHAVL"],
                            "MONTH": item.get("CHAVL_EXT", ""),  # campo de ejemplo
                        }
                    )

        # Creación de DataFrame a partir de los datos de los ejes
        df_data = pd.DataFrame(data)

        # Creación de DataFrame a partir de los datos de las celdas
        # df_cells = pd.DataFrame(cell_data)
        # df_cells = df_cells.rename(columns={'CELL_ORDINAL': 'TUPLE_ORDINAL'})

        # Fusión de los DataFrames en 'TUPLE_ORDINAL'
        # merged_df = pd.merge(df_data, df_cells, on='TUPLE_ORDINAL', how='left')

        return df_data
        # return merged_df #KEVIN

    def data_structuring(self, df, axis_info=None, values=["CAPTION"]):
        """
        Organiza los datos en un formato estructurado, transformando filas repetidas en columnas.

        Args:
            df (pd.DataFrame): DataFrame que contiene los datos a organizar.
            axis_info (pd.DataFrame): DataFrame opcional que contiene información sobre los ejes para identificar las columnas dinámicamente.
            values (list): Lista con los nombres de las columnas que desea obtener del df

        Returns:
            pd.DataFrame: DataFrame organizado con filas repetidas transformadas en columnas.
        """
        if axis_info is not None:
            # Usamos la información del eje para identificar columnas clave
            key_columns = axis_info[axis_info["CHATYP"] == "1"]["CHANM"].tolist()
        else:
            # Definición estática de columnas clave si no se proporciona axis_info
            key_columns = ["0MATERIAL__ZCH_MARCA", "0MATERIAL", "0CALMONTH2"]

        # Filtrar el DataFrame original para mantener solo las columnas clave y sus valores
        filtered_df = df[df["CHANM"].isin(key_columns)]

        # Usar pivot_table para manejar múltiples valores de 'values'
        pivot_df = filtered_df.pivot_table(
            index="TUPLE_ORDINAL", columns="CHANM", values=values, aggfunc="last"
        ).reset_index()

        # Aplanar las columnas Multindex resultantes
        pivot_df.columns = [" ".join(col).strip() for col in pivot_df.columns.values]

        # Construir diccionario de renombrado si axis_info está disponible
        if axis_info is not None:
            rename_dict = {}
            for _, row in axis_info.iterrows():
                if row["CHANM"] in key_columns:
                    for suffix in values:
                        old_col_name = f"{suffix} {row['CHANM']}"
                        new_col_name = f"{row['CAPTION']}-{suffix}"
                        rename_dict[old_col_name] = new_col_name
            pivot_df = pivot_df.rename(columns=rename_dict)

        return pivot_df

    def extract_all_data(
        self, column_names: List[str], query_name, view_id, params
    ) -> pd.DataFrame:

        self.open_connection()
        raw_data = self.execute_query(query_name, view_id, params)

        # Obtenemos diccionario con los nombres originales de las columnas
        axis_info = self.extract_axis_info(raw_data["E_AXIS_INFO"])
        # Obtenemos información combinada y transformada
        data_clean = self.clean_data(raw_data["E_AXIS_DATA"], raw_data["E_CELL_DATA"])
        # Estructuramos columnas y filas para un mejor entendimiento y visualización
        df_axis_values = self.data_structuring(
            data_clean, axis_info, ["CAPTION", "CHAVL"]
        )  # ,'VALUE']) #kevin

        # Extraer los datos de las celdas del cubo y organizarlos en un DataFrame
        cell_records = [
            {"CELL_ORDINAL": record["CELL_ORDINAL"], "VALUE": record["VALUE"]}
            for record in raw_data["E_CELL_DATA"]
        ]
        df_cell = pd.DataFrame(cell_records)

        df_cell["Group"] = df_cell.index // (len(column_names))

        # Generar el DataFrame con las columnas ordenadas de acuerdo a `column_names`
        df_cell_values = pd.DataFrame(
            {
                name: df_cell.groupby("Group")["VALUE"].nth(i).values
                for i, name in enumerate(column_names)
            }
        )

        df_combined = pd.concat([df_axis_values, df_cell_values], axis=1)

        return df_combined

    def data_structuring(self, df, axis_info=None, values=["CAPTION"]):
        """
        Organiza los datos en un formato estructurado, transformando filas repetidas en columnas.

        Args:
            df (pd.DataFrame): DataFrame que contiene los datos a organizar.
            axis_info (pd.DataFrame): DataFrame opcional que contiene información sobre los ejes para identificar las columnas dinámicamente.
            values (list): Lista con los nombres de las columnas que desea obtener del df

        Returns:
            pd.DataFrame: DataFrame organizado con filas repetidas transformadas en columnas.
        """
        if axis_info is not None:
            # Usamos la información del eje para identificar columnas clave
            key_columns = axis_info[axis_info["CHATYP"] == "1"]["CHANM"].tolist()
        else:
            # Definición estática de columnas clave si no se proporciona axis_info
            key_columns = ["0MATERIAL__ZCH_MARCA", "0MATERIAL", "0CALMONTH2"]

        # Filtrar el DataFrame original para mantener solo las columnas clave y sus valores
        filtered_df = df[df["CHANM"].isin(key_columns)]

        # Usar pivot_table para manejar múltiples valores de 'values'
        pivot_df = filtered_df.pivot_table(
            index="TUPLE_ORDINAL", columns="CHANM", values=values, aggfunc="last"
        ).reset_index()

        # Aplanar las columnas Multindex resultantes
        pivot_df.columns = [" ".join(col).strip() for col in pivot_df.columns.values]

        # Construir diccionario de renombrado si axis_info está disponible
        if axis_info is not None:
            rename_dict = {}
            for _, row in axis_info.iterrows():
                if row["CHANM"] in key_columns:
                    for suffix in values:
                        old_col_name = f"{suffix} {row['CHANM']}"
                        new_col_name = f"{row['CAPTION']}-{suffix}"
                        rename_dict[old_col_name] = new_col_name
            pivot_df = pivot_df.rename(columns=rename_dict)

        return pivot_df

    def extract_all_data(
        self, column_names: List[str], query_name, view_id, params
    ) -> pd.DataFrame:

        self.open_connection()
        raw_data = self.execute_query(query_name, view_id, params)

        # Obtenemos diccionario con los nombres originales de las columnas
        axis_info = self.extract_axis_info(raw_data["E_AXIS_INFO"])
        # Obtenemos información combinada y transformada
        data_clean = self.clean_data(raw_data["E_AXIS_DATA"], raw_data["E_CELL_DATA"])
        # Estructuramos columnas y filas para un mejor entendimiento y visualización
        df_axis_values = self.data_structuring(
            data_clean, axis_info, ["CAPTION", "CHAVL"]
        )  # ,'VALUE']) #kevin

        # Extraer los datos de las celdas del cubo y organizarlos en un DataFrame
        cell_records = [
            {"CELL_ORDINAL": record["CELL_ORDINAL"], "VALUE": record["VALUE"]}
            for record in raw_data["E_CELL_DATA"]
        ]
        df_cell = pd.DataFrame(cell_records)

        df_cell["Group"] = df_cell.index // (len(column_names))

        # Generar el DataFrame con las columnas ordenadas de acuerdo a `column_names`
        df_cell_values = pd.DataFrame(
            {
                name: df_cell.groupby("Group")["VALUE"].nth(i).values
                for i, name in enumerate(column_names)
            }
        )

        df_combined = pd.concat([df_axis_values, df_cell_values], axis=1)

        return df_combined


# ----------- FUNCION PARA EXTRAER Y CONVERTIR LA VISTA EN UN DATAFRAME  --------- #


def get_sap_risk_data(month: str = datetime.now().strftime("%m.%Y")) -> pd.DataFrame:
    """
    Extrae datos de riesgo desde SAP:
    - Conecta a SAP BIP
    - Ejecuta query ZICM_CM03_Q001
    - Procesa datos del cubo
    - Retorna DataFrame con métricas de riesgo

    Args:
        month (str): Mes en formato MM.YYYY

    Returns:
        pd.DataFrame: Datos combinados de ejes y métricas
    """
    sap_conn = SAPConnection(
        ashost=os.getenv("ASHOST"),
        sysnr=os.getenv("SYSNR"),
        client=os.getenv("CLIENT"),
        user=os.getenv("USER_SAP"),
        passwd=os.getenv("PASSWORD_SAP"),
        lang="ES",
    )

    params = [
        ("VAR_ID_6", "0I_CMNTH                      0004"),
        ("VAR_VALUE_LOW_EXT_6", month),
        ("VAR_VALUE_HIGH_EXT_6", month),
    ]

    result = sap_conn.execute_query("ZICM_CM03_Q001", "Z_BASE_RIESGO", params)

    axis_info = sap_conn.extract_axis_info(result["E_AXIS_INFO"])
    data_clean = sap_conn.clean_data(result["E_AXIS_DATA"], result["E_CELL_DATA"])
    df_axis_values = sap_conn.data_structuring(
        data_clean, axis_info, ["CAPTION", "CHAVL"]
    )

    column_names = [
        "Costo Unitario Real",
        "Inventario Disponibl",
        "Inventario No Dispon",
        "Valor Obsoleto",
        "Valor Bloqueado MM",
        "Valor Total MM",
        "Permanencia",
    ]

    cell_records = [
        {"CELL_ORDINAL": record["CELL_ORDINAL"], "VALUE": record["VALUE"]}
        for record in result["E_CELL_DATA"]
    ]
    df_cell = pd.DataFrame(cell_records)
    df_cell["Group"] = df_cell.index // (len(column_names))

    df_cell_values = pd.DataFrame(
        {
            name: df_cell.groupby("Group")["VALUE"].nth(i).values
            for i, name in enumerate(column_names)
        }
    )

    df_combined = pd.concat([df_axis_values, df_cell_values], axis=1)

    return df_combined


# ----------- FUNCION PARA LIMPIAR EL DATAFRAME  --------- #


def clean_risk_data(df_combined: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y transforma el DataFrame obtenido de SAP para el análisis de riesgo.

    Realiza las siguientes operaciones:
    - Elimina columnas innecesarias
    - Elimina sufijos de los nombres de columnas
    - Convierte texto a mayúsculas
    - Convierte columnas numéricas y de fechas al formato correcto

    Args:
        df_combined (pd.DataFrame): DataFrame obtenido de la función get_sap_risk_data

    Returns:
        pd.DataFrame: DataFrame limpio y transformado
    """

    df_combined = df_combined.drop(
        columns=[
            "TUPLE_ORDINAL",
            "Lote-CAPTION",
            "Fecha entrada-CAPTION",
            "Centro-CAPTION",
            "Unidad medida-CAPTION",
            "Codigo Almacen Cliente-CAPTION",
            "Rango Cobertura-CAPTION",
            "Creado el-CAPTION",
            "Fecha Bloqueado-CAPTION",
            "Fecha Obsoleto-CAPTION",
            "Fech. Fabricación-CAPTION",
            "Rango de Permanencia-CAPTION",
            "Rango Bloqueado-CAPTION",
            "Rango Vencidos-CAPTION",
            "Rango Obsoleto-CAPTION",
            "Rango Próximos a Ven-CAPTION",
            "Rango Próx.Vencer MM-CAPTION",
            "Fech, Caducidad/Fech Pref. Consumo-CAPTION",
            "Año natural/Mes-CHAVL",
            "Indicador Stock Espec.-CHAVL",
            "Marca de QM-CHAVL",
            "Tipo Material Inventario-CHAVL",
            "Negocio Inventarios-CHAVL",
            "Tipo de Material (I)-CHAVL",
            "Núm.stock.esp.-CHAVL",
        ]
    )

    # Eliminar los sufijos '-CHAVL' y '-CAPTION' de los nombres de las columnas
    df_combined.columns = df_combined.columns.str.replace("-CHAVL", "").str.replace(
        "-CAPTION", ""
    )

    # Convertir todas las columnas a mayúsculas
    df_combined = df_combined.apply(
        lambda x: x.str.upper() if x.dtype == "object" else x
    )
    df_combined.columns = df_combined.columns.str.upper()

    # Convertir columnas numéricas
    columnas_numericas = [
        "COSTO UNITARIO REAL",
        "INVENTARIO DISPONIBL",
        "INVENTARIO NO DISPON",
        "VALOR OBSOLETO",
        "VALOR BLOQUEADO MM",
        "VALOR TOTAL MM",
        "PERMANENCIA",
    ]

    for col in columnas_numericas:
        if col in df_combined.columns:
            df_combined[col] = pd.to_numeric(df_combined[col], errors="coerce")

    # Convertir columnas de fechas
    columnas_fecha = [
        "FECHA ENTRADA",
        "CREADO EL",
        "FECHA BLOQUEADO",
        "FECHA OBSOLETO",
        "FECH. FABRICACIÓN",
        "FECH, CADUCIDAD/FECH PREF. CONSUMO",
    ]

    for col in columnas_fecha:
        if col in df_combined.columns:
            df_combined[col] = pd.to_datetime(
                df_combined[col], errors="coerce"
            ).dt.strftime("%d/%m/%Y")

    return df_combined


# ----------- FUNCION PARA EXPORTAR EL DATAFRAME A EXCEL  --------- #


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
        filename = f"Analisis_Base_Riesgo_{current_date}.xlsx"

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
