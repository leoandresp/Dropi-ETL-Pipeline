from pipeline.extract import *
from pipeline.load import *
from config import *


raw_data= extract_data(False)
load_raw_data(raw_data,RAW_TABLES)