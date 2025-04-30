from pyrfc._cyrfc import Connection, ABAPApplicationError
import pandas as pd
import numpy as np
from typing import List
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class SAPConnection:
    def __init__(self, ashost, sysnr, client, user, passwd, lang):
        """
        Inicializa la conexión a SAP.
        """
        self.connection_params = {
            'ashost': ashost,
            'sysnr': sysnr,
            'client': client,
            'user': user,
            'passwd': passwd,
            'lang': lang
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
        formatted_parameters += [
        ]

        print("🛠 Sending Parameters to SAP BW:") ##DEBUGGING
        for param in formatted_parameters:
            print(f"{param['NAME']} = {param['VALUE']}")


        try: 
            result = self.connection.call(
                "RRW3_GET_QUERY_VIEW_DATA",
                I_QUERY=query_name,
                I_VIEW_ID=view_id,
                I_T_PARAMETER=formatted_parameters
            )
            print("✅ Query executed successfully!") ##DEBUGGING
            return result
        except ABAPApplicationError as error:
            print("Error en SAP: " + error.message)
            return None
        finally:
            self.close_connection()

    def extract_axis_data(self, axis_data):
        """ Extrae información de las columnas (metadatos) de los datos del eje.
        
        Args:
            axis_data (list): Lista de diccionarios que representa los datos de los ejes de la respuesta de SAP.
        
        Returns:
            pandas.DataFrame: DataFrame con la información de las columnas como CHANM y sus etiquetas CAPTION.
        """
        column_info = []
        # Iterar a través de todos los datos de los ejes
        for data in axis_data:
            for set_item in data['SET']:
                # Agregar solo si el item es nuevo
                if not any(d['CHANM'] == set_item['CHANM'] for d in column_info):
                    column_info.append({
                        'CHANM': set_item['CHANM'],
                        'CAPTION': set_item['CAPTION']
                    })
    
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
            for char in axis.get('CHARS', []):
                axis_info.append({
                    'AXIS': axis['AXIS'],
                    'CHANM': char['CHANM'],
                    'CAPTION': char['CAPTION'],
                    'CHATYP': char['CHATYP'],
                    'DETAILS': f"Presentaciones: {char['CHAPRSNT']}, Atributos: {len(char.get('ATTRINM', []))}"
                })
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
            if entry['AXIS'] == '001':  # ejemplo, ajustar basado en el caso de uso real
                for item in entry['SET']:
                    data.append({
                        'TUPLE_ORDINAL': item['TUPLE_ORDINAL'],
                        'CHANM': item['CHANM'],
                        'CAPTION': item['CAPTION'],
                        'CHAVL': item['CHAVL'],
                        'MONTH': item.get('CHAVL_EXT', '')  # campo de ejemplo
                    })
        
        # Creación de DataFrame a partir de los datos de los ejes
        df_final_data = pd.DataFrame(data)
        
        # Creación de DataFrame a partir de los datos de las celdas
        #df_final_cells = pd.DataFrame(cell_data)
        #df_final_cells = df_final_cells.rename(columns={'CELL_ORDINAL': 'TUPLE_ORDINAL'})
        
        # Fusión de los DataFrames en 'TUPLE_ORDINAL'
        #merged_df_final = pd.merge(df_final_data, df_final_cells, on='TUPLE_ORDINAL', how='left')
        
        return df_final_data
        #return merged_df_final #KEVIN

    def data_structuring(self, df_final, axis_info=None, values=['CAPTION']):
        """
        Organiza los datos en un formato estructurado, transformando filas repetidas en columnas.
        
        Args:
            df_final (pd.DataFrame): DataFrame que contiene los datos a organizar.
            axis_info (pd.DataFrame): DataFrame opcional que contiene información sobre los ejes para identificar las columnas dinámicamente.
            values (list): Lista con los nombres de las columnas que desea obtener del df_final
            
        Returns:
            pd.DataFrame: DataFrame organizado con filas repetidas transformadas en columnas.
        """
        if axis_info is not None:
            # Usamos la información del eje para identificar columnas CLAVE
            key_columns = axis_info[axis_info['CHATYP'] == '1']['CHANM'].tolist()
        
        # Filtrar el DataFrame original para mantener solo las columnas CLAVE y sus valores
        filtered_df_final = df_final[df_final['CHANM'].isin(key_columns)]
        
        # Usar pivot_table para manejar múltiples valores de 'values'
        pivot_df_final = filtered_df_final.pivot_table(index='TUPLE_ORDINAL', columns='CHANM', 
                                        values=values, 
                                        aggfunc='last').reset_index()

        # Aplanar las columnas Multindex resultantes
        pivot_df_final.columns = [' '.join(col).strip() for col in pivot_df_final.columns.values]

        # Construir diccionario de renombrado si axis_info está DISPONIBLE
        if axis_info is not None:
            rename_dict = {}
            for _, row in axis_info.iterrows():
                if row['CHANM'] in key_columns:
                    for suffix in values:
                        old_col_name = f"{suffix} {row['CHANM']}"
                        new_col_name = f"{row['CAPTION']}-{suffix}"
                        rename_dict[old_col_name] = new_col_name
            pivot_df_final = pivot_df_final.rename(columns=rename_dict)

        return pivot_df_final
    
    def extract_all_data(self, column_names: List[str],query_name, view_id, params) -> pd.DataFrame:

        self.open_connection()
        raw_data = self.execute_query(query_name, view_id, params)


        # Obtenemos diccionario con los nombres originales de las columnas
        axis_info = self.extract_axis_info(raw_data['E_AXIS_INFO'])
        # Obtenemos información combinada y transformada
        data_clean = self.clean_data(raw_data['E_AXIS_DATA'], raw_data['E_CELL_DATA'])
        # Estructuramos columnas y filas para un mejor entendimiento y visualización
        df_final_axis_values = self.data_structuring(data_clean, axis_info, ['CAPTION','CHAVL','VALUE']) #kevin
        
        for record in raw_data['E_CELL_DATA']:
            print(record)
        
        # Extraer los datos de las celdas del cubo y organizarlos en un DataFrame
        cell_records = [
            {'CELL_ORDINAL': record['CELL_ORDINAL'], 'VALUE': record['VALUE']}
            for record in raw_data['E_CELL_DATA']
        ]
        df_final_cell = pd.DataFrame(cell_records)

        df_final_cell['Group'] = df_final_cell.index // (len(column_names))

        # Generar el DataFrame con las columnas ordenadas de acuerdo a `column_names`
        df_final_cell_values = pd.DataFrame({
            name: df_final_cell.groupby('Group')['VALUE'].nth(i).values
            for i, name in enumerate(column_names)
        })
        return df_final_cell_values

def get_data_sap():
    """
    Conecta a SAP y obtiene el stock del mes ANTERIOR al mes actual.
    """
    today = datetime.now()
    month = today.strftime("%m.%Y")

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

    # Primero extraemos la informacion de los ejes y los limpiamos
    axis_info = sap_conn.extract_axis_info(result["E_AXIS_INFO"])

    # Limpia los datos de la consulta y la informacion de las celdas
    data_clean = sap_conn.clean_data(result["E_AXIS_DATA"], result["E_CELL_DATA"])

    # Con la informacion de los ejes, estructuramos los datos para que se ajusten a la estructura de un DataFrame
    df_final_axis_values = sap_conn.data_structuring(
        data_clean, axis_info, ["CAPTION", "CHAVL"]
    )

    # Estos son los nombres de las columnas que se van a crear en el DataFrame final
    column_names = ['Costo Unitario Real',
                    'Inventario Disponibl', 
                    'Inventario No Dispon', 
                    'Valor OBSOLETO', 
                    'Valor BLOQUEADO MM', 
                    'Valor Total MM', 
                    'Permanencia'
                ]

    # Con la informacion de las celdas, creamos un diccionario que contiene los valores de cada celda
    cell_records = [
        {'CELL_ORDINAL': record['CELL_ORDINAL'], 'VALUE': record['VALUE']}
        for record in result['E_CELL_DATA']
    ]

    # Con el diccionario, creamos un DataFrame que contiene los valores de las celdas
    df_final_cell = pd.DataFrame(cell_records)

    # Agregamos una columna 'Group' que indica a que grupo pertenece cada celda. Se hace con // (divisin entera)
    df_final_cell['Group'] = df_final_cell.index // (len(column_names))

    # Creamos un nuevo DataFrame que contiene los valores de las celdas agrupados por el grupo
    df_final_cell_values = pd.DataFrame({
        name: df_final_cell.groupby('Group')['VALUE'].nth(i).values
        for i, name in enumerate(column_names)
    })

    # Finalmente, concatenamos los dos DataFrames en uno solo, con la informacion de los ejes y los valores de las celdas
    df_final_combined = pd.concat([df_final_axis_values, df_final_cell_values], axis=1)

    # Renombrar columnas
    df_final_combined = df_final_combined.rename(
        columns={
            'Material-CAPTION': 'Descripción', 
        }
    )

    # Eliminar columnas innecesarias
    df_final_combined = df_final_combined.drop(
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

    # Eliminar sufijos de los nombres de columnas
    df_final_combined.columns = df_final_combined.columns.str.replace("-CHAVL", "").str.replace(
        "-CAPTION", ""
    )

    # Convertir todas las columnas a mayúsculas
    df_final_combined = df_final_combined.apply(
        lambda x: x.str.upper() if x.dtype == "object" else x
    )
    df_final_combined.columns = df_final_combined.columns.str.upper()

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
        if col in df_final_combined.columns:
            df_final_combined[col] = pd.to_numeric(df_final_combined[col], errors="coerce")

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
        if col in df_final_combined.columns:
            df_final_combined[col] = pd.to_datetime(
                df_final_combined[col], errors="coerce"
            ).dt.strftime("%d/%m/%Y")

    df_final_combined = pd.DataFrame(df_final_combined)

    return df_final_combined
