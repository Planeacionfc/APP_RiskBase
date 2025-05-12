import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
import os
from sqlalchemy import create_engine

def insert_marks() -> Dict[str, str]:
    """
    Retorna un diccionario con el mapeo de marcas QM a marcas concatenadas.
    
    Esta función proporciona un mapeo entre las marcas originales de QM y sus equivalentes
    concatenados utilizados en el sistema. Sirve como referencia para estandarizar
    los nombres de las marcas en todo el proceso de análisis de riesgo.
    
    Returns:
        Dict[str, str]: Diccionario donde la clave es el nombre original de la marca QM
                        y el valor es el nombre concatenado o estandarizado.
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
    Retorna un diccionario con el mapeo de marcas QM a subsegmentación.
    
    Esta función proporciona la clasificación de subsegmentación para cada marca QM.
    Las subsegmentaciones posibles incluyen: FULL, RETAILERS, SISTEMA DE VENTAS,
    PROFESIONALES, OTROS, TOLL, y NUDE. Esta clasificación es utilizada en el
    proceso de análisis de riesgo para categorizar las marcas.
    
    Returns:
        Dict[str, str]: Diccionario donde la clave es el nombre de la marca QM
                        y el valor es la categoría de subsegmentación asignada.
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
    
    Esta función proporciona la clasificación de segmentación para cada marca QM.
    Las segmentaciones posibles incluyen: DUEÑOS DE CANAL, EXPERTOS LOCALES,
    EXPERTOS NO LOCALES, MARCAS PROPIAS y NO APLICA. Esta clasificación es
    fundamental para el análisis de riesgo y la toma de decisiones.
    
    Returns:
        Dict[str, str]: Diccionario donde la clave es el nombre de la marca QM
                        y el valor es la categoría de segmentación asignada.
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
    
    Esta función evalúa el tiempo de permanencia de un producto en inventario
    y lo clasifica en rangos predefinidos. Considera casos especiales como lotes
    específicos (222222) y ajusta los rangos según el valor de permanencia en días.
    
    Args:
        row: Fila del DataFrame con las columnas 'LOTE', 'PERMANENCIA' y 'RANGO DE PERMANENCIA'
    
    Returns:
        str: Rango de permanencia calculado, que puede ser uno de los siguientes:
             - '1.MENOR DE 90 DIAS'
             - '5.ENTRE 360 Y 540 DIAS'
             - '6.ENTRE 540 Y 720 DIAS'
             - '7.MAYOR DE 720 DIAS'
             - O el valor original de 'RANGO DE PERMANENCIA' si no aplican las condiciones
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
    
    Esta función determina el estado actual de un producto en inventario evaluando
    su condición de vencimiento, bloqueo y obsolescencia. Sigue una jerarquía de
    prioridad para asignar el estado más crítico cuando múltiples condiciones aplican.
    
    Args:
        row: Fila del DataFrame con las columnas 'RANGO PRÓX.VENCER MM', 'VALOR BLOQUEADO MM'
             y 'VALOR OBSOLETO'
    
    Returns:
        str: Estado calculado que puede ser uno de los siguientes:
             - 'VENCIDO': Producto que ha superado su fecha de caducidad
             - 'BLOQUEADO': Producto bloqueado para su uso o venta
             - 'OBSOLETO': Producto considerado obsoleto
             - 'PAV': Producto próximo a vencer (en los próximos 3 o 6 meses)
             - 'DISPONIBLE': Producto disponible para uso o venta
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
    
    Esta función determina el valor monetario definitivo de un producto en inventario
    según su estado de consumo. Para productos bloqueados, utiliza el valor bloqueado;
    para los demás estados, utiliza el valor total.
    
    Args:
        row: Fila del DataFrame con las columnas 'STATUS CONS', 'VALOR BLOQUEADO MM'
             y 'VALOR TOTAL MM'
    
    Returns:
        float: Valor definitivo calculado en millones de moneda local. Si el producto
               está bloqueado, retorna el valor bloqueado; de lo contrario, retorna
               el valor total.
    """
    status_cons = row.get("STATUS CONS")
    valor_bloqueado = row.get("VALOR BLOQUEADO MM")
    valor_total = row.get("VALOR TOTAL MM")

    return valor_bloqueado if status_cons == "BLOQUEADO" else valor_total


def calculate_rango_obsoleto_column(row: pd.Series) -> str:
    """
    Calcula el rango de obsolescencia basado en las fechas de entrada y obsolescencia.
    
    Esta función determina el tiempo transcurrido desde que un producto fue declarado
    obsoleto y lo clasifica en rangos predefinidos. Solo aplica para productos con
    estado 'OBSOLETO' y con fechas válidas de entrada y obsolescencia.
    
    Args:
        row: Fila del DataFrame con las columnas 'STATUS CONS', 'FECHA ENTRADA'
             y 'FECHA OBSOLETO'
    
    Returns:
        str: Rango de obsolescencia calculado, que puede ser uno de los siguientes:
             - 'FALSO': Si el producto no está obsoleto o faltan fechas
             - '1.MENOR DE 90 DIAS': Si el tiempo de obsolescencia es <= 90 días
             - '2.ENTRE 90 Y 180 DIAS': Si está entre 91 y 180 días
             - '3.ENTRE 180 Y 270 DIAS': Si está entre 181 y 270 días
             - '4.ENTRE 270 Y 360 DIAS': Si está entre 271 y 360 días
             - '5.ENTRE 360 Y 540 DIAS': Si está entre 361 y 540 días
             - '6.ENTRE 540 Y 720 DIAS': Si está entre 541 y 720 días
             - '7.MAYOR DE 720 DIAS': Si es mayor a 720 días
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
    
    Esta función determina el tiempo transcurrido desde que un producto se venció
    y lo clasifica en rangos predefinidos. Solo aplica para productos con estado
    'VENCIDO' y con fechas válidas de entrada y caducidad.
    
    Args:
        row: Fila del DataFrame con las columnas 'STATUS CONS', 'FECHA ENTRADA'
             y 'FECH, CADUCIDAD/FECH PREF. CONSUMO'
    
    Returns:
        str: Rango de vencimiento calculado, que puede ser uno de los siguientes:
             - 'FALSO': Si el producto no está vencido o faltan fechas
             - '1.MENOR DE 90 DIAS': Si el tiempo de vencimiento es <= 90 días
             - '2.ENTRE 90 Y 180 DIAS': Si está entre 91 y 180 días
             - '3.ENTRE 180 Y 270 DIAS': Si está entre 181 y 270 días
             - '4.ENTRE 270 Y 360 DIAS': Si está entre 271 y 360 días
             - '5.ENTRE 360 Y 540 DIAS': Si está entre 361 y 540 días
             - '6.ENTRE 540 Y 720 DIAS': Si está entre 541 y 720 días
             - '7.MAYOR DE 720 DIAS': Si es mayor a 720 días
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
    
    Esta función determina el tiempo transcurrido desde que un producto fue bloqueado
    y lo clasifica en rangos predefinidos. Solo aplica para productos con estado
    'BLOQUEADO' y con fechas válidas de entrada y bloqueo.
    
    Args:
        row: Fila del DataFrame con las columnas 'STATUS CONS', 'FECHA ENTRADA'
             y 'FECHA BLOQUEADO'
    
    Returns:
        str: Rango de bloqueo calculado, que puede ser uno de los siguientes:
             - 'FALSO': Si el producto no está bloqueado o faltan fechas
             - '1.MENOR DE 90 DIAS': Si el tiempo de bloqueo es <= 90 días
             - '2.ENTRE 90 Y 180 DIAS': Si está entre 91 y 180 días
             - '3.ENTRE 180 Y 270 DIAS': Si está entre 181 y 270 días
             - '4.ENTRE 270 Y 360 DIAS': Si está entre 271 y 360 días
             - '5.ENTRE 360 Y 540 DIAS': Si está entre 361 y 540 días
             - '6.ENTRE 540 Y 720 DIAS': Si está entre 541 y 720 días
             - '7.MAYOR A 720 DIAS': Si es mayor a 720 días
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


def calculate_tiempo_bloqueo_column(row: pd.Series) -> int:
    """
    Calcula el tiempo de bloqueo basado en las fechas de entrada y bloqueo.
    
    Esta función calcula la cantidad de días transcurridos desde que un producto
    fue bloqueado hasta su fecha de entrada al sistema. Si alguna de las fechas
    no está disponible, retorna 0.
    
    Args:
        row: Fila del DataFrame con las columnas 'FECHA ENTRADA' y 'FECHA BLOQUEADO'
    
    Returns:
        int: Número de días transcurridos desde el bloqueo del producto. Si alguna
             fecha no está disponible, retorna 0.
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
    
    Esta función determina el rango de consumo final de un producto basándose en su
    estado actual (STATUS CONS) y seleccionando el rango correspondiente según una
    jerarquía predefinida de estados.
    
    Args:
        row: Fila del DataFrame con las columnas 'STATUS CONS', 'RANGO OBSOLESCENCIA',
             'RANGO VENCIDO 2', 'RANGO BLOQUEADO 2' y 'RANGO DE PERMANENCIA 2'
    
    Returns:
        str: Rango de consumo final determinado según el estado del producto:
             - Para productos OBSOLETOS: utiliza 'RANGO OBSOLESCENCIA'
             - Para productos VENCIDOS: utiliza 'RANGO VENCIDO 2'
             - Para productos BLOQUEADOS: utiliza 'RANGO BLOQUEADO 2'
             - Para productos PAV o DISPONIBLES: utiliza 'RANGO DE PERMANENCIA 2'
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
    Calcula el valor de la columna de base riesgo.
    
    Esta función determina el valor monetario que debe considerarse como base para
    el cálculo de riesgo. Si la clasificación de base de riesgo es 'BAJO', el valor
    es 0; de lo contrario, se utiliza el valor definitivo del producto.
    
    Args:
        row: Fila del DataFrame con las columnas 'CLAS BASE RIESGO' y 'VALOR DEF'
    
    Returns:
        float: Valor de base de riesgo calculado. Si la clasificación es 'BAJO',
               retorna 0.0; de lo contrario, retorna el valor definitivo del producto.
    """
    if row["CLAS BASE RIESGO"] == "BAJO":
        return 0.0
    else:
        return row["VALOR DEF"]


def calculate_provision_column(row: pd.Series) -> float:
    """
    Calcula el valor de la columna de provisión.
    
    Esta función determina el monto de provisión que debe asignarse a un producto
    basándose en su marca y factor de provisión. Si la marca es 'OTRAS', no se
    aplica provisión; de lo contrario, se calcula multiplicando el valor definitivo
    por el factor de provisión asignado.
    
    Args:
        row: Fila del DataFrame con las columnas 'MARCA DE QM', 'VALOR DEF' y 'FACTOR PROV'
    
    Returns:
        float: Valor de provisión calculado. Si la marca es 'OTRAS', retorna 0.0;
               de lo contrario, retorna el producto del valor definitivo por el factor
               de provisión.
    """
    if row["MARCA DE QM"] == "OTRAS":
        return 0.0
    else:
        return row["VALOR DEF"] * row['FACTOR PROV']


def calculate_avon_natura_factor_and_class(row: pd.Series, lookup_dict: dict) -> tuple[float, str]:
    """
    Calcula factor provisional y clasificación solo para materiales de AVON y NATURA.
    
    Esta función aplica reglas específicas para determinar el factor de provisión
    y la clasificación de riesgo para los productos de las marcas AVON y NATURA,
    siguiendo una lógica de negocio predefinida basada en múltiples criterios.
    
    Args:
        row: Fila del DataFrame con múltiples columnas necesarias para el cálculo
        lookup_dict: Diccionario de búsqueda con valores predefinidos para factores
                    y clasificaciones según combinaciones específicas de criterios
    
    Returns:
        tuple[float, str]: Una tupla que contiene:
                          - float: Factor de provisión (entre 0.0 y 1.0)
                          - str: Clasificación de riesgo ('BAJO', 'MEDIO', 'MUY ALTO', etc.)
    """
    seg        = row["SEGMENTACION"]
    status     = row["STATUS CONS"]
    tiempo     = row["TIEMPO BLOQUEO"]
    perm       = row["PERMANENCIA"]
    tipo_mat   = row["TIPO DE MATERIAL (I)"]
    negocio    = row["NEGOCIO INVENTARIOS"]
    rango_cons = str(row["RANGO CONS"]).strip()
    indic      = row["INDICADOR STOCK ESPEC."]

    # 1) Segmento interno bloqueado poco tiempo
    if seg in ["MARCAS PROPIAS", "EXPERTOS NO LOCALES", "DUEÑOS DE DEMANDA"] \
       and status == "BLOQUEADO" and tiempo <= 30:
        return 0.0, "BAJO"

    # 2) Disponible o PAV y permanencia <= 30 en granel
    if status in ["DISPONIBLE", "PAV"] \
       and perm <= 30 \
       and tipo_mat in ["GRANEL FAB A TERCERO", "GRANEL"]:
        return 0.0, "BAJO"

    # 3) Negocio FPT → lookup con negocio+status+rango_cons
    if negocio == "FPT":
        key = f"{negocio}{status}{rango_cons}"
        return lookup_dict.get(key, (0.0, "BAJO"))

    # 4) Stock ≠ W y obsoleto/bloqueado/vencido → mismo lookup
    if indic != "W" and status in ["OBSOLETO", "BLOQUEADO", "VENCIDO"]:
        key = f"{negocio}{status}{rango_cons}"
        return lookup_dict.get(key, (0.0, "BAJO"))

    # 5) Stock ≠ W y disponible → lookup con cobertura+permanencia2
    if indic != "W" and status == "DISPONIBLE":
        key = (
            str(row["RANGO COBERTURA"]).strip()
            + str(row["RANGO DE PERMANENCIA 2"]).strip()
        )
        return lookup_dict.get(key, (0.0, "BAJO"))

    # 6) Marca Avon/Natura y estado vencido/obsoleto/PAV → primer dígito
    marca_qm = row["MARCA DE QM"]
    if marca_qm in ["AVON", "NATURA"] and status in ["VENCIDO", "OBSOLETO", "PAV"]:
        try:
            first_digit = int(rango_cons[0])
            return (1.0, "MUY ALTO") if first_digit > 4 else (0.2, "MEDIO")
        except:
            return 0.0, "BAJO"

    # Default
    return 0.0, "BAJO"


def calculate_otros_marcas_factor_and_class(row: pd.Series, lookup_dict: dict) -> tuple[float, str]:
    """
    Calcula factor provisional y clasificación para el resto de marcas (excluyendo Avon/Natura).
    
    Esta función aplica reglas específicas para determinar el factor de provisión
    y la clasificación de riesgo para los productos de marcas diferentes a AVON y NATURA,
    siguiendo una lógica de negocio predefinida basada en múltiples criterios como
    segmentación, estado, tiempo de bloqueo, entre otros.
    
    Args:
        row: Fila del DataFrame con múltiples columnas necesarias para el cálculo
        lookup_dict: Diccionario de búsqueda con valores predefinidos para factores
                    y clasificaciones según combinaciones específicas de criterios
    
    Returns:
        tuple[float, str]: Una tupla que contiene:
                          - float: Factor de provisión (entre 0.0 y 1.0)
                          - str: Clasificación de riesgo ('BAJO', 'MEDIO', 'MUY ALTO', etc.)
    """
    seg         = row["SEGMENTACION"]
    status      = row["STATUS CONS"]
    tiempo      = row["TIEMPO BLOQUEO"]
    indic       = row["INDICADOR STOCK ESPEC."]
    perm        = row["PERMANENCIA"]
    tipo_mat    = row["TIPO DE MATERIAL (I)"]
    rango_cons  = str(row["RANGO CONS"]).strip()
    cobertura   = str(row["RANGO COBERTURA"]).strip()
    subseg      = str(row.get("SUBSEGMENTACION", "")).strip()
    prox_vencer = str(row.get("RANGO PRÓX.VENCER MM", "")).strip()
    negocio     = row["NEGOCIO INVENTARIOS"]

    # 1) Dueños de canal / Marcas propias / Expertos no locales + Bloqueado corto → 0%, BAJO
    if seg in ["DUEÑOS DE CANAL", "MARCAS PROPIAS", "EXPERTOS NO LOCALES"] \
       and status == "BLOQUEADO" \
       and tiempo <= 30:
        return 0.0, "BAJO"

    # 2) Indicador stock = "K" → 0%, BAJO
    if indic == "K":
        return 0.0, "BAJO"

    # 3) Disponible/PAV + Granel y permanencia corta → 0%, BAJO
    if status in ["DISPONIBLE", "PAV"] \
       and tipo_mat in ["GRANEL", "GRANEL FAB A TERCERO"] \
       and perm <= 30:
        return 0.0, "BAJO"

    # 4) Marca "OTRAS" o (Disponible + cobertura "") → 0%, BAJO
    if row["MARCA DE QM"] == "OTRAS" \
       or (status == "DISPONIBLE" and cobertura == ""):
        return 0.0, "BAJO"

    # 5) Stock = "W" → lookup según status
    if indic == "W":
        if status in ["VENCIDO", "PAV"]:
            key = f"{seg}{status}{row['RANGO DE PERMANENCIA 2']}"
        elif status == "DISPONIBLE":
            key = f"{seg}{cobertura}{row['RANGO DE PERMANENCIA 2']}"
        else:
            key = f"{seg}{status}{rango_cons}"
        return lookup_dict.get(key, (0.0, "BAJO"))

    # 6) Stock = "SIN ASIGNAR" u "O"
    if indic in ["SIN ASIGNAR", "O"]:
        # a) PAV + próxima a vencer 3 o 4-6 meses
        if status == "PAV" and prox_vencer in ["1.PAV 3 MESES", "2.PAV 4 A 6 MESES"]:
            key = f"{seg}{subseg}{cobertura}{row['RANGO DE PERMANENCIA 2']}"
            return lookup_dict.get(key, (0.0, "BAJO"))
        # b) Disponible → lookup principal y fallback
        if status == "DISPONIBLE":
            key = f"{seg}{subseg}{cobertura}{row['RANGO DE PERMANENCIA 2']}"
            if key in lookup_dict:
                return lookup_dict[key]
            alt = f"{seg}{subseg}{status} {rango_cons}"
            return lookup_dict.get(alt, (0.0, "BAJO"))
        # c) Obsoleto/Vencido/Bloqueado
        if status in ["OBSOLETO", "VENCIDO", "BLOQUEADO"]:
            key = f"{seg}{subseg}{status} {rango_cons}"
            return lookup_dict.get(key, (0.0, "BAJO"))

    # 7) Fallback por defecto → 0%, BAJO
    return 0.0, "BAJO"


def process_dataframe_avon_natura(df_avon_natura: pd.DataFrame, df_matrices_avon_natura: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa el DataFrame de AVON y NATURA aplicando todas las reglas de negocio en orden.
    
    Esta función realiza el procesamiento completo de los datos de inventario para las
    marcas AVON y NATURA, aplicando secuencialmente todas las transformaciones y cálculos
    necesarios para el análisis de riesgo, incluyendo mapeos, cálculos de rangos,
    estados, valores y provisiones.
    
    Args:
        df_avon_natura: DataFrame con los datos de inventario de AVON y NATURA
        df_matrices_avon_natura: DataFrame con las matrices de referencia para el cálculo
                                de factores de provisión y clasificaciones
    
    Returns:
        pd.DataFrame: DataFrame procesado con todas las columnas calculadas, incluyendo
                     marcas concatenadas, segmentaciones, rangos, estados, valores,
                     factores de provisión, clasificaciones y montos de provisión.
    """
    # 1. Añadir columnas formuladas de 'MARCA CONCAT' y 'SEGMENTACION'
    df_avon_natura["MARCA CONCAT"] = df_avon_natura["MARCA DE QM"].apply(lambda x: insert_marks().get(x, ""))
    df_avon_natura["SEGMENTACION"] = df_avon_natura["MARCA DE QM"].apply(
        lambda x: insert_segments().get(x, "OTRAS")
    )
    df_avon_natura["SUBSEGMENTACION"] = df_avon_natura["MARCA DE QM"].apply(
        lambda x: insert_subsegmentacion().get(x, "")
    )

    # 2. Calcular 'RANGO DE PERMANENCIA 2'
    required_columns = {"LOTE", "PERMANENCIA", "RANGO DE PERMANENCIA"}
    if required_columns.issubset(df_avon_natura.columns):
        df_avon_natura["RANGO DE PERMANENCIA 2"] = df_avon_natura.apply(calculate_rango_permanencia_column, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df_avon_natura.columns)}")

    # 3. Calcular 'STATUS CONS'
    required_columns = {"RANGO PRÓX.VENCER MM", "VALOR BLOQUEADO MM", "VALOR OBSOLETO"}
    if required_columns.issubset(df_avon_natura.columns):
        df_avon_natura["STATUS CONS"] = df_avon_natura.apply(calculate_status_cons_column, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df_avon_natura.columns)}")

    # 4. Calcular 'VALOR DEF'
    required_columns = {"STATUS CONS", "VALOR BLOQUEADO MM", "VALOR TOTAL MM"}
    if required_columns.issubset(df_avon_natura.columns):
        df_avon_natura["VALOR DEF"] = df_avon_natura.apply(calculate_valor_def_column, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df_avon_natura.columns)}")

    # 5. Reemplazar valores inválidos
    df_avon_natura.replace("#", np.nan, inplace=True)

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
        if col in df_avon_natura.columns:
            df_avon_natura[col] = pd.to_datetime(df_avon_natura[col], format="%d/%m/%Y", errors="coerce")

    # 7. Calcular 'RANGO OBSOLESCENCIA'
    df_avon_natura["RANGO OBSOLESCENCIA"] = df_avon_natura.apply(calculate_rango_obsoleto_column, axis=1)

    # 8. Calcular 'RANGO VENCIDO 2'
    df_avon_natura["RANGO VENCIDO 2"] = df_avon_natura.apply(calculate_rango_vencido_column, axis=1)

    # 9. Calcular 'RANGO BLOQUEADO 2'
    df_avon_natura["RANGO BLOQUEADO 2"] = df_avon_natura.apply(calculate_rango_bloqueado_column, axis=1)

    # 10. Calcular 'RANGO CONS'
    df_avon_natura["RANGO CONS"] = df_avon_natura.apply(calculate_rango_cons_column, axis=1)
    
    # 11. Calcular 'TIEMPO BLOQUEO'
    df_avon_natura["TIEMPO BLOQUEO"] = df_avon_natura.apply(calculate_tiempo_bloqueo_column, axis=1)

    # Construir lookup_dict **una vez** antes del apply
    lookup_dict = {
        str(r["concatenado"]).strip(): (r["factor_prov"], r["clasificacion"])
        for _, r in df_matrices_avon_natura.iterrows()
    }

    # Aplicar fila a fila y asignar dos nuevas columnas
    df_avon_natura[["FACTOR PROV", "CLAS BASE RIESGO"]] = df_avon_natura.apply(
        lambda row: pd.Series(calculate_avon_natura_factor_and_class(row, lookup_dict)),
        axis=1
    )

    # 13. BASE RIESGO
    df_avon_natura["BASE RIESGO"] = df_avon_natura.apply(
        calculate_base_riesgo_column, axis=1
    )
    # 14. PROVISION
    df_avon_natura["PROVISION"] = df_avon_natura.apply(
        calculate_provision_column, axis=1
    )

    return df_avon_natura


def process_dataframe_otras_marcas(df_otras_marcas: pd.DataFrame, df_matrices_otros_tipos: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa el DataFrame de otras marcas aplicando todas las reglas de negocio en orden.
    
    Esta función realiza el procesamiento completo de los datos de inventario para marcas
    diferentes a AVON y NATURA, aplicando secuencialmente todas las transformaciones y
    cálculos necesarios para el análisis de riesgo, incluyendo mapeos, cálculos de rangos,
    estados, valores y provisiones.
    
    Args:
        df_otras_marcas: DataFrame con los datos de inventario de marcas diferentes a AVON y NATURA
        df_matrices_otros_tipos: DataFrame con las matrices de referencia para el cálculo
                                de factores de provisión y clasificaciones
    
    Returns:
        pd.DataFrame: DataFrame procesado con todas las columnas calculadas, incluyendo
                     marcas concatenadas, segmentaciones, rangos, estados, valores,
                     factores de provisión, clasificaciones y montos de provisión.
    """
    # 1. Añadir columnas formuladas de 'MARCA CONCAT' y 'SEGMENTACION'
    df_otras_marcas["MARCA CONCAT"] = df_otras_marcas["MARCA DE QM"].apply(lambda x: insert_marks().get(x, ""))
    df_otras_marcas["SEGMENTACION"] = df_otras_marcas["MARCA DE QM"].apply(
        lambda x: insert_segments().get(x, "OTRAS")
    )
    df_otras_marcas["SUBSEGMENTACION"] = df_otras_marcas["MARCA DE QM"].apply(
        lambda x: insert_subsegmentacion().get(x, "")
    )

    # 2. Calcular 'RANGO DE PERMANENCIA 2'
    required_columns = {"LOTE", "PERMANENCIA", "RANGO DE PERMANENCIA"}
    if required_columns.issubset(df_otras_marcas.columns):
        df_otras_marcas["RANGO DE PERMANENCIA 2"] = df_otras_marcas.apply(calculate_rango_permanencia_column, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df_otras_marcas.columns)}")

    # 3. Calcular 'STATUS CONS'
    required_columns = {"RANGO PRÓX.VENCER MM", "VALOR BLOQUEADO MM", "VALOR OBSOLETO"}
    if required_columns.issubset(df_otras_marcas.columns):
        df_otras_marcas["STATUS CONS"] = df_otras_marcas.apply(calculate_status_cons_column, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df_otras_marcas.columns)}")

    # 4. Calcular 'VALOR DEF'
    required_columns = {"STATUS CONS", "VALOR BLOQUEADO MM", "VALOR TOTAL MM"}
    if required_columns.issubset(df_otras_marcas.columns):
        df_otras_marcas["VALOR DEF"] = df_otras_marcas.apply(calculate_valor_def_column, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df_otras_marcas.columns)}")

    # 5. Reemplazar valores inválidos
    df_otras_marcas.replace("#", np.nan, inplace=True)

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
        if col in df_otras_marcas.columns:
            df_otras_marcas[col] = pd.to_datetime(df_otras_marcas[col], format="%d/%m/%Y", errors="coerce")

    # 7. Calcular 'RANGO OBSOLESCENCIA'
    df_otras_marcas["RANGO OBSOLESCENCIA"] = df_otras_marcas.apply(calculate_rango_obsoleto_column, axis=1)

    # 8. Calcular 'RANGO VENCIDO 2'
    df_otras_marcas["RANGO VENCIDO 2"] = df_otras_marcas.apply(calculate_rango_vencido_column, axis=1)

    # 9. Calcular 'RANGO BLOQUEADO 2'
    df_otras_marcas["RANGO BLOQUEADO 2"] = df_otras_marcas.apply(calculate_rango_bloqueado_column, axis=1)

    # 10. Calcular 'RANGO CONS'
    df_otras_marcas["RANGO CONS"] = df_otras_marcas.apply(calculate_rango_cons_column, axis=1)
    
    # 11. Calcular 'TIEMPO BLOQUEO'
    df_otras_marcas["TIEMPO BLOQUEO"] = df_otras_marcas.apply(calculate_tiempo_bloqueo_column, axis=1)

    # Construir lookup_dict **una vez** antes del apply
    lookup_dict = {
        str(r["concatenado"]).strip(): (r["factor_prov"], r["clasificacion"])
        for _, r in df_matrices_otros_tipos.iterrows()
    }

    # Aplicar fila a fila y asignar dos nuevas columnas
    df_otras_marcas[["FACTOR PROV", "CLAS BASE RIESGO"]] = df_otras_marcas.apply(
        lambda row: pd.Series(calculate_otros_marcas_factor_and_class(row, lookup_dict)),
        axis=1
    )

    # 13. Calcular 'BASE RIESGO'
    df_otras_marcas["BASE RIESGO"] = df_otras_marcas.apply(calculate_base_riesgo_column, axis=1)
    
    # 14. Calcular 'PROVISION'
    df_otras_marcas["PROVISION"] = df_otras_marcas.apply(calculate_provision_column, axis=1)
    
    return df_otras_marcas


def combine_final_dataframes(
    df_final_avon_natura: pd.DataFrame,
    df_final_otras_marcas: pd.DataFrame
) -> pd.DataFrame:
    """
    Combina en un único DataFrame los resultados procesados de AVON/NATURA y otras marcas.
    
    Esta función une los DataFrames procesados de AVON/NATURA y otras marcas en un
    único DataFrame consolidado, verificando la compatibilidad de columnas, ordenando
    las columnas según un orden predefinido y manejando posibles duplicados en nombres
    de columnas.
    
    Args:
        df_final_avon_natura: DataFrame procesado con los datos de AVON y NATURA
        df_final_otras_marcas: DataFrame procesado con los datos de otras marcas
    
    Returns:
        pd.DataFrame: DataFrame combinado con todos los registros de ambos DataFrames,
                     con índice reiniciado y columnas ordenadas según el orden predefinido.
                     Si hay columnas duplicadas, se renombran automáticamente.
    
    Raises:
        ValueError: Si los DataFrames no tienen las mismas columnas, lo que indicaría
                  incompatibilidad para la combinación.
    """
    # Verificar que tengan las mismas columnas
    cols1 = list(df_final_avon_natura.columns)
    cols2 = list(df_final_otras_marcas.columns)
    if cols1 != cols2:
        raise ValueError(
            "Los DataFrames no coinciden en sus columnas.\n"
            f"Avon/Natura: {cols1}\n"
            f"Otras marcas: {cols2}"
        )

    # Concatenar uno encima del otro
    df_final_combined = pd.concat([df_final_avon_natura, df_final_otras_marcas], ignore_index=True)
    
    # Columnas en el orden deseado
    columnas_ordenadas = [
        "NEGOCIO INVENTARIOS", "AÑO NATURAL/MES","TIPO MATERIAL INVENTARIO", "MARCA DE QM", "MATERIAL", 
        "DESCRIPCIÓN", "UNIDAD MEDIDA", "CENTRO", "CODIGO ALMACEN CLIENTE", "INDICADOR STOCK ESPEC.",
        "NÚM.STOCK.ESP.", "LOTE", "CREADO EL", "FECH. FABRICACIÓN", "FECH, CADUCIDAD/FECH PREF. CONSUMO",
        "FECHA BLOQUEADO", "FECHA OBSOLETO", "FECHA ENTRADA", "RANGO OBSOLETO 2", "RANGO COBERTURA",
        "RANGO DE PERMANENCIA", "RANGO BLOQUEADO", "RANGO OBSOLETO", "RANGO VENCIDOS", "PRÓXIMO A VENCER",
        "RANGO PRÓX.VENCER MM", "RANGO PRÓXIMOS A VEN", "TIPO DE MATERIAL (I)", "COSTO UNITARIO REAL",
        "INVENTARIO DISPONIBL", "INVENTARIO NO DISPON", "VALOR OBSOLETO", "VALOR BLOQUEADO MM", "VALOR TOTAL MM", "PERMANENCIA",

        "MARCA CONCAT", "SEGMENTACION", "SUBSEGMENTACION",  
        "RANGO DE PERMANENCIA 2",
        "STATUS CONS", "VALOR DEF", "RANGO OBSOLESCENCIA", "RANGO VENCIDO 2",
        "RANGO BLOQUEADO 2", "RANGO CONS", "TIEMPO BLOQUEO", 
        "FACTOR PROV", "CLAS BASE RIESGO", "BASE RIESGO", "PROVISION" 
    ]
    
    # Renombrar columnas duplicadas automáticamente
    nuevos_nombres = []
    conteo = {}
    for col in df_final_combined.columns:
        if col in conteo:
            conteo[col] += 1
            nuevos_nombres.append(f"{col}_{conteo[col]}")
        else:
            conteo[col] = 0
            nuevos_nombres.append(col)
    df_final_combined.columns = nuevos_nombres
    
    df_final_combined = df_final_combined.reindex(columns=columnas_ordenadas)

    return df_final_combined