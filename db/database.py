import duckdb
import pandas as pd
from db.utils_db import *
from typing import Optional, Any, List, Tuple


@with_connection() # Usará DATABASE_FILE por defecto (archivo persistente)
def create_table_sql(conn: duckdb.DuckDBPyConnection, table_name: str, column_definition: str):
    """
    Crea una tabla usando una definición de columnas SQL (ej: 'id INTEGER, name VARCHAR, age INTEGER').
    """
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {column_definition}
        );
    """)
    print(f"Tabla '{table_name}' creada o ya existente.")

@with_connection()
def ingestion_data_sql_df(conn: duckdb.DuckDBPyConnection, table_name: str, df):
    """
    Inserta los dartos de una df en una tabla
    """
    
    result = conn.execute(f"INSERT INTO {table_name} SELECT * FROM df ON CONFLICT (ingestion_id) DO NOTHING")
    print(f"Se han insertado {result.rowcount} en {table_name}")

@with_connection()
def upsert_data_sql_df(conn: duckdb.DuckDBPyConnection, table_name: str, df):
    """
    Inserta los dartos de una df en una tabla
    """
    
    result = conn.execute(f"INSERT INTO {table_name} SELECT * FROM df ON CONFLICT (ID) DO UPDATE SET" )
    #print(f"Se han insertado {result.rowcount} en {table_name}")

@with_connection()
def direct_query_data(conn: duckdb.DuckDBPyConnection, query: str):
    """
    Ejecuta una consulta SELECT y devuelve los resultados como una lista de tuplas.
    """
    result = conn.execute(query).fetchdf()
    #print(f"Consulta ejecutada: {query}")
    return result

@with_connection()
def file_query_data(conn:duckdb.DuckDBPyConnection,query_path:str,df=False):
    
    #Leemos el archivo .sql
    with open(query_path,'r',encoding='utf-8') as f:
        sql_script = f.read()
    
    #Guardamos el resultado de la consulta en un df
    result = conn.execute(sql_script)
    return result.fetchdf()

# --- 3. Function to Create Table from DataFrame (Función con DataFrames) ---

@handle_exceptions
def create_table_from_df(table_name: str, df: pd.DataFrame, db_file: str):
    """
    Crea o reemplaza una tabla en DuckDB a partir de un DataFrame de Pandas.
    Gestiona su propia conexión para flexibilidad (archivo o ':memory:').
    
    Args:
        table_name (str): El nombre de la tabla a crear.
        df (pd.DataFrame): El DataFrame de Pandas.
        db_file (str): Archivo de la base de datos o ':memory:'.
    """
    # Usamos gestión de contexto para abrir y cerrar la conexión
    with duckdb.connect(database=db_file, read_only=False) as conn:
        
        # DuckDB crea la tabla automáticamente usando el DataFrame
        conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df;")
        
        print(f"Tabla '{table_name}' creada y poblada desde DataFrame en {db_file}.")
        
        # Devolvemos el número de filas para verificación
        return conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    
    