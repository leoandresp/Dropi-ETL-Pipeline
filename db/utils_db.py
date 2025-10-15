import duckdb
import functools
from config import DATABASE_FILE

def handle_exceptions(func):
    """
    Decorador para envolver funciones de DB y manejar excepciones de DuckDB y generales.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except duckdb.Error as e:
            print(f"❌ Error de DuckDB en '{func.__name__}': {e}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado en '{func.__name__}': {e}")
            return None
    return wrapper

def with_connection(db_file: str = DATABASE_FILE, autocommit: bool = True):
    """
    Decorador que abre y cierra la conexión DuckDB automáticamente.
    La función decorada debe aceptar 'conn' como su primer argumento.
    Acepta el path del archivo o ':memory:' para una DB temporal.
    """
    def decorator(func):
        @wraps(func)
        @handle_exceptions
        def wrapper(*args, **kwargs):
            conn = None
            db_name = "MEMORIA" if db_file == ":memory:" else db_file
            try:
                # 1. Establecer conexión
                conn = duckdb.connect(database=db_file, read_only=False)
                #print(f"⚙️ Conexión abierta a {db_name} para '{func.__name__}'") # Comentario opcional de debug
                
                # 2. Ejecutar la función, inyectando 'conn'
                result = func(conn, *args, **kwargs)

                # 3. Commit automático para operaciones de escritura
                if autocommit:
                    conn.commit()

                return result
                
            finally:
                # 4. Cerrar conexión
                if conn:
                    conn.close()
                    #print(f"⚙️ Conexión cerrada después de '{func.__name__}'") # Comentario opcional de debug
        return wrapper
    return decorator
