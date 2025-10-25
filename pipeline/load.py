'''
-Crear la funcion para cargar las tablas ya existentes en base a dataframes
-Crear funcion para limpiar duplicados, convertir vacios en 0 si es numerico, formato fecha en df, arreglar formato fecha malo y vacios si estan en nulo o NAN
-Crear las tablas correspondientes que guardaran los datos silver
-Crear transformacion segun las reglas de Ana Karina, para guardar en la capa gold
-Crear tabla de la capa gold
-Enviar datos a el archivo correspondiente
-Crear la configuracion Logging y el run_pipeline.py
-Crear validaciones correspondientes y test
-Orquestar con Cron
-Subir a la nube

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