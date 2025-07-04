import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from datetime import datetime
import os
from sqlalchemy import create_engine

#* AQUÍ SE ENCUENTRAN TODAS LAS FUNCIONES DE MAPEO

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
    # TODO: Añadir, eliminar o modificar marcas según la lógica de negocio
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
        "CALA": "CALA",
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
        "KOBA": "KOBA",
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
        "D1": "KOBA",
        "WORMSER": "WORMSER",
        "PROCTER AND GAMBLE": "P&G",
        "DAVINES": "DAVINES",
        "REVOX": "REVOX",
        "CATÁLOGO DE PRODUCTOS": "CATÁLOGO DE PRODUCTOS",
        "ATENEA": "ATENEA",
        "TENDENCIAS AB": "TENDENCIAS AB",
        "LA FABRIL": "LA FABRIL",
        "EDGEWELL": "EDGEWELL",
        "MONTOC": "MONTOC",
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

    # TODO: Añadir, eliminar o modificar subsegmentaciones según la lógica de negocio
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
        "TENDENCIAS AB": "RETAILERS",
        "LA FABRIL": "RETAILERS",
        "EDGEWELL": "FULL",
        "REVOX": "OTROS",
        "ATENEA": "OTROS",
        "MONTOC": "OTROS",
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
    # TODO: Añadir, eliminar o modificar segmentaciones según la lógica de negocio
    return {
        "ACCESORIOS": "EXPERTOS NO LOCALES",
        "ADIDAS": "EXPERTOS NO LOCALES",
        "AGATHA RUIZ DE LA PRADA": "EXPERTOS NO LOCALES",
        "ALICORP": "EXPERTOS LOCALES",
        "AMAZON": "DUEÑOS DE CANAL",
        "AMWAY": "DUEÑOS DE CANAL",
        "ARDEN FOR MEN": "MARCAS PROPIAS",
        "AVON": "EXPERTOS LOCALES",
        "BALANCE": "EXPERTOS LOCALES",
        "BANCO PREBEL": "EXPERTOS LOCALES",
        "BEAUTYHOLICS": "EXPERTOS NO LOCALES",
        "BIO OIL": "EXPERTOS NO LOCALES",
        "BIOTECNIK": "EXPERTOS LOCALES",
        "BURTS_BEES": "EXPERTOS NO LOCALES",
        "CADIVEU": "EXPERTOS NO LOCALES",
        "CALA": "EXPERTOS LOCALES",
        "CATRICE": "EXPERTOS NO LOCALES",
        "CONNECT FOR MEN": "MARCAS PROPIAS",
        "COSMETRIX": "EXPERTOS NO LOCALES",
        "COVER GIRL": "EXPERTOS NO LOCALES",
        "DIAL": "DUEÑOS DE CANAL",
        "DOVE": "EXPERTOS NO LOCALES",
        "DYCLASS": "EXPERTOS LOCALES",
        "ECAR": "EXPERTOS LOCALES",
        "EL EXITO": "DUEÑOS DE CANAL",
        "ELIZABETH ARDEN": "MARCAS PROPIAS",
        "ESSENCE": "EXPERTOS NO LOCALES",
        "FAMILIA": "EXPERTOS LOCALES",
        "FEBREZE": "EXPERTOS NO LOCALES",
        "FISA": "EXPERTOS LOCALES",
        "HASK": "EXPERTOS NO LOCALES",
        "HENKEL": "EXPERTOS LOCALES",
        "HERBAL ESSENCES": "EXPERTOS NO LOCALES",
        "IMPORTADOS PROCTER": "EXPERTOS NO LOCALES",
        "JERONIMO MARTINS": "DUEÑOS DE CANAL",
        "KANABECARE": "EXPERTOS NO LOCALES",
        "KIMBERLY": "EXPERTOS LOCALES",
        "KOBA": "DUEÑOS DE CANAL",
        "L&G ASOCIADOS": "EXPERTOS LOCALES",
        "LA POPULAR": "DUEÑOS DE CANAL",
        "LEONISA": "DUEÑOS DE CANAL",
        "LOCATEL": "DUEÑOS DE CANAL",
        "LOREAL": "EXPERTOS LOCALES",
        "LOVE, BEAUTY AND PLANET": "EXPERTOS NO LOCALES",
        "MAUI": "EXPERTOS NO LOCALES",
        "MAX FACTOR": "EXPERTOS NO LOCALES",
        "MAX FACTOR EXPORTACIÓN": "EXPERTOS NO LOCALES",
        "MAX FACTOR GLOBAL": "EXPERTOS NO LOCALES",
        "MILAGROS": "DUEÑOS DE CANAL",
        "MONCLER": "DUEÑOS DE CANAL",
        "MORROCCANOIL": "EXPERTOS NO LOCALES",
        "NATURA": "EXPERTOS LOCALES",
        "NATURAL PARADISE": "MARCAS PROPIAS",
        "NIVEA": "EXPERTOS LOCALES",
        "NOPIKEX": "EXPERTOS NO LOCALES",
        "NOVAVENTA FPT": "DUEÑOS DE CANAL",
        "NUDE": "MARCAS PROPIAS",
        "OGX": "EXPERTOS NO LOCALES",
        "OLAY": "EXPERTOS NO LOCALES",
        "OMNILIFE": "DUEÑOS DE CANAL",
        "OTRAS": "MARCAS PROPIAS",
        "PREBEL": "MARCAS PROPIAS",
        "PROCTER AND GAMBLE": "EXPERTOS LOCALES",
        "QVS": "EXPERTOS NO LOCALES",
        "SALLY HANSEN": "EXPERTOS NO LOCALES",
        "SIN ASIGNAR": "EXPERTOS LOCALES",
        "SOLLA": "EXPERTOS LOCALES",
        "ST. IVES": "EXPERTOS NO LOCALES",
        "UBU": "EXPERTOS NO LOCALES",
        "UNILEVER": "EXPERTOS LOCALES",
        "VENTA DIRECTA COSMÉTICOS": "EXPERTOS LOCALES",
        "VITÚ": "MARCAS PROPIAS",
        "VITÚ  EXPORTACIÓN": "MARCAS PROPIAS",
        "WELLA CONSUMO": "EXPERTOS NO LOCALES",
        "WELLA PROFESSIONAL": "EXPERTOS NO LOCALES",
        "YARDLEY": "MARCAS PROPIAS",
        "D1": "DUEÑOS DE CANAL",
        "CATÁLOGO DE PRODUCTOS": "DUEÑOS DE CANAL",
        "WORMSER": "DUEÑOS DE CANAL",
        "PROCTER AND GAMBLE": "EXPERTOS LOCALES",
        "DAVINES": "EXPERTOS NO LOCALES",
        "LA FABRIL": "DUEÑOS DE CANAL",
        "TENDENCIAS AB": "DUEÑOS DE CANAL",
        "EDGEWELL": "EXPERTOS LOCALES",
        "REVOX": "EXPERTOS NO LOCALES",
        "ATENEA": "EXPERTOS NO LOCALES",
        "MONTOC": "EXPERTOS NO LOCALES",
    }


#* AQUÍ PUEDES AÑADIR MÁS FUNCIONES DE COLUMNAS FORMULADAS SEGUN LO NECESITE LA LÓGICA DE NEGOCIO

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
        return row["VALOR DEF"] * row["FACTOR PROV"]


#* AQUÍ SE APLICA TODA LA LÓGICA DE NEGOCIO PARA AVON Y NATURA, MODIFICAR SEGÚN CONVENGA

def calculate_avon_natura_factor_and_class(
    row: pd.Series, lookup_dict: dict
) -> tuple[float, str]:
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
    # Si el segmento es marcas propias, expertos no locales o dueños de demanda y el producto está bloqueado poco tiempo, no hay riesgo
    seg = row["SEGMENTACION"]
    status = row["STATUS CONS"]
    tiempo = row["TIEMPO BLOQUEADO"]
    if (
        seg in ["MARCAS PROPIAS", "EXPERTOS NO LOCALES", "DUEÑOS DE DEMANDA"]
        and status == "BLOQUEADO"
        and tiempo <= 30
    ):
        return 0.0, "BAJO"

    # Si el producto es disponible o PAV y su permanencia es <= 30, no hay riesgo
    perm = row["PERMANENCIA"]
    tipo_mat = row["TIPO DE MATERIAL (I)"]
    if (
        status in ["DISPONIBLE", "PAV"]
        and perm <= 30
        and tipo_mat in ["GRANEL FAB A TERCERO", "GRANEL"]
    ):
        return 0.0, "BAJO"

    # Si el negocio es FPT, buscar en el lookup_dict
    negocio = row["NEGOCIO INVENTARIOS"]
    rango_cons = str(row["RANGO CONS"]).strip()
    if negocio == "FPT":
        key = f"{negocio}{status}{rango_cons}"
        return lookup_dict.get(key, (0.0, "BAJO"))

    # Si el stock no es W y el producto es obsoleto/bloqueado/vencido, buscar en el lookup_dict
    indic = row["INDICADOR STOCK ESPEC."]
    if indic != "W" and status in ["OBSOLETO", "BLOQUEADO", "VENCIDO"]:
        key = f"{negocio}{status}{rango_cons}"
        return lookup_dict.get(key, (0.0, "BAJO"))

    # Si el stock no es W y el producto es disponible, buscar en el lookup_dict con cobertura+permanencia2
    if indic != "W" and status == "DISPONIBLE":
        key = (
            str(row["RANGO COBERTURA"]).strip()
            + str(row["RANGO DE PERMANENCIA 2"]).strip()
        )
        return lookup_dict.get(key, (0.0, "BAJO"))

    # Si la marca es Avon/Natura y el estado es vencido/obsoleto/PAV, mirar el primer dígito
    marca_qm = row["MARCA DE QM"]
    if marca_qm in ["AVON", "NATURA"] and status in ["VENCIDO", "OBSOLETO", "PAV"]:
        try:
            first_digit = int(rango_cons[0])
            return (1.0, "MUY ALTO") if first_digit > 4 else (0.2, "MEDIO")
        except:
            return 0.0, "BAJO"

    # Default
    return 0.0, "BAJO"


#* AQUÍ SE APLICA TODA LA LÓGICA DE NEGOCIO PARA EL RESTO DE MARCAS, MODIFICAR SEGÚN CONVENGA

def lookup_dict_by_tipo(
    tipo_busqueda: str, lookup_dict: Dict[str, Tuple[float, str]]
) -> Tuple[float, str]:
    """
    Busca en el lookup_dict la primera fila cuya 'tipo_matriz' coincide con tipo_busqueda.
    El lookup_dict deberá mapear también tipo_matriz → (factor, clasif).
    """
    return lookup_dict.get(tipo_busqueda, (0.0, "BAJO"))


def calculate_otros_marcas_factor_and_class(
    row: pd.Series, df_matrices_otros_tipos: pd.DataFrame
) -> Tuple[float, str]:

    # Extraer campos
    seg = row["SEGMENTACION"].strip()
    subseg = row.get("SUBSEGMENTACION", "").strip()
    status = row["STATUS CONS"].strip()
    tiempo = row["TIEMPO BLOQUEADO"]
    indic = row["INDICADOR STOCK ESPEC."].strip()
    tipo_mat = row["TIPO DE MATERIAL (I)"]
    perm = row["PERMANENCIA"]
    rango_cons = str(row["RANGO CONS"]).strip()
    rango_perm = str(row["RANGO DE PERMANENCIA 2"]).strip()
    cobertura = str(row["RANGO COBERTURA"]).strip()
    prox_vencer = str(row.get("RANGO PRÓX.VENCER MM", "")).strip()

    def safe_get_factor_and_class(mat):
        try:
            return float(mat.iloc[0]["factor_prov"]), mat.iloc[0]["clasificacion"]
        except Exception:
            return 0.0, "BAJO"

    # Si el segmento es Dueños de canal o Marcas propias o Expertos no locales y el producto está bloqueado por poco tiempo, no hay riesgo
    if (
        seg in ["DUEÑOS DE CANAL", "MARCAS PROPIAS", "EXPERTOS NO LOCALES"]
        and status == "BLOQUEADO"
        and tiempo <= 30
    ):
        return 0.0, "BAJO"

    # Si el indicador de stock es "K", no hay riesgo
    if indic == "K":
        return 0.0, "BAJO"

    # Si el producto es disponible o PAV y su permanencia es <= 30 y es granel, no hay riesgo
    if (
        status in ["DISPONIBLE", "PAV"]
        and tipo_mat in ["GRANEL", "GRANEL FAB A TERCERO"]
        and perm <= 30
    ):
        return 0.0, "BAJO"

    # Si el producto es de la marca "OTRAS" o su cobertura es vacía, no hay riesgo
    if row["MARCA DE QM"] == "OTRAS" or (status == "DISPONIBLE" and cobertura == ""):
        return 0.0, "BAJO"

    # Si el indicador de stock es "W", buscar en el lookup_dict con el tipo de matriz específico
    if indic == "W":
        if status in ["VENCIDO", "PAV"]:
            clave = seg + status + rango_perm
            tipo_busqueda = "PVA Y VENCIDOS"
        elif status == "DISPONIBLE":
            clave = seg + cobertura + rango_perm
            tipo_busqueda = "MATRIZ DISPONIBLES VMI"
        else:
            clave = seg + status + rango_cons
            tipo_busqueda = "OBSOLETO"

        mat = df_matrices_otros_tipos.loc[
            (df_matrices_otros_tipos["tipo_matriz"] == tipo_busqueda)
            & (df_matrices_otros_tipos["concatenado"].str.strip() == clave)
        ]

        if not mat.empty:
            return safe_get_factor_and_class(mat)
        return 0.0, "BAJO"

    # Si el indicador de stock es "SIN ASIGNAR" o "O", buscar en el lookup_dict con diferentes combinaciones
    if indic in ["SIN ASIGNAR", "O"]:
        # Si el producto es PAV y su proximidad a vencer es 1.PAV 3 MESES, buscar en el lookup_dict con el tipo de matriz "PVA 1 A 3 MESES"
        if status == "PAV" and prox_vencer == "1.PAV 3 MESES":
            clave = seg + subseg + cobertura + rango_perm
            tipo = "PVA 1 A 3 MESES"
            mat = df_matrices_otros_tipos.loc[
                (df_matrices_otros_tipos["tipo_matriz"] == tipo)
                & (df_matrices_otros_tipos["concatenado"].str.strip() == clave)
            ]
            if not mat.empty:
                return safe_get_factor_and_class(mat)

        # Si el producto es PAV y su proximidad a vencer es 2.PAV 4 A 6 MESES, buscar en el lookup_dict con el tipo de matriz "PVA 4 A 6 MESES"
        if status == "PAV" and prox_vencer == "2.PAV 4 A 6 MESES":
            clave = seg + subseg + cobertura + rango_perm
            tipo = "PVA 4 A 6 MESES"
            mat = df_matrices_otros_tipos.loc[
                (df_matrices_otros_tipos["tipo_matriz"] == tipo)
                & (df_matrices_otros_tipos["concatenado"].str.strip() == clave)
            ]
            if not mat.empty:
                return safe_get_factor_and_class(mat)

        # Si el producto es disponible, buscar en el lookup_dict con el tipo de matriz "DISPONIBLE" y si falla, buscar en el lookup_dict con el tipo de matriz "OBSOLETOS, BLOQUEADOS, VENCIDOS"
        if status == "DISPONIBLE":
            # 1er intento sobre H:L
            clave1 = seg + subseg + cobertura + rango_perm
            mat1 = df_matrices_otros_tipos.loc[
                (df_matrices_otros_tipos["tipo_matriz"] == "DISPONIBLE")
                & (df_matrices_otros_tipos["concatenado"].str.strip() == clave1)
            ]
            if not mat1.empty:
                return safe_get_factor_and_class(mat1)
            # fallback sobre B:F (note el espacio antes de rango_cons)
            clave2 = seg + subseg + status + " " + rango_cons
            mat2 = df_matrices_otros_tipos.loc[
                (
                    df_matrices_otros_tipos["tipo_matriz"]
                    == "OBSOLETOS, BLOQUEADOS, VENCIDOS"
                )
                & (df_matrices_otros_tipos["concatenado"].str.strip() == clave2)
            ]
            if not mat2.empty:
                return safe_get_factor_and_class(mat2)
            return 0.0, "BAJO"

        # Si el producto es obsoleto, vencido o bloqueado, buscar en el lookup_dict con el tipo de matriz "OBSOLETOS, BLOQUEADOS, VENCIDOS"
        if status in ["OBSOLETO", "VENCIDO", "BLOQUEADO"]:
            clave = seg + subseg + status + " " + rango_cons
            mat = df_matrices_otros_tipos.loc[
                (
                    df_matrices_otros_tipos["tipo_matriz"]
                    == "OBSOLETOS, BLOQUEADOS, VENCIDOS"
                )
                & (df_matrices_otros_tipos["concatenado"].str.strip() == clave)
            ]
            if not mat.empty:
                return safe_get_factor_and_class(mat)

    # Si no se cumple ninguna de las condiciones anteriores, no hay riesgo
    return 0.0, "BAJO"


#! PRIMERO REALIZAR PRUEBAS ANTES DE MODIFICAR LA LÓGICA TANTO PARA AVON Y NATURA COMO PARA EL RESTO DE MARCAS


#* AQUÍ SE ENCUENTRAN LAS DOS FUNCIONES PARA EL PROCESAMIENTO DE LOS DATOS DE AVON Y NATURA Y EL RESTO DE MARCAS
#TODO: CADA QUE SE CREA UNA COLUMNA FORMULADA DEBES DE AÑADIRLA A ESTAS FUNCIONES

def process_dataframe_avon_natura(
    df_avon_natura: pd.DataFrame, df_matrices_avon_natura: pd.DataFrame
) -> pd.DataFrame:
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
    df_avon_natura["MARCA CONCAT"] = df_avon_natura["MARCA DE QM"].apply(
        lambda x: insert_marks().get(x, "")
    )
    df_avon_natura["SEGMENTACION"] = df_avon_natura["MARCA DE QM"].apply(
        lambda x: insert_segments().get(x, "OTRAS")
    )
    df_avon_natura["SUBSEGMENTACION"] = df_avon_natura["MARCA DE QM"].apply(
        lambda x: insert_subsegmentacion().get(x, "")
    )

    # 2. Calcular 'RANGO DE PERMANENCIA 2'
    required_columns = {"LOTE", "PERMANENCIA", "RANGO DE PERMANENCIA"}
    if required_columns.issubset(df_avon_natura.columns):
        df_avon_natura["RANGO DE PERMANENCIA 2"] = df_avon_natura.apply(
            calculate_rango_permanencia_column, axis=1
        )
    else:
        print(f"Faltan columnas: {required_columns - set(df_avon_natura.columns)}")

    # 3. Calcular 'STATUS CONS'
    required_columns = {"RANGO PRÓX.VENCER MM", "VALOR BLOQUEADO MM", "VALOR OBSOLETO"}
    if required_columns.issubset(df_avon_natura.columns):
        df_avon_natura["STATUS CONS"] = df_avon_natura.apply(
            calculate_status_cons_column, axis=1
        )
    else:
        print(f"Faltan columnas: {required_columns - set(df_avon_natura.columns)}")

    # 4. Calcular 'VALOR DEF'
    required_columns = {"STATUS CONS", "VALOR BLOQUEADO MM", "VALOR TOTAL MM"}
    if required_columns.issubset(df_avon_natura.columns):
        df_avon_natura["VALOR DEF"] = df_avon_natura.apply(
            calculate_valor_def_column, axis=1
        )
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
            df_avon_natura[col] = pd.to_datetime(
                df_avon_natura[col], format="%d/%m/%Y", errors="coerce"
            )

    # 7. Calcular 'RANGO OBSOLESCENCIA'
    df_avon_natura["RANGO OBSOLESCENCIA"] = df_avon_natura.apply(
        calculate_rango_obsoleto_column, axis=1
    )

    # 8. Calcular 'RANGO VENCIDO 2'
    df_avon_natura["RANGO VENCIDO 2"] = df_avon_natura.apply(
        calculate_rango_vencido_column, axis=1
    )

    # 9. Calcular 'RANGO BLOQUEADO 2'
    df_avon_natura["RANGO BLOQUEADO 2"] = df_avon_natura.apply(
        calculate_rango_bloqueado_column, axis=1
    )

    # 10. Calcular 'RANGO CONS'
    df_avon_natura["RANGO CONS"] = df_avon_natura.apply(
        calculate_rango_cons_column, axis=1
    )

    # 11. Calcular 'TIEMPO BLOQUEO'
    df_avon_natura["TIEMPO BLOQUEADO"] = df_avon_natura.apply(
        calculate_tiempo_bloqueo_column, axis=1
    )

    # Construir lookup_dict **una vez** antes del apply
    lookup_dict = {
        str(r["concatenado"]).strip(): (r["factor_prov"], r["clasificacion"])
        for _, r in df_matrices_avon_natura.iterrows()
    }

    # Aplicar fila a fila y asignar dos nuevas columnas
    df_avon_natura[["FACTOR PROV", "CLAS BASE RIESGO"]] = df_avon_natura.apply(
        lambda row: pd.Series(calculate_avon_natura_factor_and_class(row, lookup_dict)),
        axis=1,
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


def process_dataframe_otras_marcas(
    df_otras_marcas: pd.DataFrame, df_matrices_otros_tipos: pd.DataFrame
) -> pd.DataFrame:
    """
    Procesa el DataFrame aplicando todas las reglas de negocio en el orden específico requerido.

    Args:
        df: DataFrame con los datos de SAP

    Returns:
        pd.DataFrame: DataFrame procesado con todas las columnas calculadas
    """

    # 1. Añadir columnas formuladas de 'MARCA CONCAT' y 'SEGMENTACION'
    df_otras_marcas["MARCA CONCAT"] = df_otras_marcas["MARCA DE QM"].apply(
        lambda x: insert_marks().get(x, "")
    )
    df_otras_marcas["SEGMENTACION"] = df_otras_marcas["MARCA DE QM"].apply(
        lambda x: insert_segments().get(x, "OTRAS")
    )
    df_otras_marcas["SUBSEGMENTACION"] = df_otras_marcas["MARCA DE QM"].apply(
        lambda x: insert_subsegmentacion().get(x, "")
    )

    # 2. Calcular 'RANGO DE PERMANENCIA 2'
    required_columns = {"LOTE", "PERMANENCIA", "RANGO DE PERMANENCIA"}
    if required_columns.issubset(df_otras_marcas.columns):
        df_otras_marcas["RANGO DE PERMANENCIA 2"] = df_otras_marcas.apply(
            calculate_rango_permanencia_column, axis=1
        )
    else:
        print(f"Faltan columnas: {required_columns - set(df_otras_marcas.columns)}")

    # 3. Calcular 'STATUS CONS'
    required_columns = {"RANGO PRÓX.VENCER MM", "VALOR BLOQUEADO MM", "VALOR OBSOLETO"}
    if required_columns.issubset(df_otras_marcas.columns):
        df_otras_marcas["STATUS CONS"] = df_otras_marcas.apply(
            calculate_status_cons_column, axis=1
        )
    else:
        print(f"Faltan columnas: {required_columns - set(df_otras_marcas.columns)}")

    # 4. Calcular 'VALOR DEF'
    required_columns = {"STATUS CONS", "VALOR BLOQUEADO MM", "VALOR TOTAL MM"}
    if required_columns.issubset(df_otras_marcas.columns):
        df_otras_marcas["VALOR DEF"] = df_otras_marcas.apply(
            calculate_valor_def_column, axis=1
        )
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
            df_otras_marcas[col] = pd.to_datetime(
                df_otras_marcas[col], format="%d/%m/%Y", errors="coerce"
            )

    # 7. Calcular 'RANGO OBSOLESCENCIA'
    df_otras_marcas["RANGO OBSOLESCENCIA"] = df_otras_marcas.apply(
        calculate_rango_obsoleto_column, axis=1
    )

    # 8. Calcular 'RANGO VENCIDO 2'
    df_otras_marcas["RANGO VENCIDO 2"] = df_otras_marcas.apply(
        calculate_rango_vencido_column, axis=1
    )

    # 9. Calcular 'RANGO BLOQUEADO 2'
    df_otras_marcas["RANGO BLOQUEADO 2"] = df_otras_marcas.apply(
        calculate_rango_bloqueado_column, axis=1
    )

    # 10. Calcular 'RANGO CONS'
    df_otras_marcas["RANGO CONS"] = df_otras_marcas.apply(
        calculate_rango_cons_column, axis=1
    )

    # 11. Calcular 'TIEMPO BLOQUEO'
    df_otras_marcas["TIEMPO BLOQUEADO"] = df_otras_marcas.apply(
        calculate_tiempo_bloqueo_column, axis=1
    )

    # 12. Aplicar cálculo fila a fila, pasando el DataFrame de matrices:
    df_otras_marcas[["FACTOR PROV", "CLAS BASE RIESGO"]] = df_otras_marcas.apply(
        lambda r: pd.Series(
            calculate_otros_marcas_factor_and_class(r, df_matrices_otros_tipos)
        ),
        axis=1,
    )

    # 13. Calcular 'BASE RIESGO'
    df_otras_marcas["BASE RIESGO"] = df_otras_marcas.apply(
        calculate_base_riesgo_column, axis=1
    )

    # 14. Calcular 'PROVISION'
    df_otras_marcas["PROVISION"] = df_otras_marcas.apply(
        calculate_provision_column, axis=1
    )

    return df_otras_marcas


#* AQUÍ SE ENCUENTRA LA FUNCION PARA UNIR LOS DATAFRAMES

def combine_final_dataframes(
    df_final_avon_natura: pd.DataFrame, df_final_otras_marcas: pd.DataFrame
) -> pd.DataFrame:
    """
    Combina en un único DataFrame los resultados procesados para:
      - Avon/Natura (df_final_avon_natura)
      - Resto de marcas (df_final_otras_marcas)

    Devuelve un nuevo DataFrame con todos los registros y reinicia el índice.
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
    df_final_merge = pd.concat(
        [df_final_avon_natura, df_final_otras_marcas], ignore_index=True
    )

    # Columnas en el orden deseado
    columnas_ordenadas = [
        "NEGOCIO INVENTARIOS",
        "AÑO NATURAL/MES",
        "TIPO MATERIAL INVENTARIO",
        "MARCA DE QM",
        "MATERIAL",
        "DESCRIPCIÓN",
        "UNIDAD MEDIDA",
        "CENTRO",
        "CODIGO ALMACEN CLIENTE",
        "INDICADOR STOCK ESPEC.",
        "NÚM.STOCK.ESP.",
        "LOTE",
        "CREADO EL",
        "FECH. FABRICACIÓN",
        "FECH, CADUCIDAD/FECH PREF. CONSUMO",
        "FECHA BLOQUEADO",
        "FECHA OBSOLETO",
        "FECHA ENTRADA",
        "RANGO OBSOLETO 2",
        "RANGO COBERTURA",
        "RANGO DE PERMANENCIA",
        "RANGO BLOQUEADO",
        "RANGO OBSOLETO",
        "RANGO VENCIDOS",
        "PRÓXIMO A VENCER",
        "RANGO PRÓX.VENCER MM",
        "RANGO PRÓXIMOS A VEN",
        "TIPO DE MATERIAL (I)",
        "COSTO UNITARIO REAL",
        "INVENTARIO DISPONIBL",
        "INVENTARIO NO DISPON",
        "VALOR OBSOLETO",
        "VALOR BLOQUEADO MM",
        "VALOR TOTAL MM",
        "PERMANENCIA",
        "TIEMPO BLOQUEADO",
        "MARCA CONCAT",
        "SEGMENTACION",
        "SUBSEGMENTACION",
        "RANGO DE PERMANENCIA 2",
        "STATUS CONS",
        "VALOR DEF",
        "RANGO OBSOLESCENCIA",
        "RANGO VENCIDO 2",
        "RANGO BLOQUEADO 2",
        "RANGO CONS",
        "FACTOR PROV",
        "CLAS BASE RIESGO",
        "BASE RIESGO",
        "PROVISION",
    ]

    # Renombrar columnas duplicadas automáticamente
    nuevos_nombres = []
    conteo = {}
    for col in df_final_merge.columns:
        if col in conteo:
            conteo[col] += 1
            nuevos_nombres.append(f"{col}_{conteo[col]}")
        else:
            conteo[col] = 0
            nuevos_nombres.append(col)
    df_final_merge.columns = nuevos_nombres

    df_final_merge = df_final_merge.reindex(columns=columnas_ordenadas)

    return df_final_merge
