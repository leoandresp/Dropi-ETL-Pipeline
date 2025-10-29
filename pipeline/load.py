

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

def load(tables:list,datas:list):    
    for i in range(len(tables)):
        insert_data_sql_df(datas[i],tables[i])
    print("Lista la carga inicial")

