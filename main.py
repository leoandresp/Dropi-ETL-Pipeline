import subprocess
import logging
import sys 
import os  
from datetime import datetime
from config import *





logging.info(f"Usando ejecutable de Python: {PYTHON_EXECUTABLE}")

# --- Función Principal Modificada ---

def run_step(module_name):
    logging.info(f"Iniciando {module_name}")
    try:
        process = subprocess.Popen(
            [PYTHON_EXECUTABLE, '-m', module_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Leer y loguear línea por línea en tiempo real
        for line in iter(process.stdout.readline, ''):
            if line:
                logging.info(line.strip())

        process.stdout.close()
        return_code = process.wait()
        if return_code != 0:
            logging.error(f"Error en {module_name}, código de salida {return_code}")
            return False

        logging.info(f"✅ {module_name} completado exitosamente")
        return True

    except FileNotFoundError:
        logging.error(f"Error: El ejecutable de Python '{PYTHON_EXECUTABLE}' no fue encontrado.")
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