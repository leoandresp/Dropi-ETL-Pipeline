import db.database as db


df_query = db.file_query_data(r"db\querys\general_sales_report.sql")

#print(df_query)

#Cargamos los datos en la tabla
db.file_query_data(r"db\querys\upserts\general_sales_upsert.sql",df_query)

