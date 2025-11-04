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

#
def add_date_column(df: pd.DataFrame)-> pd.DataFrame:
    """
    Añade una columna fecha a un dataframe
    """
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

    separates_parts = df[column_to_separate].str.split(separator_element, expand=True).apply(lambda x: x.str.strip())

    # 2. Asignar los nombres a las nuevas columnas.
    separates_parts.columns = new_columns_name

    # 3. Concatenar las nuevas columnas al DataFrame original.
    df = pd.concat([df, separates_parts], axis=1)

    # 4. Eliminar la columna original.
    df = df.drop(columns=[column_to_separate])

    return df

@handle_pandas_errors
def parse_date_with_formats(date_str: str) -> pd.Timestamp:
    """
    Intenta parsear una cadena de fecha con múltiples formatos.
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

def renames_columns(df: pd.DataFrame,columns_renamed:dict) -> pd.DataFrame:
    ''' Renombra un grupo de columnas de un dataframe'''
    df_renamed = df.rename(columns_renamed)
    return df_renamed

def add_unique_product_id(df: pd.DataFrame)-> pd.DataFrame:
    '''Crea un ID unico para la Tabla de Orders_Product'''
    df[ID_ORDER_PRUDCUCT] = (
        df[ID].astype(str) + 
        '-' + 
        df[ROW_NUMBER].astype(str)
    )
    return df

def mapping_column(df: pd.DataFrame,column:str,dt_mapped:dict) -> pd.DataFrame:
    '''
    Mapea los valores de una columna por otros según un diccionario previamente establecido
    '''
    df[column] = df[column].apply(lambda x: dt_mapped.get(x,"SIN DEFINIR"))
    return df
    
#--------------------------------------------------------------
#TRANSFORMACIÓN CAPA SILVER------------------------------------
#--------------------------------------------------------------
    
def clean_raw_data(data):
        print("Incio de limpieza de datos para capa Silver")        
        #Limpiamos la DATA
        print("Limpienado datos")
        silver_data = clean_list_of_dataframes(data,DICT_DATES)
        return silver_data


def silver_data_transform(data):
    
    #Realizamos las Transformaciones correspondientes
    print("Realizando las tranformaciones correspondientes")
    #Dividimos la columna de producto
    data[2] = split_column(data[2],WARRANTY_SPLIT_COLUMN,"-",WARRANTY_LIST_SPLITTED) 
    
    #Renombramos el ID GARANTIA por ID
    data[2] = renames_columns(data[2],WARRANTY_RANAMED_COLUMNS)
    
    #Mapeamos el Status según las reglas de negocio solicitadas
    data[0] = mapping_column(data[0],"ESTATUS",DICT_STATUS) #MAPEAMOS ORDERS
    data[1] = mapping_column(data[1],"ESTATUS",DICT_STATUS) #MAPEAMOS ORDERS_PRODUCTS
    
    #Añadimos un ID unico al df que tiene el detalle de ordenes y sus productos
    data[1] = add_unique_product_id(data[1])
    
    return data
        

    
    
    