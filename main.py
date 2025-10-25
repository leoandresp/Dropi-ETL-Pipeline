from pipeline.extract import *
from pipeline.load import *
from config import *

raw_data = extract_data()
load(raw_data,RAW_LOAD)
print(raw_data[1].loc[3])


