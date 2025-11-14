import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import logging

#Cargamos las variables del archivo .env
load_dotenv()

# Configurar logging (mantenido igual)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


#Rutas Base del Proyecto
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "db"


# --- Configuración de la ruta del ejecutable de Python para multiplataforma ---

#Nombre de la carpeta del VENV
VENV_NAME = 'dropi-extractor-venv'

if sys.platform == 'win32':
    PYTHON_EXECUTABLE = BASE_DIR  / VENV_NAME / 'Scripts' / 'python.exe'
elif sys.platform.startswith('linux') or sys.platform == 'darwin':
    PYTHON_EXECUTABLE = BASE_DIR / VENV_NAME / 'bin' / 'python'
else:
    # Caso por defecto o no soportado, podría requerir ajuste
    raise OSError(f"Plataforma no soportada: {sys.platform}")



#--------------------------------------
#BASE DE DATOS
#-------------------------------------
DATABASE_FILE = str(DB_DIR / "Oferfly.duckdb")
DF_ORDERS_DTYPE = {
    "FECHA DE REPORTE": str,
    "ID": str,
    "FECHA": str,
    "NÚMERO GUIA": str,
    "TOTAL DE LA ORDEN": float,
    "GANANCIA": float,
    "PRECIO FLETE": float,
    "COSTO DEVOLUCION FLETE": float,
    "COMISION": float,
    "FECHA DE NOVEDAD": str,
    "FECHA DE SOLUCIÓN": str,
    "FECHA DE ÚLTIMO MOVIMIENTO":str,
    "ID DE ORDEN DE TIENDA": str,
    "NUMERO DE PEDIDO DE TIENDA": str,
    "FECHA GENERACION DE GUIA":str,
    "CODIGO POSTAL": str
}

DF_ORDERS_PRODUCTS_DTYPE = {
    "FECHA DE REPORTE": str,
    "ID": str,
    "FECHA": str,
    "NÚMERO GUIA": str,
    "TOTAL DE LA ORDEN": float,
    "GANANCIA": float,
    "PRECIO FLETE": float,
    "COSTO DEVOLUCION FLETE": float,
    "COMISION": float,
    "PRECIO PROVEEDOR":float,
    "PRECIO PROVEEDOR X CANTIDAD":float,
    "PRODUCTO ID":str,
    "VARIACION ID":str,
    "CANTIDAD":int,
    "FECHA DE NOVEDAD": str,
    "FECHA DE SOLUCIÓN": str,
    "FECHA DE ÚLTIMO MOVIMIENTO":str,
    "ID DE ORDEN DE TIENDA": str,
    "NUMERO DE PEDIDO DE TIENDA": str,
    "FECHA GENERACION DE GUIA":str,
    "CODIGO POSTAL": str
}

DF_WARRANTY_DTYPE = {
    "ID GARANTIA": str,
    "ID ORDEN":str,
    "GUIA ORIGINAL":str,
    "NUMERO DE CONTACTO TIENDA":str,
    "NUMERO DE PROVEEDOR":str,
    "FECHA DE CREACION":str,
    "GUIA DE DESPACHO":str,
    "NUMERO DE GUIA O ORDEN DE RECOLECCION":str
}

DF_WALLET_DTYPE = {
    "ID":str,
    "FECHA":str,
    "MONTO":float,
    "MONTO PREVIO":float,
    "ORDEN ID":str,
    "NUMERO DE GUIA":str,
}

DF_DEVOLUTIONS_DTYPE = {
    "ID":str,
    "MOVIMIENTO": float,
    "STOCK PREVIO":float,
    "STOCK ACTUAL":float,
    "NUMERO DE GUIA":str
}

#TablesName
RAW_ORDERS= "RAW_ORDERS"
RAW_ORDERS_PRODUCT = "RAW_ORDERS_PRODUCTS"
RAW_WARRANTYS = "RAW_WARRANTYS"
RAW_WALLET = "RAW_WALLET"
RAW_DEVOLUTIONS = "RAW_DEVOLUTIONS"
ORDERS = "ORDERS"
ORDERS_PRODUCT = "ORDERS_PRODUCT"
WARRANTYS = "WARRANTYS"
WALLET = "WALLET"
DEVOLUTION = "DEVOLUTIONS"
GENERAL_SALES = "GENERAL_SALES"

#QUERYS
SQL_GET_GENERAL_SALES_DATA =  DB_DIR / "querys" /   "general_sales_report.sql"
SQL_UPSERT_ORDERS_DATA =   DB_DIR / "querys" / "upserts" /"orders_upsert.sql"
SQL_UPSERT_ORDERS_PRODUCT_DATA = DB_DIR / "querys" / "upserts" / "orders_product_upsert.sql"
SQL_UPSERT_WALLET_DATA = DB_DIR / "querys" / "upserts" /"wallet_upsert.sql"
SQL_UPSERT_DEVOLUTION_DATA = DB_DIR / "querys" / "upserts" / "devolutions_upsert.sql" 
SQL_UPSERT_GENERAL_SALES_DATA = DB_DIR / "querys" / "upserts" /"general_sales_upsert.sql"


#LOAD
RAW_TABLES =[RAW_ORDERS,RAW_ORDERS_PRODUCT,RAW_WARRANTYS,RAW_WALLET,RAW_DEVOLUTIONS]


#------------------------------------------------------------------
#EXTRACT----------------------------------------------------------
#------------------------------------------------------------------

ID_ORDER_PRUDCUCT = "ID_ORDER_PRODUCT" #Nombre de ID unico para Orders_product
ID = "ID" #Primera parte de la concatenación del campo unique ID de Orders_product
ROW_NUMBER = "row_number" #Segunda parte de la concatenación del campo unique ID de Orders_product

#--------------------------------------------------------------------
#TRANSFORM
#--------------------------------------------------------------------

#Columnas que serán transformadas en tipo fecha.
DICT_DATES = {
    0: ["FECHA DE REPORTE","FECHA","FECHA DE NOVEDAD","FECHA DE SOLUCIÓN","FECHA DE ÚLTIMO MOVIMIENTO","FECHA GENERACION DE GUIA"],
    1: ["FECHA DE REPORTE","FECHA","FECHA DE NOVEDAD","FECHA DE SOLUCIÓN","FECHA DE ÚLTIMO MOVIMIENTO","FECHA GUIA GENERADA"],
    2: ["FECHA DE CREACION"],
    3:["FECHA"],
    4: []
}

DICT_STATUS = {
        "DEVOLUCION A REMITENTE": "EN DEVOLUCION",
        "EN REPARTO": "EN TRANSITO",
        "CANCELADO": "CANCELADO",
        "ENTREGADO": "ENTREGADO",
        "DEVOLUCION": "DEVUELTO",
        "INGRESO CAMION": "EN TRANSITO",
        "NOVEDAD SOLUCIONADA": "EN TRANSITO",
        "NADIE EN CASA": "EN TRANSITO",
        "NOVEDAD": "EN TRANSITO",
        "EN ESPERA EN OFICINA": "EN TRANSITO",
        "PICK UP HUB": "EN TRANSITO",
        "GUIA_GENERADA": "GUIA GENERADA",
        "PENDIENTE": "PENDIENTE",
        "CARGA EN TRANSITO": "EN TRANSITO",
        "ADMITIDA EN SUCURSAL": "EN TRANSITO",
        "SIN ACCESO": "EN TRANSITO",
        "REHUZA PRODUCTO": "EN DEVOLUCION",
        "OFICINA CERRADA": "EN TRANSITO"
    }



#Consulta para obtener los datos de la última ingesta
SQL_GET_LAST_RAW_DATA = "SELECT * FROM {} WHERE  ingestion_timestamp = (SELECT MAX(ingestion_timestamp) FROM {})"

#Constantes para lógica de separación del campo Producto en Garantias
WARRANTY_SPLIT_COLUMN = "PRODUCTO"
WARRANTY_LIST_SPLITTED = ["ID PRODUCTO","DESCRIPCION PRODUCTO"]
WARRANTY_RANAMED_COLUMNS = {"ID GARANTIA":"ID"}

#--------------------------------------
#GOOGLE SHEETS CONFIG
#-------------------------------------
DROPI_SHEETS_ID = os.environ.get('DROPI_SHEETS_ID')
SHEETS_KEY_PATH = BASE_DIR / "assets" / "anakarinadropi-572e7897ef4c.json"

#--------------------------------------
#Rutas universales del SO
#-------------------------------------

home_directory = Path.home()

download_path_object = home_directory / "Downloads" 
DOWNLOAD_FOLDER = str(download_path_object) #String de Ruta de Descargar

#---------------------------------------
#VALIDATION
#--------------------------------------

#Lista de Validación de Nulos
LIST_RAW_ORDER_NULL_VALIDATION =["ID","ingestion_id","ingestion_timestamp","row_number"]
LIST_RAW_WARRANRY_NULL_VALIDATION = ["ID GARANTIA","ID ORDEN","ingestion_id","ingestion_timestamp","row_number"]
LIST_RAW_WALLET_NULL_VALIDATION =["ID","ingestion_id","ORDEN ID","NUMERO DE GUIA","ingestion_timestamp","row_number"]
LIST_RAW_DEVOLUTION_NULL_VALIDATION =["ID","NUMERO DE GUIA","ingestion_id","ingestion_timestamp","row_number"]

#Lista de Validación Numerica




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

#Sub-Strings DE NOMBRES DE LOS REPORTES RECIEN DESCARGADOS
ORDER_BY_ROW_FILE_NAME = "ordenes-"
ORDER_BY_PRODUCT_FILE_NAME = "ordenes_productos"
WARRANTY_FILE_NAME = "garantias"
WALLET_FILE_NAME = "historial"
DEVOLUTIONS_FILE_NAME = "excelInfoDevolutions"


#VARIABLES GLOBALES
ACTION_WITH_REPORT_LIST = [
    'Formato de órdenes Masivas', 'Órdenes (Una orden por fila)', 'Órdenes con Productos (Un producto por fila)'
    ]
