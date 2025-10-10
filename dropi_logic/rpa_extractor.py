from .scraping import * 
from .utils import try_exception_selenium 
from config import *
 

#Funciones para el extractor de Datos Droppi

#Inicio de Sesión
@try_exception_selenium
def logging(driver,user,wait_time,password):
    input_action(driver,By.ID,'email',wait_time,user)
    input_action(driver,By.ID,'password',wait_time,password)
    click_action(driver,By.XPATH, "//button[.//span[text()='Iniciar Sesión']]", 60)

#Ingresar a los módulos principales
@try_exception_selenium
def access_module(driver,module,wait_time):
    click_action(driver,By.XPATH, rf"//a[.//span[contains(text(), '{module}')]]",wait_time)

#Acceder a los Sub-Módulos
@try_exception_selenium
def access_sub_module(driver,submodule,wait_time):
    click_action(driver, By.XPATH, rf"//a[contains(text(), '{submodule}')]", wait_time)
    
#Presionar alguna acción dentro de los módulos.
@try_exception_selenium    
def module_actions_button(driver,action,wait_time):
    click_action(driver, By.XPATH, rf"//a[contains(text(), 'Acciones')]", wait_time)
    click_action(driver, By.XPATH, rf"//button[contains(text(), '{action}')]", wait_time)
    
    if action in ACTION_WITH_REPORT_LIST: 
        click_action(driver, By.XPATH, "//button[contains(text(), 'Ver reportes')]", 10)
            
    else:
        pass
    
def download_report(driver,index_row,wait_time):
    
    report_table = waitAndFindElement(driver,By.CLASS_NAME,"table",wait_time) #Ubicamos la tabla del módulo
    row = waitAndFindElement(driver,By.XPATH, f".//tbody/tr[{index_row}]",wait_time) #Indicamos la fila donde se descargará el reporte
    click_action(driver,By.XPATH,"//app-icon[.//use[contains(@xlink:href, '#File-download')]]",wait_time)

if __name__ == "__main__":
    pass
    