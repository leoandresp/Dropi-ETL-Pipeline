from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import functools
import logging 
import glob
import os
import pandas as pd
from pandas.errors import EmptyDataError
from zipfile import BadZipFile
from datetime import datetime, timedelta
import hashlib
import uuid

# Configuración básica de logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

INGESTION_NAMESPACE = uuid.NAMESPACE_DNS

#------------------------------------------------------------
# FUNCIONES DECORADORAS
#------------------------------------------------------------

def try_exception_selenium(func):
    "Decorador que envuelve funciones de Selenium para capturar errores"
    
    @functools.wraps(func) #Guarda los metadatos de la funcion original
    def wrapper(*args,**kwargs): #Decora la funcion tomando aceptando todos sus argumentos
        try:
            return func(*args,**kwargs)
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"FALLO DE ELEMENTO en {func.__name__}. Selector: {args[2] if len(args) > 2 else 'N/A'}. Error: {type(e).__name__}")
            raise 
        except WebDriverException as e:
            logging.error(f"FALLO DEL DRIVER en {func.__name__}. Error: {type(e).__name__}")
            raise 
        except Exception as e:
            logging.error(f"ERROR INESPERADO en {func.__name__}. Detalle: {e}")
            raise
    return wrapper

def file_error_handler(func):
    """
    Decorador para manejar excepciones comunes durante la manipulación o 
    lectura de archivos (I/O, formato, archivo vacío, etc.).
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(f"ERROR: Archivo no encontrado. Revisar la ruta.")
            return None
        except (ValueError, EmptyDataError, BadZipFile):
            print(f"ERROR: El archivo no pudo ser leído por pandas (posiblemente corrupto o formato incorrecto).")
            return None
        except Exception as e:
            print(f"ERROR INESPERADO en la manipulación de archivos: {e}")
            return None
    return wrapper

def handle_pandas_errors(func):
    """
    Decorador para controlar errores de Pandas (ValueError, TypeError) 
    y otros errores inesperados.
    Si el error es de conversión de tipo (ValueError/TypeError), retorna None.
    Si es cualquier otro error, imprime una advertencia y retorna None.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Llama a la función original de procesamiento
            return func(*args, **kwargs)
        
        except (ValueError, TypeError) as e:
            # Captura errores comunes de Pandas como fallos de to_datetime
            # Retorna None para marcar el dato como faltante/inválido.
            # print(f"ADVERTENCIA: Fallo de conversión de tipo: {e}") 
            return None 
            
        except Exception as e:
            # Captura cualquier otro error no esperado (except genérico)
            print(f"ERROR FATAL INESPERADO en la función {func.__name__}: {e}. Retornando None.")
            return None
    return wrapper

def try_except_sheets(func):
    """Decorador que envuelve la función en un bloque try/except genérico para la api de Google Sheets"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"[Error] No se encontró el archivo: {e}")
        except Exception as e:
            print(f"[Error] Ocurrió un problema en '{func.__name__}': {e}")
    return wrapper

#--------------------------------------------
# FUNCIONES  OBTENCION Y MANIPULACIÓN DE ARCHIVOS
#-------------------------------------------


@file_error_handler
def read_excel_safely(file_path,columns_types=False):
    """Lee un archivo Excel y retorna su DataFrame, manejando errores a través del decorador."""
    if columns_types:
        return pd.read_excel(file_path,dtype=columns_types)
    else:
        return pd.read_excel(file_path)

def generate_sha256(text):
    """Genera un hash SHA256 de una cadena de texto."""
    if pd.isna(text): # Manejo de posibles NaN o None
        return None
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def add_ingestion_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea un ID de ingesta único basado en el contenido de la fila
    y un contador para filas idénticas (para idempotencia robusta).
    """
    
    # 1. Preparación y Generación del Hash de Contenido (Agrupador)
    
    # Crea una copia para trabajar y llena NaN con una cadena vacía para hashear
    df_temp = df.copy().fillna("")
    
    # Concatenar todas las columnas en una sola cadena de entrada
    columns_to_hash = df_temp.columns.tolist()
    df_temp['content_hash_input'] = df_temp[columns_to_hash].astype(str).agg('|'.join, axis=1)

    # Calcular el hash que servirá como ID de AGRUPACIÓN
    df['ingestion_id'] = df_temp['content_hash_input'].apply(generate_sha256)
    
    # Añadir la marca de tiempo de la ingesta
    df['ingestion_timestamp'] = pd.Timestamp.now()
    
    # 2. Diferenciar Filas Idénticas 
    
    df['row_number'] = df.groupby(['ingestion_id']).cumcount() + 1
    
    
    # 3. Calcular el ID de Ingesta FINAL ÚNICO (Recalcular el Hash)
    
    # Combina el hash de contenido con el número de fila. 
    df['final_hash_input'] = (
        df['ingestion_id'].astype(str) + 
        '_' + 
        df['row_number'].astype(str)
    )
    
    # Recalcula el hash
    df['ingestion_id'] = df['final_hash_input'].apply(generate_sha256)
    
    # Eliminar columnas auxiliares
    df = df.drop(columns=['final_hash_input'])
    
    return df



def get_files(path, file_name,multiple_files=False,columns_types=False):
    
    """
    Busca archivos en una ruta específica que coincidan con un nombre parcial.

    Si multiple_files es True, combina los archivos cuya fecha de modificación 
    esté dentro de los últimos 10 minutos.
    """
    logging.info(f"Iniciando extracción de la raw data de {file_name}")
    
    # 1. Definir el patrón de búsqueda y encontrar todos los archivos
    pattern = os.path.join(path, f'*{file_name}*')
    current_files = glob.glob(pattern)

    if not current_files:
        logging.info(f"INFO: No se encontraron archivos disponibles para {file_name}")
        return None

    # 2. Ordenar todos los archivos por fecha de modificación (más reciente primero)
    current_files.sort(key=os.path.getmtime, reverse=True)

    if not multiple_files:
        # Retornar el DataFrame del archivo más reciente
        latest_file = current_files[0]
        df = read_excel_safely(latest_file,columns_types)
        final_df = add_ingestion_id(df)
        
        #Eliminamos el archivo descargado
        #os.remove(latest_file)
        logging.info(f"{file_name} extraida correctamente")
        return  final_df

    # 3. Calcular el umbral de tiempo (hace 10 minutos)
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    
    # 4. Filtrar los archivos por fecha de modificación
    recent_files = []
    for file in current_files:
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file))
        
        # Si el archivo fue modificado después del umbral de 10 minutos
        #if file_mtime > ten_minutes_ago:
        if True:
            recent_files.append(file)
        else:
            # Optimización: si los archivos están ordenados, podemos detener el bucle
            break

    # 5. Procesar los archivos recientes
    if not recent_files:
        logging.info(f"INFO: No hay archivos que cumplan el filtro de 10 minutos de {file_name}")
        return None
        
    dataframes = []
    for file in recent_files:
        df = read_excel_safely(file,columns_types) 
        
        if df is not None:
            dataframes.append(df)
            #Eliminamos el archivo utilizado
            #os.remove(file)
        else:
            logging.error(f"ERROR: El archivo '{os.path.basename(file)}' fue omitido debido a un error de lectura.")

    if dataframes:
        # Combinar todos los DataFrames en una sola estructura
        combined_df = pd.concat(dataframes, axis=0, ignore_index=True)
        
        final_df = add_ingestion_id(combined_df)
        
        logging.info(f"{file_name} extraida correctamente")
        return final_df
    else:
        logging.error("ERROR: Los archivos encontrados en el rango de 10 minutos no pudieron ser leídos.")
        return None
    
    
