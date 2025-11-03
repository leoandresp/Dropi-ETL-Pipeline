from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import time
import os
import sys
import pandas as pd

def set_googleSheets(df: pd.DataFrame,sheets_id:str,path_key:str,range):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    ruta_exe = os.path.abspath(sys.argv[0])
    directorio_actual = os.path.dirname(ruta_exe)
    ruta_key = os.path.join(directorio_actual, path_key)
    SPREADSHEET_ID = sheets_id
    
    try:
        creds = service_account.Credentials.from_service_account_file(ruta_key, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        # Borra todos los datos de la hoja excepto la primera fila (encabezado)
        clear_range = range
        sheet.values().clear(
            spreadsheetId=SPREADSHEET_ID, 
            range=clear_range, 
            body={}
        ).execute()
        
        # Función para procesar cada elemento
        def procesar_valor(x):
            # 1. Si el valor es nulo (NaN o NaT), retorna cadena vacía
            if pd.isna(x):
                return ""
            
            # 2. Si es Timestamp (Fecha y Hora), lo formatea
            if isinstance(x, pd.Timestamp):
                return x.strftime('%Y-%m-%d %H:%M:%S')
            
            # 3. AÑADIDO: Si es un objeto de tiempo puro (datetime.time), lo formatea
            if isinstance(x, time):
                return str(x) # Convierte el objeto time (ej: 08:30:00) a string
                # Alternativamente: return x.strftime('%H:%M:%S')
                
            # 4. Retorna el valor convertido a string para asegurar compatibilidad
            return str(x)
        
        # Aplica la función a todo el DataFrame
        df_procesado = df.applymap(procesar_valor)
        
        # Convierte el DataFrame a lista de listas
        values = df_procesado.values.tolist()
        
        # Actualiza el rango empezando en A2
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='A2',
            valueInputOption='USER_ENTERED',
            body={'values': values}
        ).execute()
        
        if 'updatedCells' in result:
            print("Datos enviados de forma exitosa", "Información")
        else:
            raise Exception("No se pudo obtener información sobre las celdas actualizadas")
    
    except FileNotFoundError as e:
        print("Error al leer el archivo de clave:", str(e))
    
    except Exception as e:
        print(f'Ocurrió un error al insertar los datos en Google Sheets: {str(e)}', "Error")