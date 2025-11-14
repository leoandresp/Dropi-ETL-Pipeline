from .scraping import * 
from .utils import try_exception_selenium 
from config import *
from selenium.webdriver import ActionChains
import datetime
import time
from config import *

#Funciones para el extractor de Datos Droppi

#Inicio de Sesión
@try_exception_selenium
def log_in(driver,user,wait_time,password):
    input_action(driver,By.ID,'email',wait_time,user)
    input_action(driver,By.ID,'password',wait_time,password)
    click_action(driver,By.XPATH, "//button[.//span[text()='Iniciar Sesión']]", 60)

#Ingresar a los módulos principales
@try_exception_selenium
def access_module(driver,module,wait_time):
    logging.info(f"Accediendo al módulo {module}")
    click_action(driver,By.XPATH, rf"//a[.//span[contains(text(), '{module}')]]",wait_time)

#Acceder a los Sub-Módulos
@try_exception_selenium
def access_sub_module(driver,submodule,wait_time):
    logging.info(f"Accediendo al Sub-módulo {submodule}")
    click_action(driver, By.XPATH, rf"//a[contains(text(), '{submodule}')]", wait_time)
    
#Presionar alguna acción dentro de los módulos.
@try_exception_selenium    
def module_actions_button(driver,action,wait_time):
    xpath_acciones = rf"//a[contains(text(), 'Acciones')]"
    
    #Validamos si existen el botón de "Acciones", sino presionamos la acción directamente
    if element_exists(driver,By.XPATH,xpath_acciones):
        logging.info(f"Presionando {action}")
        click_action(driver, By.XPATH, rf"//a[contains(text(), 'Acciones')]", wait_time)
        click_action(driver, By.XPATH, rf"//button[contains(text(), '{action}')]", wait_time)
    else:
        logging.info(f"Presionando {action}")
        click_action(driver, By.XPATH, rf"//button[contains(span, '{action}')]", wait_time)
    
    if action in ACTION_WITH_REPORT_LIST: 
        logging.info(f"Cambiando al módulo de Reportes")
        click_action(driver, By.XPATH, "//button[contains(text(), 'Ver reportes')]", 10)

@try_exception_selenium
def element_exists(driver, by, value):
    # Busca los elementos con un timeout muy corto (e.g., 1 segundo)
    # y retorna True o False sin lanzar excepción.
    driver.implicitly_wait(1) 
    found = len(driver.find_elements(by, value)) > 0
    driver.implicitly_wait(10) # Restaura el implicit wait original
    return found

@try_exception_selenium    
def download_report(driver,index_row,wait_time):
    
    report_table = waitAndFindElement(driver,By.CLASS_NAME, "custom-table",wait_time) #Ubicamos la tabla del módulo
    print("Tabla encontrada")
    row = report_table.find_element(By.XPATH, f"./tbody/tr[{index_row}]") #Indicamos la fila donde se descargará el reporte
    print("Fila encontrada")
    
    download_icon = row.find_element(
    By.XPATH,
    ".//td[contains(@class,'action-button')]//app-icon[1]"
    )
    
    actions = ActionChains(driver)
    actions.move_to_element(download_icon).click().perform()

@try_exception_selenium 
def logistic(driver, action):
    if action == 'Devoluciones':
        logging.info(f"Accediendo al Sub-módulo Devoluciones")
        click_action(driver, By.XPATH, "//a[contains(text(), 'Devoluciones')]", 10)
        #current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")


        # Espera la tabla usando un selector CSS
        principal_window = driver.current_window_handle

        table = waitAndFindElement(
                driver, 
                By.CSS_SELECTOR, 
                "table.table-centered.table-nowrap.mb-0.align-middle.table-hover", 
                60
            )

        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # omitir encabezado
        count = 0 #Para mostrar cuantos archivos se descargaron
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            row_date = cols[3].text.strip()

            # Solo tomar la parte YYYY-MM-DD
            row_date = row_date.split("T")[0]

            print("Actual:", current_date, "Fila:", row_date)

            if row_date == current_date:
                    download_btn = row.find_element(By.XPATH, ".//a[contains(@class, 'btn-outline-success')]")
                    driver.execute_script("arguments[0].scrollIntoView(true);", download_btn)
                    download_btn.click()
                    time.sleep(5)  # espera por la descarga
                    close_new_windows_and_return_to_main(driver,principal_window)
                    
        logging.info(f"Fueron descargados {count} reportes de devoluciones")
                    

if __name__ == "__main__":
    pass
    