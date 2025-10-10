import dropi_logic.scraping as sc
from dropi_logic.rpa_extractor import *
import time


#Configuramos la conexión con el navegador
driver = sc.WebDriverManager().get_driver()
driver.get("https://app.dropi.cl/auth/login")
current_windows = driver.current_window_handle

#Nos logueamos en la Página de Dropi
logging(driver,DROPI_USER,60,DROPI_PASS) 
time.sleep(20) #Esperamos a que desaparezcan los distintos modales

#Accedemos al primer módulo para descargar el reporte
access_module(driver,'Órdenes',60)
access_sub_module(driver,'Mis Pedidos',60)

#Seleccionamos Los dos tipos de reporte que necesitamos descargar
module_actions_button(driver,'Órdenes (Una orden por fila)',10)
time.sleep(180)
driver.refresh()
download_report(driver,1,10)