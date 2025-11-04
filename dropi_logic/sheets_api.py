from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import time
import os
import sys
import pandas as pd
from dropi_logic.utils import *

#
@try_except_sheets
def set_googleSheets(
    df: pd.DataFrame,
    sheets_id: str,
    path_key: str,
    range: str,
    clear_sheet: bool = True
):
    """
    Sube un DataFrame a Google Sheets.
    - Si clear_sheet=True: borra los datos antes de insertar.
    - Si clear_sheet=False: agrega los datos al final automáticamente.
    """

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    path_exe = os.path.abspath(sys.argv[0])
    current_directory = os.path.dirname(path_exe)
    path_key = os.path.join(current_directory, path_key)
    SPREADSHEET_ID = sheets_id

    creds = service_account.Credentials.from_service_account_file(path_key, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    df_procesado = df.map(procesar_valor)
    values = df_procesado.values.tolist()

    if clear_sheet:
        #Limpia el rango
        sheet.values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range=range,
            body={}
        ).execute()
        
        #Inserta desde A2
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range,
            valueInputOption='USER_ENTERED',
            body={'values': values}
        ).execute()
        affected_rows = result.get('updatedRows', 0)
        
    else:
        #Agrega automáticamente al final
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=range,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': values}
        ).execute()
        affected_rows = result.get('updates', {}).get('updatedRows', 0)

    if affected_rows > 0:
        action = "borrados y cargados" if clear_sheet else "agregados al final"
        print(f"✅ {affected_rows} filas {action} de forma exitosa")
    else:
        raise Exception(f"No se pudo obtener información sobre la operación realizada. Respuesta: {result}")
        
        
# Función Auxiliar para adaptar cada elemento al formato aceptado por google Sheets
def procesar_valor(x):
    # Si el valor es nulo (NaN o NaT), retorna cadena vacía
    if pd.isna(x):
        return ""
    
    # Si es Timestamp (Fecha y Hora), lo formatea
    if isinstance(x, pd.Timestamp):
        return x.strftime('%Y-%m-%d %H:%M:%S')
    
    #Si es un objeto de tiempo puro (datetime.time), lo formatea
    if isinstance(x, time):
        return str(x) 
        
    return str(x)