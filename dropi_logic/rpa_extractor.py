from .scraping import * 
from .utils import try_exception_selenium 
from config import *
 

#Funciones para el extractor de Datos Droppi

@try_exception_selenium
def logging(driver,user,wait_time,password):
    input_action(driver,By.ID,'email',wait_time,user)
    input_action(driver,By.ID,'password',wait_time,password)
    click_action(driver,By.XPATH, "//button[.//span[text()='Iniciar Sesión']]", 60)

@try_exception_selenium
def access_module(driver,module,wait_time):
    click_action(driver,By.XPATH, rf"//a[.//span[contains(text(), '{module}')]]",wait_time)

if __name__ == "__main__":
    pass
    