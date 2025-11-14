from pipeline.extract import *
from pipeline.load import *
from config import *
import validations.validations as v


raw_data= extract_data(False)
v.raw_data_validation(raw_data)
load_raw_data(raw_data,RAW_TABLES)