import subprocess
import logging
import sys 
import os  
from datetime import datetime
from config import *





logging.info(f"Usando ejecutable de Python: {PYTHON_EXECUTABLE}")

# --- Función Principal Modificada ---

def run_step(module_name):
    """Ejecuta un módulo y verifica su resultado"""
    logging.info(f"Iniciando {module_name}")
    try:
        result = subprocess.run(
            [PYTHON_EXECUTABLE, '-m', module_name],
            check=True,
            capture_output=True,
            text=True
        )
        logging.info(f"✅ {module_name} completado exitosamente")
        logging.debug(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error en {module_name}: {e}")
        logging.error(f"Salida estándar:\n{e.stdout}")
        logging.error(f"Error estándar:\n{e.stderr}")
        return False
    except FileNotFoundError:
        logging.error(f"Error: El ejecutable de Python '{PYTHON_EXECUTABLE}' no fue encontrado.")
        logging.error("Asegúrate de que el entorno virtual esté creado y activado correctamente.")
        return False


if __name__ == "__main__":
    steps = [
        'pipeline.run_bronze_pipeline',
        'pipeline.run_silver_pipeline',
        'pipeline.run_gold_pipeline',
    ]

    logging.info(f"Iniciando Pipeline con {len(steps)} pasos.")
    for step in steps:
        if not run_step(step):
            logging.critical("Pipeline detenido por error en el paso anterior.")
            exit(1)

    logging.info("Pipeline completado exitosamente")