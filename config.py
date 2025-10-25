import os
from dotenv import load_dotenv
from pathlib import Path

#Cargamos las variables del archivo .env
load_dotenv()

#--------------------------------------
#BASE DE DATOS
#-------------------------------------
DATABASE_FILE = "db/Oferfly.duckdb"
DF_ORDERS_DTYPE = {
    "FECHA DE REPORTE": str,
    "ID": str,
    "FECHA": str,
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
RAW_ORDERS= "RAW_Orders"
RAW_ORDERS_DETAILS = "RAW_Orders_details"
RAW_WARRANTYS = "RAW_Warrantys"
RAW_WALLET = "RAW_Wallet"
RAW_DEVOLUTIONS = "RAW_Devolutions"

#LOAD
RAW_LOAD =[RAW_ORDERS,RAW_ORDERS_DETAILS,RAW_WARRANTYS,RAW_WALLET,RAW_DEVOLUTIONS]

#Columnas que generaran Id unico para evitar duplicidad en la ingesta.
COLUMNS_UUID_INGS_ORDERS = ["FECHA DE REPORTE","ID","HORA","FECHA"]
COLUMNS_UUID_INGS_ORDERS_PRODUCT = ["FECHA DE REPORTE","ID","HORA","FECHA","PRODUCTO ID","VARIACION ID"]
COLUMNS_UUID_INGS_WARRANY = ["ID GARANTIA","ID ORDEN", "GUIA ORIGINAL","ESTADO","PRODUCTO","FECHA DE CREACION"]
COLUMNS_UUID_INGS_WALLET = ["ID","FECHA","TIPO","ORDEN ID","NUMERO DE GUIA"]
COLUMNS_UUID_INGS_DEVOLUTIONS = ["ID","PRODUCTO","USUARIO","BODEGA","TIPO","MOVIMIENTO","NUMERO DE GUIA"]

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
