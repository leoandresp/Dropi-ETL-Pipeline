import os
from dotenv import load_dotenv

#Cargamos las variables del archivo .env
load_dotenv()


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


#VARIABLES GLOBALES
ACTION_WITH_REPORT_LIST = [
    'Formato de órdenes Masivas', 'Órdenes (Una orden por fila)', 'Órdenes con Productos (Un producto por fila)'
    ]
