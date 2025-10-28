import pandas as pd
import numpy as np
from typing import List, Union, Dict
from dropi_logic.utils import *
import datetime
from config import *
from db.database import *

# Se mantiene la función parse_date_smart como está

#---------------------------------------------------------------
#CLEAN FUNCTIONS------------------------------------------------
#---------------------------------------------------------------

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


#--------------------------------------------------------------------
#GENERAL TRANSFORMATION FUNCTIONS-----------------------------------
#--------------------------------------------------------------------


def split_column(df: pd.DataFrame, column_to_separate:str, 
                              separator_element:str, new_columns_name:list) -> pd.DataFrame:
    """
    Separa una columna de un DataFrame en dos nuevas columnas basándose en un separador,
    elimina la columna original y limpia los espacios en blanco alrededor de los valores.
    """
    if len(new_columns_name) != 2:
        raise ValueError("La lista 'nombres_nuevas_columnas' debe contener exactamente dos nombres.")

    # 1. Separar la columna. 'expand=True' crea un DataFrame con las partes separadas.
    #    '.str.strip()' se encadena para limpiar los espacios en blanco de cada parte.
    partes_separadas = df[column_to_separate].str.split(separator_element, expand=True).apply(lambda x: x.str.strip())

    # 2. Asignar los nombres a las nuevas columnas.
    partes_separadas.columns = new_columns_name

    # 3. Concatenar las nuevas columnas al DataFrame original.
    df = pd.concat([df, partes_separadas], axis=1)

    # 4. Eliminar la columna original.
    df = df.drop(columns=[column_to_separate])

    return df

@handle_pandas_errors
def parse_date_with_formats(date_str: str) -> pd.Timestamp:
    """
    Intenta parsear una cadena de fecha con múltiples formatos.
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


if __name__ == "__main__":
    
    #--------------------------------------------------------------
    #TRANSFORMACIÓN CAPA SILVER------------------------------------
    #--------------------------------------------------------------
    
    print("Incio de limpieza de datos para capa Silver")
    
    #Obtenemos la RAW DATA
    raw_data = [direct_query_data(f"SELECT * FROM {df}") for df in RAW_LOAD]
    
    #Limpiamos la DATA
    silver_data = silver_data = clean_list_of_dataframes(raw_data,DICT_DATES)
    
    #Realizamos las Transformaciones correspondientes
    silver_data[2] = split_column(silver_data[2],"PRODUCTO","-",["ID PRODUCTO","DESCRIPCION PRODUCTO"])
    
    