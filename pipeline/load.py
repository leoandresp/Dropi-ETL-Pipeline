

''' 
    create_table_from_df("RAW_Orders",df_order_by_row,DATABASE_FILE)
    create_table_from_df("RAW_Orders_details",df_order_by_product,DATABASE_FILE)
    create_table_from_df("RAW_Warrantys",df_warrantys,DATABASE_FILE)
    create_table_from_df("RAW_Wallet",df_wallet,DATABASE_FILE)
    create_table_from_df("RAW_Devolutions",df_devolutions,DATABASE_FILE)
    
    result = direct_query_data("SELECT * FROM RAW_Orders")
    print(result)

'''
from db.utils_db import *
from db.database import *

def load_raw_data(datas:list,tables:list):    
    for i in range(len(datas)):
        insert_data_sql_df(tables[i],datas[i])
    print("Lista la carga inicial")

def load_silver_data(transformed_data):
        #Cargamos los datos nuevos a sus respectivas Tablas según corresponda:
        
        #Upsert de la tabla de Ordenes
        file_query_data(r"db\querys\upserts\orders_upsert.sql",transformed_data[0])
        
        #Upsert de la tabla de Ordenes por producto:
        file_query_data(r"db\querys\upserts\orders_product_upsert.sql",transformed_data[1])
        
        #Reemplazamos la tabla de Garantias (Las garantias que extraemos del sistema son las que están activas)
        create_table_from_df("ORDERS_PRODUCT",transformed_data[2],DATABASE_FILE)
        
        #Upsert de Wallet
        file_query_data(r"db\querys\upserts\wallet_upsert.sql",transformed_data[3])
        
        #Upsert Devoluciones
        file_query_data(r"db\querys\upserts\devolutions_upsert.sql",transformed_data[4])
