import os
from dotenv import load_dotenv

#Cargamos las variables del archivo .env
load_dotenv()

#CREDENCIALES
DROPI_USER = os.environ.get('DROPI_USER')
DROPI_PASS = os.environ.get('DROPI_PASS')
