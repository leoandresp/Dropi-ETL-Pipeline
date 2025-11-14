"""
Script de inicialización de tablas para DuckDB.
Crea todas las tablas necesarias si es la primera vez que se ejecuta el proyecto.
"""
import duckdb
from pathlib import Path
from config import DATABASE_FILE, DB_DIR
import logging

# Mapeo de nombres de tablas a sus archivos SQL de creación
CREATE_TABLES_FILES = {
    # Tablas RAW (Bronze Layer)
    "RAW_ORDERS": "create_RAW_ORDERS.sql",
    "RAW_ORDERS_PRODUCTS": "create_RAW_ORDERS_PRODUCTS.sql",
    "RAW_WARRANTYS": "create_RAW_WARRANTYS.sql",
    "RAW_WALLET": "create_RAW_WALLET.sql",
    "RAW_DEVOLUTIONS": "create_RAW_DEVOLUTIONS.sql",
    
    # Tablas finales (Silver/Gold Layer)
    "ORDERS": "create_order_table.sql",
    "ORDERS_PRODUCT": "create_orders_products_table.sql",
    "WARRANTYS": "create_warrantys_table.sql",
    "WALLET": "create_wallet_table.sql",
    "DEVOLUTIONS": "create_devolution_table.sql",
    "GENERAL_SALES": "create_general_sales.sql"
}

CREATE_TABLES_DIR = DB_DIR / "querys" / "create_tables"


def table_exists(conn: duckdb.DuckDBPyConnection, table_name: str) -> bool:
    """
    Verifica si una tabla existe en la base de datos.
    
    Args:
        conn: Conexión a DuckDB
        table_name: Nombre de la tabla a verificar
        
    Returns:
        True si la tabla existe, False en caso contrario
    """
    try:
        # Intentar hacer una consulta simple a la tabla
        # Si la tabla no existe, lanzará una excepción
        conn.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
        return True
    except Exception:
        # Si hay error, la tabla no existe
        return False


def create_table_from_file(conn: duckdb.DuckDBPyConnection, sql_file: Path):
    """
    Crea una tabla ejecutando un archivo SQL.
    
    Args:
        conn: Conexión a DuckDB
        sql_file: Ruta al archivo SQL con el CREATE TABLE
    """
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        conn.execute(sql_script)
        logging.info(f"✅ Tabla creada desde {sql_file.name}")
    except Exception as e:
        logging.error(f"❌ Error al crear tabla desde {sql_file.name}: {e}")
        raise


def init_database():
    """
    Inicializa la base de datos creando todas las tablas necesarias si no existen.
    La base de datos Oferfly.duckdb se crea automáticamente en la carpeta db/ si no existe.
    """
    # Asegurar que el directorio de la base de datos existe
    db_path = Path(DATABASE_FILE)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Conectar a la base de datos (se crea automáticamente si no existe)
    conn = duckdb.connect(database=DATABASE_FILE, read_only=False)
    
    try:
        logging.info("🔍 Verificando existencia de tablas...")
        
        tables_to_create = []
        tables_existing = []
        
        # Verificar qué tablas existen y cuáles faltan
        for table_name, sql_file in CREATE_TABLES_FILES.items():
            if table_exists(conn, table_name):
                tables_existing.append(table_name)
            else:
                tables_to_create.append((table_name, sql_file))
        
        if tables_existing:
            logging.info(f"📊 Tablas existentes ({len(tables_existing)}): {', '.join(tables_existing)}")
        
        if not tables_to_create:
            logging.info("✅ Todas las tablas ya existen. No se requiere inicialización.")
            return
        
        logging.info(f"🔨 Creando {len(tables_to_create)} tabla(s) faltante(s)...")
        
        # Crear las tablas faltantes
        for table_name, sql_file in tables_to_create:
            sql_path = CREATE_TABLES_DIR / sql_file
            if not sql_path.exists():
                logging.warning(f"⚠️  Archivo SQL no encontrado: {sql_path}")
                continue
            
            logging.info(f"📝 Creando tabla: {table_name}")
            create_table_from_file(conn, sql_path)
        
        conn.commit()
        logging.info("✅ Inicialización de base de datos completada exitosamente.")
        
    except Exception as e:
        logging.error(f"❌ Error durante la inicialización: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    # Configurar logging si se ejecuta directamente
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    init_database()

