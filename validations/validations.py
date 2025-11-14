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


def absence_nulls_validation(df: pd.DataFrame, colums: List[str]) -> None:
    """
    Valida que las columnas especificadas no contengan valores nulos (NaN).
    Detiene el proceso si se encuentran nulos.
    """
    for col in colums:
        if col not in df.columns:
            logger.warning(f"⚠️ Advertencia: La columna '{col}' no existe en el DataFrame.")
            continue

        if df[col].isnull().any():
            columns_with_nulls = df.columns[df.isnull().any()].tolist()
            error_msg = (
                f"Se encontraron valores nulos (NaN) en las siguientes columnas especificadas: "
                f"{columns_with_nulls}. La carga de datos se detiene."
            )
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)
            
    logger.info("✅ Validación de ausencia de nulos exitosa.")


def positive_numeric_validation(df: pd.DataFrame, columns: List[str]) -> None:
    """
    Valida que las columnas especificadas sean numéricas y no contengan valores negativos.
    Detiene el proceso si encuentra valores no numéricos o negativos.
    """
    for col in columns:
        if col not in df.columns:
            logger.warning(f"⚠️ Advertencia: La columna '{col}' no existe en el DataFrame.")
            continue

        # 1. Validación de tipo numérico
        if not pd.api.types.is_numeric_dtype(df[col]):
             error_msg = (
                f"La columna '{col}' contiene datos no numéricos o de tipo incorrecto. "
                "Se esperaban datos numéricos. La carga de datos se detiene."
            )
             logger.error(f"❌ {error_msg}")
             raise ValueError(error_msg)

        # 2. Validación de ausencia de negativos
        if (df[col] < 0).any():
            negatives_found = df[df[col] < 0].shape[0]
            error_msg = (
                f"Se encontraron {negatives_found} valores negativos en la columna '{col}'. "
                "La carga de datos se detiene."
            )
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)

    logger.info("✅ Validación de valores numéricos positivos exitosa.")


def format_date_validation(df: pd.DataFrame, columns: List[str], format: str = '%Y-%m-%d') -> None:
    """
    Valida que las columnas especificadas contengan fechas válidas y en el formato correcto.
    Detiene el proceso si una fecha es inválida o no coincide con el formato.
    """
    for col in columns:
        if col not in df.columns:
            logger.warning(f"⚠️ Advertencia: La columna '{col}' no existe en el DataFrame.")
            continue

        # Intenta convertir la columna a datetime y los errores a NaT
        converted_dates = pd.to_datetime(df[col], format=format, errors='coerce')

        # Verifica si hay valores NaT (indicando fechas no válidas)
        if converted_dates.isnull().any():
            invalid_date = df.loc[converted_dates.isnull(), col].iloc[0]
            error_msg = (
                f"Se encontraron fechas inválidas o con formato incorrecto en la columna '{col}'. "
                f"Ejemplo de valor no válido: '{invalid_date}'. Se esperaba el formato '{format}'. "
                "La carga de datos se detiene."
            )
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)

    logger.info("✅ Validación de formato de fechas exitosa.")
    
    #-------------------------------------------------------------------------------------------------------
    # VALIDACIONES DE CARGA
    #-------------------------------------------------------------------------------------------------------
    
    def raw_data_validation(raw_data: list):
        
        