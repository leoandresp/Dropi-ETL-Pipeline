'''
-Agregar el MAX ingestion_timestamp para las cargas delta
-Agregar la columna Update_at en las tablas silver
-Probar todo el flujo
-Pendiente de los upsert ya que estoy tomando toda la raw data y el ingestion id puede jugar en contra
-Validar lo de las garantias activas


-Se añadio la columa fecha en devoluciones ✅
-Separar el ID producto, la cantidad y la descripcion en garantias ✅
-Validar lo del producto en devoluciones
-Editar funcion para permitir que los archivos .sql puedan leer las df en memoria y no solo los de ruta
-Crear funcion para limpiar duplicados, convertir vacios en 0 si es numerico, formato fecha en df, arreglar formato fecha malo y vacios si estan en nulo o NAN en PK, que el formato UTF-8 correcto ✅
-Crear las tablas correspondientes que guardaran los datos silver 
-Crear transformacion segun las reglas de Ana Karina, para guardar en la capa gold
-Crear tabla de la capa gold
-Enviar datos a el archivo correspondiente
-Crear la configuracion Logging y el run_pipeline.py
-Crear validaciones correspondientes y test
-Orquestar con Cron
-Subir a la nube
-Los ID no pueden ser nulos
- Principios ACID
- Para las devoluciones y otros casos que valide la ultima fecha de actualizacion y apartir de esa fecha descargue


Otros cosas a aprender:
Pendiente del fomato de datos del archivo UTF-8
Pendiente de los valores que no estan duplicados pero si son identicos para la RAW data

'''

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

