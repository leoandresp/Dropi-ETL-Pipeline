from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import functools
import logging 

# Configuración básica de logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
