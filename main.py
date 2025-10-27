from pipeline.extract import *
from pipeline.load import *
from pipeline.transform import *
from config import *

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

print(len(silver_data))

contador = 0
for data in silver_data:
    
    data.to_excel(f"data/Aqui{contador}.xlsx")
    contador+= 1


#print(direct_query_data("SELECT * FROM PRAGMA_TABLE_INFO('RAW_Devolutions');"))
#print( direct_query_data(
#    "ALTER TABLE RAW_Wallet ALTER COLUMN \"CUENTA\" SET DATA TYPE VARCHAR")  )

