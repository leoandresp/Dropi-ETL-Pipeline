from pipeline.extract import *
from pipeline.load import *
from pipeline.transform import *
from config import *


logging.info("Extrayendo datos de la ingesta mas reciente.")
raw_data = silver_data_extract()
clean_data = clean_raw_data(raw_data)
transformed_data = silver_data_transform(clean_data)
load_silver_data(transformed_data)