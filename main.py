import dropi_logic.scraping as sc
from dropi_logic.rpa_extractor import *
import time


driver = sc.WebDriverManager().get_driver()
driver.get("https://app.dropi.cl/auth/login")
current_windows = driver.current_window_handle


logging(driver,DROPI_USER,60,DROPI_PASS)
time.sleep(10)
access_module(driver,'Órdenes',10)
