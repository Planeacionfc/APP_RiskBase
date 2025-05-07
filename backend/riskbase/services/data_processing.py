import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
import os
from sqlalchemy import create_engine

def insert_marks() -> Dict[str, str]:
    """
    Retorna un diccionario con el mapeo de marcas QM a marcas concatenadas.
    """
    # TODO: Implementar el diccionario de marcas según la lógica de negocio
    return {
        "ACCESORIOS": "ACCESORIOS",
        "ADIDAS": "ADIDAS",
        "AGATHA RUIZ DE LA PRADA": "AGATHA RUIZ DE LA PRADA",
        "ALICORP": "ALICORP",
        "AMAZON": "AMAZON",
        "AMWAY": "AMWAY",
        "ARDEN FOR MEN": "AFM/CFM",
        "AVON": "AVON",
        "BALANCE": "BALANCE",
        "BANCO PREBEL": "BANCO PREBEL",
        "BEAUTYHOLICS": "UTOPICK",
        "BIO OIL": "BIO OIL",
        "BIOTECNIK": "BIOTECNIK",
        "BURTS_BEES": "BURT'S BEES",
        "CADIVEU": "CADIVEU",
        "calculateA": "calculateA",
        "CATRICE": "CATRICE",
        "CONNECT FOR MEN": "AFM/CFM",
        "COSMETRIX": "COSMETRIX",
        "COVER GIRL": "COVER GIRL",
        "DIAL": "DIAL",
        "DOVE": "DOVE",
        "DYCLASS": "DYCLASS",
        "ECAR": "ECAR",
        "EL EXITO": "EL EXITO",
        "ELIZABETH ARDEN": "ELIZABETH ARDEN",
        "ESSENCE": "ESSENCE",
        "FAMILIA": "FAMILIA",
        "FEBREZE": "FEBREZE",
        "FISA": "FISA",
        "HASK": "HASK",
        "HENKEL": "HENKEL",
        "HERBAL ESSENCES": "HERBAL ESSENCES",
        "IMPORTADOS PROCTER": "IMPORTADOS PROCTER",
        "JERONIMO MARTINS": "JERONIMO MARTINS",
        "KANABECARE": "KANABECARE",
        "KIMBERLY": "KIMBERLY",
        "KOBA": "D1",
        "L&G ASOCIADOS": "L&G ASOCIADOS",
        "LA POPULAR": "LA POPULAR",
        "LEONISA": "LEONISA",
        "LOCATEL": "LOCATEL",
        "LOREAL": "LOREAL",
        "LOVE, BEAUTY AND PLANET": "LOVE, BEAUTY AND PLANET",
        "MAUI": "MAUI",
        "MAX FACTOR": "MAX FACTOR",
        "MAX FACTOR EXPORTACIÓN": "MAX FACTOR",
        "MAX FACTOR GLOBAL": "MAX FACTOR",
        "MF COL + EXP": "MAX FACTOR",
        "MF GLOBAL": "MAX FACTOR",
        "MILAGROS": "MILAGROS",
        "MONCLER": "MONCLER",
        "MORROCCANOIL": "MORROCCANOIL",
        "NATURA": "NATURA",
        "NATURAL PARADISE": "NATURAL PARADISE",
        "NIVEA": "NIVEA",
        "NOPIKEX": "NOPIKEX",
        "NOVAVENTA FPT": "NOVAVENTA FPT",
        "NUDE": "NUDE",
        "OGX": "OGX",
        "OLAY": "OLAY",
        "OMNILIFE": "OMNILIFE",
        "OTRAS": "OTRAS",
        "PREBEL": "PREBEL",
        "QVS": "ACCESORIOS",
        "SALLY HANSEN": "SALLY HANSEN",
        "SIN ASIGNAR": "SIN ASIGNAR",
        "SOLLA": "SOLLA",
        "ST. IVES": "ST. IVES",
        "UBU": "ACCESORIOS",
        "UNILEVER": "UNILEVER",
        "VENTA DIRECTA COSMÉTICOS": "VENTA DIRECTA COSMÉTICOS",
        "VITÚ": "VITÚ",
        "VITÚ  EXPORTACIÓN": "VITÚ",
        "WELLA CONSUMO": "WELLA CONSUMO",
        "WELLA PROFESSIONAL": "WELLA PROFESSIONAL",
        "YARDLEY": "YARDLEY",
        "CATÁLOGO DE PRODUCTOS": "CATÁLOGO DE PRODUCTOS",
        "D1": "D1",
        "WORMSER": "WORMSER",
        "PROCTER AND GAMBLE": "P&G",
        "DAVINES": "DAVINES",
        "LA FABRIL": "LA FABRIL",
        "REVOX": "REVOX",
        "TENDENCIAS AB": "TENDENCIAS AB",
    }


def insert_subsegmentacion() -> Dict[str, str]:
    """
    RETORNA UN DICCIONARIO CON EL MAPEO DE MARCAS QM A SUBSEGMENTACIÓN.
    """
    return {
        "ACCESORIOS": "OTROS",
        "ADIDAS": "OTROS",
        "AGATHA RUIZ DE LA PRADA": "OTROS",
        "ALICORP": "FULL",
        "AMAZON": "RETAILERS",
        "AMWAY": "SISTEMA DE VENTAS",
        "ARDEN FOR MEN": "OTROS",
        "AVON": "FULL",
        "BALANCE": "FULL",
        "BANCO PREBEL": "FULL",
        "BEAUTYHOLICS": "OTROS",
        "BIO OIL": "OTROS",
        "BIOTECNIK": "FULL",
        "BURTS_BEES": "OTROS",
        "CADIVEU": "PROFESIONALES",
        "CALA": "FULL",
        "CATRICE": "OTROS",
        "CONNECT FOR MEN": "OTROS",
        "COSMETRIX": "OTROS",
        "COVER GIRL": "OTROS",
        "DIAL": "RETAILERS",
        "DOVE": "OTROS",
        "DYCLASS": "SISTEMA DE VENTAS",
        "ECAR": "FULL",
        "EL EXITO": "RETAILERS",
        "ELIZABETH ARDEN": "OTROS",
        "ESSENCE": "OTROS",
        "FAMILIA": "FULL",
        "FEBREZE": "OTROS",
        "FISA": "FULL",
        "HASK": "OTROS",
        "HENKEL": "FULL",
        "HERBAL ESSENCES": "OTROS",
        "IMPORTADOS PROCTER": "OTROS",
        "JERONIMO MARTINS": "RETAILERS",
        "KANABECARE": "OTROS",
        "KIMBERLY": "FULL",
        "KOBA": "RETAILERS",
        "L&G ASOCIADOS": "FULL",
        "LA POPULAR": "RETAILERS",
        "LEONISA": "SISTEMA DE VENTAS",
        "LOCATEL": "RETAILERS",
        "LOREAL": "FULL",
        "LOVE, BEAUTY AND PLANET": "OTROS",
        "MAUI": "OTROS",
        "MAX FACTOR": "OTROS",
        "MAX FACTOR EXPORTACIÓN": "OTROS",
        "MAX FACTOR GLOBAL": "OTROS",
        "MILAGROS": "SISTEMA DE VENTAS",
        "MONCLER": "RETAILERS",
        "MORROCCANOIL": "PROFESIONALES",
        "NATURA": "FULL",
        "NATURAL PARADISE": "OTROS",
        "NIVEA": "FULL",
        "NOPIKEX": "OTROS",
        "NOVAVENTA FPT": "SISTEMA DE VENTAS",
        "NUDE": "NUDE",
        "OGX": "OTROS",
        "OLAY": "OTROS",
        "OMNILIFE": "SISTEMA DE VENTAS",
        "OTRAS": "OTROS",
        "PREBEL": "OTROS",
        "QVS": "OTROS",
        "SALLY HANSEN": "OTROS",
        "SIN ASIGNAR": "FULL",
        "SOLLA": "FULL",
        "ST. IVES": "OTROS",
        "UBU": "OTROS",
        "UNILEVER": "TOLL",
        "VENTA DIRECTA COSMÉTICOS": "FULL",
        "VITÚ": "OTROS",
        "VITÚ  EXPORTACIÓN": "OTROS",
        "WELLA CONSUMO": "OTROS",
        "WELLA PROFESSIONAL": "PROFESIONALES",
        "YARDLEY": "OTROS",
        "D1": "RETAILERS",
        "CATÁLOGO DE PRODUCTOS": "RETAILERS",
        "WORMSER": "RETAILERS",
        "PROCTER AND GAMBLE": "FULL",
        "DAVINES": "OTROS",
        "LA FABRIL": "OTROS",
        "REVOX": "OTROS",
        "TENDENCIAS AB": "RETAILERS"
    }


def insert_segments() -> Dict[str, str]:
    """
    Retorna un diccionario con el mapeo de marcas QM a segmentaciones.
    """
    # TODO: Implementar el diccionario de segmentaciones según la lógica de negocio
    return {
        "OTROS CLIENTES DO": "DUEÑOS DE CANAL",
        "MARKETING PERSONAL": "DUEÑOS DE CANAL",
        "OMNILIFE": "DUEÑOS DE CANAL",
        "JERONIMO MARTINS": "DUEÑOS DE CANAL",
        "LEONISA": "DUEÑOS DE CANAL",
        "LOCATEL": "DUEÑOS DE CANAL",
        "NOVAVENTA": "DUEÑOS DE CANAL",
        "EL ÉXITO": "DUEÑOS DE CANAL",
        "MILAGROS ENTERPRISE": "DUEÑOS DE CANAL",
        "LA POPULAR": "DUEÑOS DE CANAL",
        "D1": "DUEÑOS DE CANAL",
        "USA": "DUEÑOS DE CANAL",
        "USA": "DUEÑOS DE CANAL",
        "EL EXITO": "DUEÑOS DE CANAL",
        "NOVAVENTA FPT": "DUEÑOS DE CANAL",
        "MILAGROS": "DUEÑOS DE CANAL",
        "WORMSER": "DUEÑOS DE CANAL",
        "TENDENCIAS AB": "DUEÑOS DE CANAL",
        "LA FABRIL": "DUEÑOS DE CANAL",
        "UNILEVER": "EXPERTOS LOCALES",
        "NATURA": "EXPERTOS LOCALES",
        "BIOTECNIK": "EXPERTOS LOCALES",
        "NIVEA": "EXPERTOS LOCALES",
        "BRITO": "EXPERTOS LOCALES",
        "AVON": "EXPERTOS LOCALES",
        "OTROS EXPERTOS LOCALES": "EXPERTOS LOCALES",
        "ALICORP": "EXPERTOS LOCALES",
        "SOLLA": "EXPERTOS LOCALES",
        "ECAR": "EXPERTOS LOCALES",
        "FISA": "EXPERTOS LOCALES",
        "KIMBERLY": "EXPERTOS LOCALES",
        "BELCORP": "EXPERTOS LOCALES",
        "AMWAY": "EXPERTOS LOCALES",
        "PROCTER AND GAMBLE": "EXPERTOS LOCALES",
        "HENKEL": "EXPERTOS LOCALES",
        "DIAL": "EXPERTOS LOCALES",
        "BEIERSDORF": "EXPERTOS LOCALES",
        "OTROS EXPERTOS LOCALES": "EXPERTOS LOCALES",
        "FAMILIA": "EXPERTOS LOCALES",
        "BALANCE": "EXPERTOS LOCALES",
        "MAX FACTOR": "EXPERTOS NO LOCALES",
        "DYCLASS": "EXPERTOS NO LOCALES",
        "WELLA CONSUMO": "EXPERTOS NO LOCALES",
        "BIO OIL": "EXPERTOS NO LOCALES",
        "OGX": "EXPERTOS NO LOCALES",
        "COVER GIRL": "EXPERTOS NO LOCALES",
        "WELLA PROFESSIONAL": "EXPERTOS NO LOCALES",
        "ADIDAS": "EXPERTOS NO LOCALES",
        "ACCESORIOS": "EXPERTOS NO LOCALES",
        "BURTS_BEES": "EXPERTOS NO LOCALES",
        "NOPIKEX": "EXPERTOS NO LOCALES",
        "QVS": "EXPERTOS NO LOCALES",
        "UBU": "EXPERTOS NO LOCALES",
        "ESSENCE": "EXPERTOS NO LOCALES",
        "MORROCCANOIL": "EXPERTOS NO LOCALES",
        "HASK": "EXPERTOS NO LOCALES",
        "HERBAL ESSENCES": "EXPERTOS NO LOCALES",
        "LOVE, BEAUTY AND PLANET": "EXPERTOS NO LOCALES",
        "CATRICE": "EXPERTOS NO LOCALES",
        "NATURAL PARADISE": "EXPERTOS NO LOCALES",
        "OLAY": "EXPERTOS NO LOCALES",
        "MID": "EXPERTOS NO LOCALES",
        "SECRET": "EXPERTOS NO LOCALES",
        "FEBREZE": "EXPERTOS NO LOCALES",
        "TAMPAX": "EXPERTOS NO LOCALES",
        "OFCORSS C.I HERMECO": "EXPERTOS NO LOCALES",
        "CADIVEU": "EXPERTOS NO LOCALES",
        "MAX FACTOR GLOBAL": "EXPERTOS NO LOCALES",
        "SEBASTIAN": "EXPERTOS NO LOCALES",
        "AFFRESH": "EXPERTOS NO LOCALES",
        "COSMETRIX": "EXPERTOS NO LOCALES",
        "INCENTIVOS MAX FACTOR": "EXPERTOS NO LOCALES",
        "OTROS EXPERTOS NO LOCALES": "EXPERTOS NO LOCALES",
        "DAVINES": "EXPERTOS NO LOCALES",
        "P&G": "EXPERTOS NO LOCALES",
        "REVOX": "EXPERTOS NO LOCALES",
        "UTOPICK": "EXPERTOS NO LOCALES",
        "IMPORTADOS PROCTER": "EXPERTOS NO LOCALES",
        "ST. IVES": "EXPERTOS NO LOCALES",
        "ARDEN FOR MEN": "MARCAS PROPIAS",
        "NUDE": "MARCAS PROPIAS",
        "ELIZABETH ARDEN": "MARCAS PROPIAS",
        "YARDLEY": "MARCAS PROPIAS",
        "VITÚ": "MARCAS PROPIAS",
        "PREBEL": "MARCAS PROPIAS",
        "OTRAS MP": "MARCAS PROPIAS",
        "AFM/CFM": "MARCAS PROPIAS",
        "BODY CLEAR": "NO APLICA",
        "OTRAS": "NO APLICA",
        "GILLETTE": "NO APLICA",
        "L&G ASOCIADOS": "NO APLICA",
        "CATÁLOGO DE PRODUCTOS": "NO APLICA",
        "HINODE": "NO APLICA",
        "PFIZER": "NO APLICA",
        "CONTEXPORT DISNEY": "NO APLICA",
        "SYSTEM PROFESSIONAL": "NO APLICA",
        "WELONDA": "NO APLICA",
        "SIN ASIGNAR": "NO APLICA",
        "CATÁLOGO DE PRODUCTOS": "NO APLICA",
    }


def calculate_rango_permanencia_column(row: pd.Series) -> str:
    """
    Calcula el rango de permanencia basado en las condiciones especificadas.

    Args:
        row: Fila del DataFrame con las columnas necesarias

    Returns:
        str: Rango de permanencia calculado
    """
    lote = row.get("LOTE", None)
    permanencia = row.get("PERMANENCIA", None)
    rango_permanencia = row.get("RANGO DE PERMANENCIA", None)

    if lote == "222222":
        return "1.MENOR DE 90 DIAS"
    elif permanencia == 0 and rango_permanencia == "5.MAYOR O IGUAL A 360 DIAS":
        return "5.ENTRE 360 Y 540 DIAS"
    elif rango_permanencia == "5.MAYOR O IGUAL A 360 DIAS":
        if permanencia < 540:
            return "5.ENTRE 360 Y 540 DIAS"
        elif permanencia < 720:
            return "6.ENTRE 540 Y 720 DIAS"
        else:
            return "7.MAYOR DE 720 DIAS"
    else:
        return rango_permanencia


def calculate_status_cons_column(row: pd.Series) -> str:
    """
    Calcula el estado de consumo basado en las condiciones de vencimiento, bloqueo y obsolescencia.

    Args:
        row: Fila del DataFrame con las columnas necesarias

    Returns:
        str: Estado calculado (VENCIDO, BLOQUEADO, OBSOLETO, PAV o DISPONIBLE)
    """
    rango_prox_vencer = row.get("RANGO PRÓX.VENCER MM")
    valor_bloqueado = row.get("VALOR BLOQUEADO MM")
    valor_obsoleto = row.get("VALOR OBSOLETO")

    if rango_prox_vencer == "VENCIDO":
        return "VENCIDO"
    elif valor_bloqueado != 0:
        return "BLOQUEADO"
    elif valor_obsoleto != 0:
        return "OBSOLETO"
    elif rango_prox_vencer in ["1.PAV 3 MESES", "2.PAV 4 A 6 MESES"]:
        return "PAV"
    else:
        return "DISPONIBLE"


def calculate_valor_def_column(row: pd.Series) -> float:
    """
    Calcula el valor definitivo basado en el estado de consumo.

    Args:
        row: Fila del DataFrame con las columnas necesarias

    Returns:
        float: Valor definitivo calculado
    """
    status_cons = row.get("STATUS CONS")
    valor_bloqueado = row.get("VALOR BLOQUEADO MM")
    valor_total = row.get("VALOR TOTAL MM")

    return valor_bloqueado if status_cons == "BLOQUEADO" else valor_total


def calculate_rango_obsoleto_column(row: pd.Series) -> str:
    """
    Calcula el rango de obsolescencia basado en las fechas de entrada y obsolescencia.

    Args:
        row: Fila del DataFrame con las columnas necesarias

    Returns:
        str: Rango de obsolescencia calculado
    """
    status_cons = row.get("STATUS CONS")
    fecha_entrada = row.get("FECHA ENTRADA")
    fecha_obsoleto = row.get("FECHA OBSOLETO")

    if status_cons != "OBSOLETO" or pd.isna(fecha_entrada) or pd.isna(fecha_obsoleto):
        return "FALSO"

    dias_obsolescencia = (fecha_entrada - fecha_obsoleto).days

    if dias_obsolescencia <= 90:
        return "1.MENOR DE 90 DIAS"
    elif 90 < dias_obsolescencia <= 180:
        return "2.ENTRE 90 Y 180 DIAS"
    elif 180 < dias_obsolescencia <= 270:
        return "3.ENTRE 180 Y 270 DIAS"
    elif 270 < dias_obsolescencia <= 360:
        return "4.ENTRE 270 Y 360 DIAS"
    elif 360 < dias_obsolescencia <= 540:
        return "5.ENTRE 360 Y 540 DIAS"
    elif 540 < dias_obsolescencia <= 720:
        return "6.ENTRE 540 Y 720 DIAS"
    else:
        return "7.MAYOR DE 720 DIAS"


def calculate_rango_vencido_column(row: pd.Series) -> str:
    """
    Calcula el rango de vencimiento basado en las fechas de entrada y caducidad.

    Args:
        row: Fila del DataFrame con las columnas necesarias

    Returns:
        str: Rango de vencimiento calculado
    """
    status_cons = row.get("STATUS CONS")
    fecha_entrada = row.get("FECHA ENTRADA")
    fecha_caducidad = row.get("FECH, CADUCIDAD/FECH PREF. CONSUMO")

    if status_cons != "VENCIDO" or pd.isna(fecha_entrada) or pd.isna(fecha_caducidad):
        return "FALSO"

    dias_vencido = (fecha_entrada - fecha_caducidad).days

    if dias_vencido <= 90:
        return "1.MENOR DE 90 DIAS"
    elif 90 < dias_vencido <= 180:
        return "2.ENTRE 90 Y 180 DIAS"
    elif 180 < dias_vencido <= 270:
        return "3.ENTRE 180 Y 270 DIAS"
    elif 270 < dias_vencido <= 360:
        return "4.ENTRE 270 Y 360 DIAS"
    elif 360 < dias_vencido <= 540:
        return "5.ENTRE 360 Y 540 DIAS"
    elif 540 < dias_vencido <= 720:
        return "6.ENTRE 540 Y 720 DIAS"
    else:
        return "7.MAYOR DE 720 DIAS"


def calculate_rango_bloqueado_column(row: pd.Series) -> str:
    """
    Calcula el rango de bloqueo basado en las fechas de entrada y bloqueo.
    """
    status_cons = row.get("STATUS CONS")
    fecha_entrada = row.get("FECHA ENTRADA")
    fecha_bloqueado = row.get("FECHA BLOQUEADO")

    if status_cons != "BLOQUEADO" or pd.isna(fecha_entrada) or pd.isna(fecha_bloqueado):
        return "FALSO"

    dias_vencido = (fecha_entrada - fecha_bloqueado).days

    if dias_vencido <= 90:
        return "1.MENOR DE 90 DIAS"
    elif 90 < dias_vencido <= 180:
        return "2.ENTRE 90 Y 180 DIAS"
    elif 180 < dias_vencido <= 270:
        return "3.ENTRE 180 Y 270 DIAS"
    elif 270 < dias_vencido <= 360:
        return "4.ENTRE 270 Y 360 DIAS"
    elif 360 < dias_vencido <= 540:
        return "5.ENTRE 360 Y 540 DIAS"
    elif 540 < dias_vencido <= 720:
        return "6.ENTRE 540 Y 720 DIAS"
    else:
        return "7.MAYOR A 720 DIAS"


def calculate_tiempo_bloqueo_column(row: pd.Series) -> str:
    """
    Calcula el tiempo de bloqueo basado en las fechas de entrada y bloqueo.
    """
    fecha_entrada = row.get("FECHA ENTRADA")
    fecha_bloqueado = row.get("FECHA BLOQUEADO")
    
    if pd.isna(fecha_entrada) or pd.isna(fecha_bloqueado):
        return 0

    tiempo_bloqueado = (fecha_entrada - fecha_bloqueado).days
    
    return tiempo_bloqueado    


def calculate_rango_cons_column(row: pd.Series) -> str:
    """
    Calcula el rango de consumo final basado en el status y los rangos correspondientes.
    """
    status = row.get("STATUS CONS")

    if status == "OBSOLETO":
        return row.get("RANGO OBSOLESCENCIA")
    elif status == "VENCIDO":
        return row.get("RANGO VENCIDO 2")
    elif status == "BLOQUEADO":
        return row.get("RANGO BLOQUEADO 2")
    elif status == "PAV":
        return row.get("RANGO DE PERMANENCIA 2")
    else:
        return row.get("RANGO DE PERMANENCIA 2")


def calculate_base_riesgo_column(row: pd.Series) -> float:
    """
    Calcula el valor de la columna de base riesgo
    """
    if row["CLAS BASE RIESGO"] == "BAJO":
        return 0.0
    else:
        return row["VALOR DEF"]


def calculate_provision_column(row: pd.Series) -> float:
    """
    Calcula el valor de la columna de provisión
    """
    if row["MARCA DE QM"] == "OTRAS":
        return 0.0
    else:
        return row["VALOR DEF"] * row['FACTOR PROV']


def process_dataframe_columns(df_final_combined: pd.DataFrame, df_matrices_merge: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa el DataFrame aplicando todas las reglas de negocio en el orden específico requerido.
    Se utilizan operaciones vectorizadas y merge para asignar 'FACTOR PROV' y 'CLAS BASE RIESGO'
    mediante un sistema de estrategias (Strategy) de modo que se genere una columna auxiliar "CLAVE"
    para las búsquedas en df_matrices_merge, y para las estrategias fijas se asignen directamente los valores.
    La columna "CLAVE" se elimina antes de retornar el DataFrame final.
    """
    df = df_final_combined.copy()
    
    # 1. Añadir columnas derivadas de 'MARCA DE QM'
    df["MARCA CONCAT"] = df["MARCA DE QM"].apply(lambda x: insert_marks().get(x, ""))
    df["SEGMENTACION"] = df["MARCA DE QM"].apply(lambda x: insert_segments().get(x, "OTRAS"))
    df["SUBSEGMENTACION"] = df["MARCA DE QM"].apply(lambda x: insert_subsegmentacion().get(x, ""))
    
    # 2. Calcular 'RANGO DE PERMANENCIA 2'
    required_columns = {"LOTE", "PERMANENCIA", "RANGO DE PERMANENCIA"}
    if required_columns.issubset(df.columns):
        df["RANGO DE PERMANENCIA 2"] = df.apply(calculate_rango_permanencia_column, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df.columns)}")
    
    # 3. Calcular 'STATUS CONS'
    required_columns = {"RANGO PRÓX.VENCER MM", "VALOR BLOQUEADO MM", "VALOR OBSOLETO"}
    if required_columns.issubset(df.columns):
        df["STATUS CONS"] = df.apply(calculate_status_cons_column, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df.columns)}")
    
    # 4. Calcular 'VALOR DEF'
    required_columns = {"STATUS CONS", "VALOR BLOQUEADO MM", "VALOR TOTAL MM"}
    if required_columns.issubset(df.columns):
        df["VALOR DEF"] = df.apply(calculate_valor_def_column, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df.columns)}")
    
    # 5. Reemplazar valores inválidos
    df.replace("#", np.nan, inplace=True)
    
    # 6. Convertir columnas de fecha
    date_columns = [
        "FECHA ENTRADA", "FECHA OBSOLETO", "FECHA BLOQUEADO",
        "FECH. FABRICACIÓN", "CREADO EL", "FECH, CADUCIDAD/FECH PREF. CONSUMO"
    ]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce")
    
    # 7. Calcular 'RANGO OBSOLESCENCIA'
    df["RANGO OBSOLESCENCIA"] = df.apply(calculate_rango_obsoleto_column, axis=1)
    
    # 8. Calcular 'RANGO VENCIDO 2'
    df["RANGO VENCIDO 2"] = df.apply(calculate_rango_vencido_column, axis=1)
    
    # 9. Calcular 'RANGO BLOQUEADO 2'
    df["RANGO BLOQUEADO 2"] = df.apply(calculate_rango_bloqueado_column, axis=1)
    
    # 10. Calcular 'RANGO CONS'
    df["RANGO CONS"] = df.apply(calculate_rango_cons_column, axis=1)
    
    # 11. Calcular 'TIEMPO BLOQUEO'
    df["TIEMPO BLOQUEO"] = df.apply(calculate_tiempo_bloqueo_column, axis=1)
    
    # 12. Calcular 'FACTOR PROV' y 'CLAS BASE RIESGO' usando estrategias vectorizadas con merge
    # Se crea una columna auxiliar "CLAVE" que será asignada sólo para las filas que requieran lookup.
    df["CLAVE"] = np.nan
    df["FACTOR PROV"] = np.nan
    df["CLAS BASE RIESGO"] = np.nan

    df["CLAVE"] = df["CLAVE"].astype(object)
    df["CLAS BASE RIESGO"] = df["CLAS BASE RIESGO"].astype(object)

    # --- Estrategias fijas: se asignan valores directos y se deja "CLAVE" en NaN ---
    # Fija 1: Si SEGMENTACION en ["DUEÑOS DE CANAL", "MARCAS PROPIAS", "EXPERTOS NO LOCALES"] y STATUS CONS=="BLOQUEADO" y TIEMPO BLOQUEO <=30
    condition_fixed1 = (
        df["SEGMENTACION"].str.upper().isin(["DUEÑOS DE CANAL", "MARCAS PROPIAS", "EXPERTOS NO LOCALES"]) &
        (df["STATUS CONS"].str.upper() == "BLOQUEADO") &
        (df["TIEMPO BLOQUEO"] <= 30)
    )

    df.loc[condition_fixed1, "FACTOR PROV"] = 0.0
    df.loc[condition_fixed1, "CLAS BASE RIESGO"] = "BAJO"
    
    # Fija 2: Si STATUS CONS in ["DISPONIBLE", "PAV"] y PERMANENCIA<=30 y TIPO DE MATERIAL (I) in ["GRANEL", "GRANEL FAB A TERCERO"]
    condition_fixed2 = (
        df["STATUS CONS"].isin(["DISPONIBLE", "PAV"]) &
        (df["PERMANENCIA"] <= 30) &
        df["TIPO DE MATERIAL (I)"].isin(["GRANEL", "GRANEL FAB A TERCERO"])
    )
    df.loc[condition_fixed2, "FACTOR PROV"] = 0.0
    df.loc[condition_fixed2, "CLAS BASE RIESGO"] = "BAJO"
    
    # Fija 3: Si INDICADOR STOCK ESPEC. es "K"
    condition_fixed3 = (df["INDICADOR STOCK ESPEC."].str.upper() == "K")
    df.loc[condition_fixed3, "FACTOR PROV"] = 0.0
    df.loc[condition_fixed3, "CLAS BASE RIESGO"] = "BAJO"
    
    # Fija 4: Si MARCA CONCAT in ["AVON", "NATURA"] y STATUS CONS in ["VENCIDO", "OBSOLETO", "PAV"],
    # se evalúa el primer dígito de RANGO CONS; si > 4 → (1.0, "MUY ALTO"), else → (0.2, "MEDIO")
    condition_fixed4 = (
        df["MARCA CONCAT"].str.upper().isin(["AVON", "NATURA"]) &
        df["STATUS CONS"].str.upper().isin(["VENCIDO", "OBSOLETO", "PAV"])
    )

    # Extraemos el primer carácter, convertimos a numérico y en caso de error se asigna NaN
    df.loc[condition_fixed4, "TEMP_DIGIT"] = pd.to_numeric(
        df.loc[condition_fixed4, "RANGO CONS"].astype(str).str.strip().str[0],
        errors="coerce"
    )

    condition_digit = df["TEMP_DIGIT"] > 4

    df.loc[condition_fixed4 & condition_digit, "FACTOR PROV"] = 1.0
    df.loc[condition_fixed4 & condition_digit, "CLAS BASE RIESGO"] = "MUY ALTO"
    df.loc[condition_fixed4 & (~condition_digit), "FACTOR PROV"] = 0.2
    df.loc[condition_fixed4 & (~condition_digit), "CLAS BASE RIESGO"] = "MEDIO"

    # Eliminamos la columna temporal
    df.drop(columns=["TEMP_DIGIT"], inplace=True)
    
    # Fija 5: Si MARCA DE QM is "OTRAS" o (STATUS CONS=="DISPONIBLE" y RANGO COBERTURA es vacío)
    condition_fixed5 = (df["MARCA DE QM"].str.upper() == "OTRAS") | (
        (df["STATUS CONS"].str.upper() == "DISPONIBLE") & (df["RANGO COBERTURA"].str.strip() == "")
    )
    df.loc[condition_fixed5, "FACTOR PROV"] = 0.0
    df.loc[condition_fixed5, "CLAS BASE RIESGO"] = "BAJO"
    
    # --- Estrategias que requieren lookup: se asigna valor a "CLAVE" para las filas que aún no tienen valor fijo ---
    condition_no_fixed = df["FACTOR PROV"].isna()
    
    # Lookup 1: Si NEGOCIO INVENTARIOS is "FPT"
    mask_lookup1 = condition_no_fixed & (df["NEGOCIO INVENTARIOS"].str.upper() == "FPT")
    df.loc[mask_lookup1, "CLAVE"] = (
         df.loc[mask_lookup1, "NEGOCIO INVENTARIOS"].str.strip() +
         df.loc[mask_lookup1, "STATUS CONS"].str.strip() +
         df.loc[mask_lookup1, "RANGO CONS"].astype(str).str.strip()
    )
    
    # Lookup 2: Si INDICADOR STOCK ESPEC. != "W" y STATUS CONS in ["OBSOLETO", "BLOQUEADO", "VENCIDO"]
    mask_lookup2 = condition_no_fixed & (df["INDICADOR STOCK ESPEC."].str.upper() != "W") & (df["STATUS CONS"].isin(["OBSOLETO", "BLOQUEADO", "VENCIDO"]))
    df.loc[mask_lookup2, "CLAVE"] = (
         df.loc[mask_lookup2, "NEGOCIO INVENTARIOS"].str.strip() +
         df.loc[mask_lookup2, "STATUS CONS"].str.strip() +
         df.loc[mask_lookup2, "RANGO CONS"].astype(str).str.strip()
    )
    
    # Lookup 3: Si INDICADOR STOCK ESPEC. == "W" y STATUS CONS in ["VENCIDO", "PAV"]
    mask_lookup3 = condition_no_fixed & (df["INDICADOR STOCK ESPEC."].str.upper() == "W") & (df["STATUS CONS"].isin(["VENCIDO", "PAV"]))
    df.loc[mask_lookup3, "CLAVE"] = (
         df.loc[mask_lookup3, "SEGMENTACION"].str.strip() +
         df.loc[mask_lookup3, "STATUS CONS"].str.strip() +
         df.loc[mask_lookup3, "RANGO DE PERMANENCIA 2"].astype(str).str.strip()
    )
    
    # Lookup 4: Si INDICADOR STOCK ESPEC. == "W" y STATUS CONS == "DISPONIBLE"
    mask_lookup4 = condition_no_fixed & (df["INDICADOR STOCK ESPEC."].str.upper() == "W") & (df["STATUS CONS"].str.upper() == "DISPONIBLE")
    df.loc[mask_lookup4, "CLAVE"] = (
         df.loc[mask_lookup4, "SEGMENTACION"].str.strip() +
         df.loc[mask_lookup4, "RANGO COBERTURA"].str.strip() +
         df.loc[mask_lookup4, "RANGO DE PERMANENCIA 2"].astype(str).str.strip()
    )
    
    # Lookup 5: Si INDICADOR STOCK ESPEC. in ["SIN ASIGNAR", "O"]
    mask_lookup5 = condition_no_fixed & (df["INDICADOR STOCK ESPEC."].str.upper().isin(["SIN ASIGNAR", "O"]))
    # Para STATUS CONS == "PAV" y RANGO PRÓX.VENCER MM in {"1.PAV 3 MESES", "2.PAV 4 A 6 MESES"}
    mask_lookup5_pav = mask_lookup5 & (df["STATUS CONS"].str.upper() == "PAV") & (df["RANGO PRÓX.VENCER MM"].str.upper().isin(["1.PAV 3 MESES", "2.PAV 4 A 6 MESES"]))
    df.loc[mask_lookup5_pav, "CLAVE"] = (
         df.loc[mask_lookup5_pav, "SEGMENTACION"].str.strip() +
         df.loc[mask_lookup5_pav, "SUBSEGMENTACION"].str.strip() +
         df.loc[mask_lookup5_pav, "RANGO COBERTURA"].str.strip() +
         df.loc[mask_lookup5_pav, "RANGO DE PERMANENCIA 2"].astype(str).str.strip()
    )
    # Para STATUS CONS == "DISPONIBLE": se asigna una primera CLAVE
    mask_lookup5_disp = mask_lookup5 & (df["STATUS CONS"].str.upper() == "DISPONIBLE")
    df.loc[mask_lookup5_disp, "CLAVE"] = (
         df.loc[mask_lookup5_disp, "SEGMENTACION"].str.strip() +
         df.loc[mask_lookup5_disp, "SUBSEGMENTACION"].str.strip() +
         df.loc[mask_lookup5_disp, "RANGO COBERTURA"].str.strip() +
         df.loc[mask_lookup5_disp, "RANGO DE PERMANENCIA 2"].astype(str).str.strip()
    )
    # Para STATUS CONS in ["OBSOLETO", "VENCIDO", "BLOQUEADO"]:
    mask_lookup5_alt = mask_lookup5 & (df["STATUS CONS"].isin(["OBSOLETO", "VENCIDO", "BLOQUEADO"]))
    df.loc[mask_lookup5_alt, "CLAVE"] = (
         df.loc[mask_lookup5_alt, "SEGMENTACION"].str.strip() +
         df.loc[mask_lookup5_alt, "SUBSEGMENTACION"].str.strip() +
         df.loc[mask_lookup5_alt, "STATUS CONS"].str.strip() + " " +
         df.loc[mask_lookup5_alt, "RANGO CONS"].astype(str).str.strip()
    )
    
    # --- Realizar el merge para las filas con clave definida ---
    df_matrices_merge["concatenado"] = df_matrices_merge["concatenado"].astype(str).str.strip()

    # Extraer la parte del df que tiene la clave
    df_subset = df.loc[~df["CLAVE"].isna()].copy()
    df_subset.reset_index(inplace=True)  # Guardamos el índice original

    # Realizar el merge usando la columna 'concatenado' original de df_matrices_merge
    merge_result = df_subset.merge(
        df_matrices_merge[["concatenado", "factor_prov", "clasificacion"]],
        left_on="CLAVE",
        right_on="concatenado",
        how="left"
    )
    
    # Asignar los valores del merge a las filas correspondientes usando el índice original
    for _, mrow in merge_result.iterrows():
        orig_idx = mrow["index"]
        df.at[orig_idx, "FACTOR PROV"] = mrow["factor_prov"]
        df.at[orig_idx, "CLAS BASE RIESGO"] = mrow["clasificacion"]
    
    # Para las filas sin CLAVE o sin coincidencia, asignar valores por defecto
    df["FACTOR PROV"] = df["FACTOR PROV"].fillna(0.0)
    df["CLAS BASE RIESGO"] = df["CLAS BASE RIESGO"].fillna("BAJO")
    
    # Eliminar la columna auxiliar "CLAVE"
    df.drop(columns=["CLAVE"], inplace=True)
    
    # 13. Calcular 'BASE RIESGO'
    df["BASE RIESGO"] = df.apply(calculate_base_riesgo_column, axis=1)
    
    # 14. Calcular 'PROVISION'
    df["PROVISION"] = df.apply(calculate_provision_column, axis=1)

    return df
