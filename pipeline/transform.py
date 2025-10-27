import pandas as pd
import numpy as np
from typing import List, Union, Dict
from dropi_logic.utils import *
import datetime

# Se mantiene la función parse_date_smart como está

@handle_pandas_errors
def parse_date_with_formats(date_str: str) -> pd.Timestamp:
    """
    Intenta parsear una cadena de fecha con múltiples formatos SIN try/except.
    El decorador handle_pandas_errors capturará cualquier fallo.
    """
    if pd.isna(date_str) or not date_str:
        return None

    # Intentar formato YYYYMMDD (la forma limpia de probar en cascada)
    try:
        return pd.to_datetime(date_str, format='%Y%m%d', errors='raise')
    except:
        pass
    
    # Intentar formato DDMMYYYY
    try:
        return pd.to_datetime(date_str, format='%d%m%Y', errors='raise')
    except:
        pass
    
    # Intentar inferencia (fallará para cadenas no válidas)
    return pd.to_datetime(date_str, errors='raise') 


@handle_pandas_errors
def clean_dataframe(
    df: pd.DataFrame, 
    date_columns: List[str]
) -> pd.DataFrame:
    """
    Realiza la limpieza de un solo DataFrame con sus columnas de fecha específicas.
    """
    # 1. Limpiar duplicados y crear copia segura
    clean_df = df.drop_duplicates().copy()
    
    # 2. Convertir Nulls/Vacíos/NA a 0 para columnas numéricas
    numeric_cols = clean_df.select_dtypes(include=[np.float64, np.int64]).columns
    for col in numeric_cols:
        clean_df[col] = clean_df[col].fillna(0)
    
    # 3. & 4. Convertir y corregir fechas
    
    #En caso de que no tenga columna de fecha, le añadimos la actual
    # HOTFIX: El cliente quiere recibir esto rapido, por eso la razón de este ajuste.
    if date_columns == []:
        add_date_column(clean_df)
    else:
        for col in date_columns:
            if col in clean_df.columns:
                # Pre-limpieza de la cadena
                clean_df[col] = clean_df[col].astype(str).str.replace(r'[\s\-]', '', regex=True)
                
                # Aplicar la función decorada
                clean_df[col] = clean_df[col].apply(parse_date_with_formats)

    return clean_df


@handle_pandas_errors
def clean_list_of_dataframes(
    list_of_dfs: List[pd.DataFrame], 
    date_columns_map: Dict[int, List[str]]
) -> List[pd.DataFrame]:
    """
    Aplica la limpieza a una lista de DataFrames usando un mapeo de columnas específico.
    """
    clean_dfs = []
    for i, df in enumerate(list_of_dfs):
        # Obtener la lista de columnas de fecha para el DataFrame actual (i)
        cols_to_clean = date_columns_map.get(i, [])
        
        # Aplicar la función de limpieza específica
        clean_df = clean_dataframe(df, cols_to_clean)
        clean_dfs.append(clean_df)
    
    return clean_dfs

def add_date_column(df: pd.DataFrame)-> pd.DataFrame:
    df["fecha"] = datetime.date.today()
    return df