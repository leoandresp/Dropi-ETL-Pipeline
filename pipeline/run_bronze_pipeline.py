from pipeline.extract import *
from pipeline.load import *
from config import *


raw_data= raw_data_ingestion()
load_raw_data(raw_data,RAW_LOAD)