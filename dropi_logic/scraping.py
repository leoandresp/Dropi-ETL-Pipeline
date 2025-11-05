from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dropi_logic.utils import try_exception_selenium



class WebDriverManager:
    _driver = None 

    #Crea y descarga el driver manager en caso que no exista.        
    @staticmethod
    def get_driver(headless=False):
        try:
            # 1. Configuración de opciones.
            chrome_options = Options()
            #Forzamos al idioma español
            chrome_options.add_argument("--lang=es")
            
            if headless:
                #Opciones para ejecución en segundo plano sin interfaz.
                chrome_options.add_argument("--headless=new") 
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
                
            if WebDriverManager._driver is None:
                # 2. Instalación y descarga Automática de ChromeDriver
                service = ChromeService(ChromeDriverManager().install())
                WebDriverManager._driver = webdriver.Chrome(service=service,options=chrome_options)
                WebDriverManager._driver.maximize_window()
                return WebDriverManager._driver
        
        except Exception as e:
            print(f"Se ha encontrado un error inesperado {e}")
     
     #Cierra el ChromeDriver   
    @staticmethod
    def quit_driver():
        if WebDriverManager._driver:
            WebDriverManager._driver.quit()
            WebDriverManager._driver = None
    
#Espera y retorna un único elemento presente en el DOM (Búsqueda limpia).
@try_exception_selenium
def waitAndFindElement(driver,by_method,name_element:str,time:int):
    return WebDriverWait(driver,time).until(
            EC.presence_of_element_located(((by_method,name_element)))
            )

#Encuentra, espera y presiona un elemento.
@try_exception_selenium
def click_action(driver,by_method,name_element:str, time:int):
    op = waitAndFindElement(driver,by_method,name_element, time)
    op.click()

#Encuentra, espera y escribe sobre un campo
@try_exception_selenium
def input_action(driver,by_method,name_element:str, time:int,text:str):
    op = waitAndFindElement(driver,by_method,name_element, time)
    op.send_keys(text)

def close_new_windows_and_return_to_main(driver, principal_window_handle: str):
    """
    Busca y cierra todas las ventanas (pestañas o pop-ups) que no sean 
    la ventana principal, y luego devuelve el foco del driver a la principal.
    """
    
    all_windows = driver.window_handles
    
    # Solo procesamos si hay más de una ventana abierta
    if len(all_windows) > 1:
        print("Detectada(s) nueva(s) ventana(s). Procediendo a cerrar.")
        
        # Iteramos sobre todos los identificadores de ventana
        for window_handle in all_windows:
            if window_handle != principal_window_handle:
                # Cambiamos el foco a la nueva ventana
                driver.switch_to.window(window_handle)
                driver.close() # Cerramos la ventana
                
        # Una vez que todas las ventanas nuevas han sido cerradas,
        # es OBLIGATORIO devolver el foco a la ventana principal.
        driver.switch_to.window(principal_window_handle)
        print("Foco devuelto a la ventana principal.")
    else:
        print("No se detectaron ventanas adicionales para cerrar.")