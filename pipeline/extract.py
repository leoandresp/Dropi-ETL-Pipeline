import dropi_logic.scraping as sc
from dropi_logic.rpa_extractor import *
from dropi_logic.utils import *
from config import *
import time
from db.database import * 
from pipeline.load import *



#Descargar el reporte seleccionado de los modulos, solo aplica para los que tienen boton de "Acciones" dentro de su módulo
def download_report_module(driver,action,wait_time,module,submodule=False):
    principal_window = driver.current_window_handle #guardamos la ventana en la que estamos actualmente
    
    access_module(driver,module,wait_time) #Ingesamos al módulo
    if submodule: 
        access_sub_module(driver,submodule,wait_time) #En caso que exista un sub-módulo
    
    
    #Presionamos la acción para el reporte que necesitamos, esperamos que se genere y lo descargamos
    module_actions_button(driver,action,10)
    time.sleep(5)
    
    #Volvemos a la pantalla principal
    close_new_windows_and_return_to_main(driver,principal_window)
        
    if action == A_EXCEL_DOWNLOAD:
        return print(f"Descarga de {action} realizada")
    
    time.sleep(180)
    driver.refresh()
    download_report(driver,1,10)
    time.sleep(10)
    print(f"Descarga de {action} realizada")
  
#HOT FIX: DESCARCODEAR LUEGO, HACERLA REUTILIZABLE. Actualmente se requiere entrega rapida al cliente    
def extract_data():
    '''
    print(f"Inicia la extracción de Datos desde DROPI")
    
    #Configuramos la conexión con el navegador
    driver = sc.WebDriverManager().get_driver()
    driver.get(DROPI_WEB)
    
    #Nos logueamos en la Página de Dropi
    log_in(driver,DROPI_USER,60,DROPI_PASS) 
    time.sleep(20) #Esperamos a que desaparezcan los distintos modales
    
    #Descargamos las ordenes por fila, producto, garantias e historial de Cartera
    download_report_module(driver,A_ORDER_BY_ROW,60,M_ORDERS,SB_MY_ORDERS)
    download_report_module(driver,A_ORDER_BY_PRODUCT,60,M_ORDERS,SB_MY_ORDERS)
    download_report_module(driver,A_EXCEL_DOWNLOAD,60,M_MY_WARRANTYS,SB_WARRANTYS)
    download_report_module(driver,A_EXCEL_DOWNLOAD,60,M_WALLET)
    
    #Descargamos las Devoluciones
    access_module(driver,M_LOGISTIC,60)
    logistic(driver,SB_DEVOLUTIONS)
    
    print(f"Guardando la data extraida en repectivos DF")
    '''
    #Guardamos los datos correspondientes en dataframes
    df_order_by_row = get_files(DOWNLOAD_FOLDER,ORDER_BY_ROW_FILE_NAME,columns_types=DF_ORDERS_DTYPE)
    df_order_by_product = get_files(DOWNLOAD_FOLDER,ORDER_BY_PRODUCT_FILE_NAME, columns_types=DF_ORDERS_PRODUCTS_DTYPE)
    df_warrantys = get_files(DOWNLOAD_FOLDER,WARRANTY_FILE_NAME,columns_types=DF_WARRANTY_DTYPE)
    df_wallet = get_files(DOWNLOAD_FOLDER,WALLET_FILE_NAME,columns_types=DF_WALLET_DTYPE)
    df_devolutions = get_files(DOWNLOAD_FOLDER,DEVOLUTIONS_FILE_NAME,multiple_files=True,columns_types=DF_DEVOLUTIONS_DTYPE)
    
    
    outputs_df = [df_order_by_row,df_order_by_product,df_warrantys,df_wallet,df_devolutions]
    
    return outputs_df
    
    
def raw_data_ingestion():
    raw_data = extract_data()
    print(f"Cargando RAW Data en sus respectivas tablas")
    return raw_data
        
"Extrae los datos de la ingesta mas reciente para transformarlos y pasarlos a la capa silver"
def silver_data_extract():
    return [direct_query_data(SQL_GET_LAST_RAW_DATA.format(df,df) ) for df in RAW_TABLES]
    

def gold_silver_data_extract():
    return file_query_data(SQL_GET_GENERAL_SALES_DATA)

