import pandas as pd
import numpy as np
from typing import Dict, Any


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


def insert_segments() -> Dict[str, str]:
    """
    Retorna un diccionario con el mapeo de marcas QM a segmentaciones.
    """
    # TODO: Implementar el diccionario de segmentaciones según la lógica de negocio
    return {
        "OTROS CLIENTES DO": "DEMAND OWNERS",
        "MARKETING PERSONAL": "DEMAND OWNERS",
        "OMNILIFE": "DEMAND OWNERS",
        "JERONIMO MARTINS": "DEMAND OWNERS",
        "LEONISA": "DEMAND OWNERS",
        "LOCATEL": "DEMAND OWNERS",
        "NOVAVENTA": "DEMAND OWNERS",
        "EL ÉXITO": "DEMAND OWNERS",
        "MILAGROS ENTERPRISE": "DEMAND OWNERS",
        "LA POPULAR": "DEMAND OWNERS",
        "D1": "DEMAND OWNERS",
        "USA": "DEMAND OWNERS",
        "USA": "DEMAND OWNERS",
        "EL EXITO": "DEMAND OWNERS",
        "NOVAVENTA FPT": "DEMAND OWNERS",
        "MILAGROS": "DEMAND OWNERS",
        "WORMSER": "DEMAND OWNERS",
        "TENDENCIAS AB": "DEMAND OWNERS",
        "LA FABRIL": "DEMAND OWNERS",
        "UNILEVER": "EXP. LOCALES",
        "NATURA": "EXP. LOCALES",
        "BIOTECNIK": "EXP. LOCALES",
        "NIVEA": "EXP. LOCALES",
        "BRITO": "EXP. LOCALES",
        "AVON": "EXP. LOCALES",
        "OTROS EXP. LOCALES": "EXP. LOCALES",
        "ALICORP": "EXP. LOCALES",
        "SOLLA": "EXP. LOCALES",
        "ECAR": "EXP. LOCALES",
        "FISA": "EXP. LOCALES",
        "KIMBERLY": "EXP. LOCALES",
        "BELCORP": "EXP. LOCALES",
        "AMWAY": "EXP. LOCALES",
        "PROCTER AND GAMBLE": "EXP. LOCALES",
        "HENKEL": "EXP. LOCALES",
        "DIAL": "EXP. LOCALES",
        "BEIERSDORF": "EXP. LOCALES",
        "OTROS EXP. LOCALES": "EXP. LOCALES",
        "FAMILIA": "EXP. LOCALES",
        "BALANCE": "EXP. LOCALES",
        "MAX FACTOR": "EXP. NO LOCALES",
        "DYCLASS": "EXP. NO LOCALES",
        "WELLA CONSUMO": "EXP. NO LOCALES",
        "BIO OIL": "EXP. NO LOCALES",
        "OGX": "EXP. NO LOCALES",
        "COVER GIRL": "EXP. NO LOCALES",
        "WELLA PROFESSIONAL": "EXP. NO LOCALES",
        "ADIDAS": "EXP. NO LOCALES",
        "ACCESORIOS": "EXP. NO LOCALES",
        "BURTS_BEES": "EXP. NO LOCALES",
        "NOPIKEX": "EXP. NO LOCALES",
        "QVS": "EXP. NO LOCALES",
        "UBU": "EXP. NO LOCALES",
        "ESSENCE": "EXP. NO LOCALES",
        "MORROCCANOIL": "EXP. NO LOCALES",
        "HASK": "EXP. NO LOCALES",
        "HERBAL ESSENCES": "EXP. NO LOCALES",
        "LOVE, BEAUTY AND PLANET": "EXP. NO LOCALES",
        "CATRICE": "EXP. NO LOCALES",
        "NATURAL PARADISE": "EXP. NO LOCALES",
        "OLAY": "EXP. NO LOCALES",
        "MID": "EXP. NO LOCALES",
        "SECRET": "EXP. NO LOCALES",
        "FEBREZE": "EXP. NO LOCALES",
        "TAMPAX": "EXP. NO LOCALES",
        "OFCORSS C.I HERMECO": "EXP. NO LOCALES",
        "CADIVEU": "EXP. NO LOCALES",
        "MAX FACTOR GLOBAL": "EXP. NO LOCALES",
        "SEBASTIAN": "EXP. NO LOCALES",
        "AFFRESH": "EXP. NO LOCALES",
        "COSMETRIX": "EXP. NO LOCALES",
        "INCENTIVOS MAX FACTOR": "EXP. NO LOCALES",
        "OTROS EXP. NO LOCALES": "EXP. NO LOCALES",
        "DAVINES": "EXP. NO LOCALES",
        "P&G": "EXP. NO LOCALES",
        "REVOX": "EXP. NO LOCALES",
        "UTOPICK": "EXP. NO LOCALES",
        "IMPORTADOS PROCTER": "EXP. NO LOCALES",
        "ST. IVES": "EXP. NO LOCALES",
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


def calculate_rango_permanencia(row: pd.Series) -> str:
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
            return "7.MAYOR A 720 DIAS"
    else:
        return rango_permanencia


def calculate_status_cons(row: pd.Series) -> str:
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


def calculate_valor_def(row: pd.Series) -> float:
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


def calculate_rango_obsolescencia(row: pd.Series) -> str:
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

    dias_obsolescencia = (fecha_obsoleto - fecha_entrada).days

    if dias_obsolescencia <= 90:
        return "1.MENOR DE 90 DÍAS"
    elif 90 < dias_obsolescencia <= 180:
        return "2.ENTRE 90 Y 180 DÍAS"
    elif 180 < dias_obsolescencia <= 270:
        return "3.ENTRE 180 Y 270 DÍAS"
    elif 270 < dias_obsolescencia <= 360:
        return "4.ENTRE 270 Y 360 DÍAS"
    elif 360 < dias_obsolescencia <= 540:
        return "5.ENTRE 360 Y 540 DÍAS"
    elif 540 < dias_obsolescencia <= 720:
        return "6.ENTRE 540 Y 720 DÍAS"
    else:
        return "7.MAYOR DE 720 DÍAS"


def calculate_rango_vencido(row: pd.Series) -> str:
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

    dias_vencido = (fecha_caducidad - fecha_entrada).days

    if dias_vencido <= 90:
        return "1.MENOR DE 90 DÍAS"
    elif 90 < dias_vencido <= 180:
        return "2.ENTRE 90 Y 180 DÍAS"
    elif 180 < dias_vencido <= 270:
        return "3.ENTRE 180 Y 270 DÍAS"
    elif 270 < dias_vencido <= 360:
        return "4.ENTRE 270 Y 360 DÍAS"
    elif 360 < dias_vencido <= 540:
        return "5.ENTRE 360 Y 540 DÍAS"
    elif 540 < dias_vencido <= 720:
        return "6.ENTRE 540 Y 720 DÍAS"
    else:
        return "7.MAYOR DE 720 DÍAS"


def calculate_rango_bloqueado(row: pd.Series) -> str:
    """
    Calcula el rango de bloqueo basado en las fechas de entrada y bloqueo.

    Args:
        row: Fila del DataFrame con las columnas necesarias

    Returns:
        str: Rango de bloqueo calculado
    """
    status_cons = row.get("STATUS CONS")
    fecha_entrada = row.get("FECHA ENTRADA")
    fecha_bloqueado = row.get("FECHA BLOQUEADO")

    if status_cons != "BLOQUEADO" or pd.isna(fecha_entrada) or pd.isna(fecha_bloqueado):
        return "FALSO"

    dias_vencido = (fecha_bloqueado - fecha_entrada).days

    if dias_vencido <= 90:
        return "1.MENOR DE 90 DÍAS"
    elif 90 < dias_vencido <= 180:
        return "2.ENTRE 90 Y 180 DÍAS"
    elif 180 < dias_vencido <= 270:
        return "3.ENTRE 180 Y 270 DÍAS"
    elif 270 < dias_vencido <= 360:
        return "4.ENTRE 270 Y 360 DÍAS"
    elif 360 < dias_vencido <= 540:
        return "5.ENTRE 360 Y 540 DÍAS"
    elif 540 < dias_vencido <= 720:
        return "6.ENTRE 540 Y 720 DÍAS"
    else:
        return "7.MAYOR DE 720 DÍAS"


def calculate_rango_cons(row: pd.Series) -> str:
    """
    Calcula el rango de consumo final basado en el status y los rangos correspondientes.

    Args:
        row: Fila del DataFrame con las columnas necesarias

    Returns:
        str: Rango de consumo calculado
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


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa el DataFrame aplicando todas las reglas de negocio en el orden específico requerido.

    Args:
        df: DataFrame con los datos de SAP

    Returns:
        pd.DataFrame: DataFrame procesado con todas las columnas calculadas
    """
    # 1. Añadir columnas formuladas de 'MARCA CONCAT' y 'SEGMENTACION'
    df["MARCA CONCAT"] = df["MARCA DE QM"].apply(lambda x: insert_marks().get(x, ""))
    df["SEGMENTACION"] = df["MARCA DE QM"].apply(
        lambda x: insert_segments().get(x, "OTRAS")
    )

    # 2. Calcular 'RANGO DE PERMANENCIA 2'
    required_columns = {"LOTE", "PERMANENCIA", "RANGO DE PERMANENCIA"}
    if required_columns.issubset(df.columns):
        df["RANGO DE PERMANENCIA 2"] = df.apply(calculate_rango_permanencia, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df.columns)}")

    # 3. Calcular 'STATUS CONS'
    required_columns = {"RANGO PRÓX.VENCER MM", "VALOR BLOQUEADO MM", "VALOR OBSOLETO"}
    if required_columns.issubset(df.columns):
        df["STATUS CONS"] = df.apply(calculate_status_cons, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df.columns)}")

    # 4. Calcular 'VALOR DEF'
    required_columns = {"STATUS CONS", "VALOR BLOQUEADO MM", "VALOR TOTAL MM"}
    if required_columns.issubset(df.columns):
        df["VALOR DEF"] = df.apply(calculate_valor_def, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df.columns)}")

    # 5. Reemplazar valores inválidos
    df.replace("#", np.nan, inplace=True)

    # 6. Convertir columnas de fecha
    date_columns = [
        "FECHA ENTRADA",
        "FECHA OBSOLETO",
        "FECHA BLOQUEADO",
        "FECH. FABRICACIÓN",
        "CREADO EL",
        "FECH, CADUCIDAD/FECH PREF. CONSUMO",
    ]

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce")

    # 7. Calcular 'RANGO OBSOLESCENCIA'
    df["RANGO OBSOLESCENCIA"] = df.apply(calculate_rango_obsolescencia, axis=1)

    # 8. Calcular 'RANGO VENCIDO 2'
    df["RANGO VENCIDO 2"] = df.apply(calculate_rango_vencido, axis=1)

    # 9. Calcular 'RANGO BLOQUEADO 2'
    df["RANGO BLOQUEADO 2"] = df.apply(calculate_rango_bloqueado, axis=1)

    # 10. Calcular 'RANGO CONS'
    df["RANGO CONS"] = df.apply(calculate_rango_cons, axis=1)

    return df
