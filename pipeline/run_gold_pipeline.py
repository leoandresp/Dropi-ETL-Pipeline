from db import database as db
from pipeline import extract as e
from pipeline import load as l
import dropi_logic.sheets_api as sh
from config import *


general_sales_df = e.gold_silver_data_extract()
l.load_gold_data(general_sales_df)
final_general_sales_df = db.direct_query_data("SELECT * FROM GENERAL_SALES")
#Pasamos los datos a la hoja de calculo correspondiente
sh.set_googleSheets(final_general_sales_df,DROPI_SHEETS_ID,SHEETS_KEY_PATH,"A2:AG")