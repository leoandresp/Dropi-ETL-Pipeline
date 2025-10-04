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
            if headless:
                # 1. Configuración de opciones.
                chrome_options = Options()
                
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
