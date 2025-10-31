import db.database as db


df = db.file_query_data("db\querys\general_sales_report.sql")
print(df)
