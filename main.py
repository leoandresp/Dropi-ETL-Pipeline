from pipeline.extract import *
from pipeline.load import *
from pipeline.transform import *
from config import *
import pandas as pd
'''

raw_data = extract_data()
load(raw_data,RAW_LOAD)

dict_dates = {
    0: ["FECHA DE REPORTE","FECHA","FECHA DE NOVEDAD","FECHA DE SOLUCIÓN","FECHA DE ÚLTIMO MOVIMIENTO","FECHA GENERACION DE GUIA"],
    1: ["FECHA DE REPORTE","FECHA","FECHA DE NOVEDAD","FECHA DE SOLUCIÓN","FECHA DE ÚLTIMO MOVIMIENTO","FECHA GENERACION DE GUIA"],
    2: ["FECHA DE CREACION"],
    3:["FECHA"],
    4: []
}

#Hay columnas que me trae en 0 cuando deberia estar vacio
silver_data = clean_list_of_dataframes(raw_data,dict_dates)

#Separamos las columnas de Productos de Garantia para hacerla un ID Producto y Descripcion de Producto
silver_data[2] = split_column(silver_data[2],"PRODUCTO","-",["ID PRODUCTO","DESCRIPCION PRODUCTO"])
#Cambios el nombre de la Columna ID Garatia por ID
silver_data[2] = renames_columns(silver_data[2],{"ID GARANTIA":"ID"})

print(len(silver_data))

contador = 0
for data in silver_data:
    
    data.to_excel(f"data/Aqui{contador}.xlsx")
    contador+= 1


#print(direct_query_data("SELECT * FROM PRAGMA_TABLE_INFO('RAW_Devolutions');"))

print( direct_query_data(
    f"ALTER TABLE RAW_Orders_details ADD COLUMN \"row_number\"  INT")  )
print( direct_query_data(
    f"ALTER TABLE Orders ADD COLUMN \"row_number\" BIGINT")  )




df= direct_query_data("DESCRIBE RAW_Orders")
print(df)
'''
df= direct_query_data("SELECT * FROM Orders")
print(df)
#df.to_excel("data\Aqui0.xlsx")
#print( direct_query_data("DESCRIBE Orders") )
#print(file_query_data("db\querys\create_devolution_table.sql"))
