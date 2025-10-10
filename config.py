import os
from dotenv import load_dotenv

#Cargamos las variables del archivo .env
load_dotenv()

#CREDENCIALES
DROPI_USER = os.environ.get('DROPI_USER')
DROPI_PASS = os.environ.get('DROPI_PASS')

#VARIABLES GLOBALES
ACTION_WITH_REPORT_LIST = [
    'Formato de órdenes Masivas', 'Órdenes (Una orden por fila)', 'Órdenes con Productos (Un producto por fila)'
    ]
