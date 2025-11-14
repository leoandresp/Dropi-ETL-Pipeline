import pandas as pd
import logging
from typing import List, Optional
from config import *


# Obtener un logger para usar en las funciones
logger = logging.getLogger(__name__)


def no_none_validation(df: Optional[pd.DataFrame]) -> None:
    
    """
    Valida que el DataFrame no sea None.
    """
    if df is None:
        error_msg = "El DataFrame de entrada es None. La carga de datos se detiene."
        logger.error(f"❌ {error_msg}")
        raise ValueError(error_msg)
    logger.info("✅Validación de DataFrame no-None exitosa.")


def absence_nulls_validation(df: pd.DataFrame, colums: List[str],df_name:str) -> None:
    
    """
    Valida que las columnas especificadas no contengan valores nulos (NaN).
    Detiene el proceso si se encuentran nulos e informa las filas.
    """
    if df is None:
        logging.info(f"No hay df que evaluar en {df_name}")
        return
    
    for col in colums:
        if col not in df.columns:
            logger.warning(f"⚠️ Advertencia: La columna '{col}' no existe en el DataFrame en {df_name}")
            continue

        if df[col].isnull().any():
            # Obtener los índices de las filas con nulos en la columna actual
            null_rows_indices = df[df[col].isnull()].index.tolist()
            
            error_msg = (
                f"Se encontraron **valores nulos (NaN)** en la columna '{col}' en las "
                f"siguientes filas (índices): **{null_rows_indices}** de la tabla {df_name}. "
                "La carga de datos se detiene."
            )
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)
            
    logger.info(f"✅ Validación de ausencia de nulos exitosa en {df_name}.")


def positive_numeric_validation(df: pd.DataFrame, columns: List[str],df_name:str) -> None:

        
    """
    Valida que las columnas especificadas sean numéricas y no contengan valores negativos.
    Detiene el proceso si encuentra valores no numéricos o negativos.
    """
        
    if df is None:
        logging.info(f"No hay df que evaluar en {df_name}")
        return
    
    for col in columns:
        if col not in df.columns:
            logger.warning(f"⚠️ Advertencia: La columna '{col}' no existe en el DataFrame en {df_name}.")
            continue

        # 1. Validación de tipo numérico
        if not pd.api.types.is_numeric_dtype(df[col]):
             error_msg = (
                f"La columna '{col}' contiene datos no numéricos o de tipo incorrecto en {df_name}. "
                "Se esperaban datos numéricos. La carga de datos se detiene."
            )
             logger.error(f"❌ {error_msg}")
             raise ValueError(error_msg)

        # 2. Validación de ausencia de negativos
        if (df[col] < 0).any():
            negatives_found = df[df[col] < 0].shape[0]
            error_msg = (
                f"Se encontraron {negatives_found} valores negativos en la columna '{col}' en {df_name}. "
                "La carga de datos se detiene."
            )
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)

    logger.info(f"✅ Validación de valores numéricos positivos exitosa en {df_name}.")


    
    #-------------------------------------------------------------------------------------------------------
    # VALIDACIONES DE CARGA
    #-------------------------------------------------------------------------------------------------------
    
def raw_data_validation(raw_data: list):
        
        #Validamos datos que no deben estar nulos.
        raw_list_null_validation = [LIST_RAW_ORDER_NULL_VALIDATION,LIST_RAW_ORDER_NULL_VALIDATION,LIST_RAW_WARRANRY_NULL_VALIDATION,LIST_RAW_WALLET_NULL_VALIDATION,LIST_RAW_DEVOLUTION_NULL_VALIDATION]
        
        for i in range(len(raw_data)):
            absence_nulls_validation(raw_data[i],raw_list_null_validation[i],RAW_TABLES[i])
        
        logging.info("Validación de Raw data Completada")
        
def silver_data_validation(silver_data:list):
        silver_list_null_validation = [LIST_ORDER_NULL_VALIDATION,LIST_ORDER_PRODUCT_NULL_VALIDATION,
                                       LIST_WARRANTY_NULL_VALIDATION,LIST_WALLET_NULL_VALIDATION,
                                       LIST_DEVOLUTION_NULL_VALIDATION]
        
        SILVER_TABLE_NAMES_FOR_NULL = [ORDERS,ORDERS_PRODUCT,WARRANTYS,WALLET,DEVOLUTION]
        
        df_silver_number_validation = [silver_data[0],silver_data[1],silver_data[3]]
        silver_list_number_validation = [LIST_ORDER_NUMBER_VALIDATION,LIST_ORDER_NUMBER_VALIDATION,LIST_WALLET_NUMBER_VALIDATION]
        
        #Validamos los valores nulos
        SILVER_TABLE_NAMES_FOR_NULL = [ORDERS,ORDERS_PRODUCT,WARRANTYS,WALLET,DEVOLUTION]
        for i in range(len(silver_data)):
            absence_nulls_validation(silver_data[i],silver_list_null_validation[i],SILVER_TABLE_NAMES_FOR_NULL[i])
            
        #Validamos que los números tenga un correcto formato
        SILVER_TABLE_NAMES_FOR_NUMBER = [ORDERS,ORDERS_PRODUCT,WALLET]
        for i in range(len(df_silver_number_validation)):
            positive_numeric_validation(df_silver_number_validation[i],silver_list_number_validation[i],
                                        SILVER_TABLE_NAMES_FOR_NUMBER[i])
        
        logging.info("Validación de Silver data Completada")
    
def gold_data_validation(gold_data):
        #Validamos que los números tenga un correcto formato
        positive_numeric_validation(gold_data,LIST_GENERAL_SALES_NUMBER_VALIDATION,GENERAL_SALES)

        logging.info("Validación de gold data Completada")