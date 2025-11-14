from db import database as db
from pipeline import extract as e
from pipeline import load as l
import dropi_logic.sheets_api as sh
from config import *
import validations.validations as v

logging.info("Obteniendo los últimos actualizados más recientes de la capa Silver")
general_sales_df = e.gold_silver_data_extract()
v.gold_data_validation(general_sales_df)
logging.info(f"Cargando datos en {GENERAL_SALES}")
l.load_gold_data(general_sales_df)
final_general_sales_df = db.direct_query_data("SELECT * FROM GENERAL_SALES")
logging.info("Enviando datos a Hoja de cálculo")
#Pasamos los datos a la hoja de calculo correspondiente
sh.set_googleSheets(final_general_sales_df,DROPI_SHEETS_ID,SHEETS_KEY_PATH,"A2:AG",True)