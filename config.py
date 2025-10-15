import os
from dotenv import load_dotenv
from pathlib import Path

#Cargamos las variables del archivo .env
load_dotenv()

#--------------------------------------
#BASE DE DATOS
#-------------------------------------
DATABASE_FILE = ""



#--------------------------------------
#Rutas universales del SO
#-------------------------------------

home_directory = Path.home()
download_path_object = home_directory / "Downloads" 
DOWNLOAD_FOLDER = str(download_path_object) #String de Ruta de Descargar


#---------------------------------------
#SCRAPPING CONFIG
#--------------------------------------
DROPI_WEB = "https://app.dropi.cl/auth/login"
DROPI_USER = os.environ.get('DROPI_USER')
DROPI_PASS = os.environ.get('DROPI_PASS')

#NOMBRES DE LOS MÓDULOS(M), SUBMODULOS(SB) y  ACCIONES(A)
M_ORDERS = 'Órdenes'
SB_MY_ORDERS = 'Mis Pedidos'
A_ORDER_BY_ROW = 'Órdenes (Una orden por fila)'
A_ORDER_BY_PRODUCT = 'Órdenes con Productos (Un producto por fila)'

M_MY_WARRANTYS = 'Mis Garantias'
SB_WARRANTYS = 'Garantias'

M_WALLET = 'Historial de Cartera'

M_LOGISTIC = 'Logistic'
SB_DEVOLUTIONS = 'Devoluciones'

A_EXCEL_DOWNLOAD = 'Descargar en Excel'

#CONTENEDORES DE NOMBRES DE LOS REPORTES RECIEN DESCARGADOS
ORDER_BY_ROW_FILE_NAME = "ordenes-"
ORDER_BY_PRODUCT_FILE_NAME = "ordenes_productos"
WARRANTY_FILE_NAME = "garantias"
WALLET_FILE_NAME = "historial"
DEVOLUTIONS_FILE_NAME = "excelInfoDevolutions"


#VARIABLES GLOBALES
ACTION_WITH_REPORT_LIST = [
    'Formato de órdenes Masivas', 'Órdenes (Una orden por fila)', 'Órdenes con Productos (Un producto por fila)'
    ]
