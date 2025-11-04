from db.utils_db import *
from db.database import *
from config import *

def load_raw_data(datas:list,tables:list):    
    for i in range(len(datas)):
        
        #Saltamos al siguiente loop si no hay datos a cargar.
        if datas[i] is None:
            print(f"No hay data para cargar en {tables[i]}")
            continue
        
        ingestion_data_sql_df(tables[i],datas[i])
    print("Lista la carga inicial")

def load_silver_data(transformed_data:list):
        #Cargamos los datos nuevos a sus respectivas Tablas según corresponda:
        
        
        #Upsert de la tabla de Ordenes
        file_query_data(SQL_UPSERT_ORDERS_DATA,transformed_data[0])
        
        #Upsert de la tabla de Ordenes por producto:
        file_query_data(SQL_UPSERT_ORDERS_PRODUCT_DATA,transformed_data[1])
        
        #Reemplazamos la tabla de Garantias (Las garantias que extraemos del sistema son las que están activas)
        create_table_from_df(WARRANTYS,transformed_data[2],DATABASE_FILE)
        
        #Upsert de Wallet
        file_query_data(SQL_UPSERT_WALLET_DATA,transformed_data[3])
        
        #Upsert Devoluciones
        file_query_data(SQL_UPSERT_DEVOLUTION_DATA,transformed_data[4])

def load_gold_data(data:pd.DataFrame):
    file_query_data(SQL_UPSERT_GENERAL_SALES_DATA,data)
