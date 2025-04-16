import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
import os
from sqlalchemy import create_engine

def calculate_rango_bloqueado_column(row: pd.Series) -> str:
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

    Args:
        row: Fila del DataFrame con las columnas necesarias

    Returns:
        str: Tiempo de bloqueo calculado
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
    
    Args:
        df_final_combined (pd.DataFrame): DataFrame con los datos de SAP.
        df_matrices_merge (pd.DataFrame): DataFrame con la información de las matrices, que contiene la 
                                 columna "concatenado", "factor_prov" y "clasificacion".
    
    Returns:
        pd.DataFrame: DataFrame final procesado con todas las columnas calculadas.
    """
    df = df_final_combined.copy()
    
    # 1. Añadir columnas derivadas de 'MARCA DE QM'
    from .data_processing import insert_marks, insert_segments, insert_subsegmentacion
    df["MARCA CONCAT"] = df["MARCA DE QM"].apply(lambda x: insert_marks().get(x, ""))
    df["SEGMENTACION"] = df["MARCA DE QM"].apply(lambda x: insert_segments().get(x, "OTRAS"))
    df["SUBSEGMENTACION"] = df["MARCA DE QM"].apply(lambda x: insert_subsegmentacion().get(x, ""))
    
    # 2. Calcular 'RANGO DE PERMANENCIA 2'
    from .data_processing import calculate_rango_permanencia_column
    required_columns = {"LOTE", "PERMANENCIA", "RANGO DE PERMANENCIA"}
    if required_columns.issubset(df.columns):
        df["RANGO DE PERMANENCIA 2"] = df.apply(calculate_rango_permanencia_column, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df.columns)}")
    
    # 3. Calcular 'STATUS CONS'
    from .data_processing import calculate_status_cons_column
    required_columns = {"RANGO PRÓX.VENCER MM", "VALOR BLOQUEADO MM", "VALOR OBSOLETO"}
    if required_columns.issubset(df.columns):
        df["STATUS CONS"] = df.apply(calculate_status_cons_column, axis=1)
    else:
        print(f"Faltan columnas: {required_columns - set(df.columns)}")
    
    # 4. Calcular 'VALOR DEF'
    from .data_processing import calculate_valor_def_column
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
    from .data_processing import calculate_rango_obsoleto_column
    df["RANGO OBSOLESCENCIA"] = df.apply(calculate_rango_obsoleto_column, axis=1)
    
    # 8. Calcular 'RANGO VENCIDO 2'
    from .data_processing import calculate_rango_vencido_column
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

    # Extraer la parte del df que tiene la clave (suponiendo que 'CLAVE' ya existe en df)
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
    for col in df.columns:
        if col in conteo:
            conteo[col] += 1
            nuevos_nombres.append(f"{col}_{conteo[col]}")
        else:
            conteo[col] = 0
            nuevos_nombres.append(col)
    df.columns = nuevos_nombres

    # Reordenar las columnas
    df = df.reindex(columns=columnas_ordenadas)
    
    return df
