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
