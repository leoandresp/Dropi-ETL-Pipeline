import subprocess
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s - %(levelname)s - %(message)s'
)
def run_step(module_name):
    """Ejecuta un módulo y verifica su resultado"""
    logging.info(f"Iniciando {module_name}")
    try:
        result = subprocess.run(
            [r'.\dropi-extractor-venv\Scripts\python.exe', '-m', module_name],
            check=True,
            capture_output=True,
            text=True
        )
        logging.info(f"{module_name} completado exitosamente")
        logging.debug(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error en {module_name}: {e}")
        logging.error(f"Salida estándar:\n{e.stdout}")
        logging.error(f"Error estándar:\n{e.stderr}")
        return False

if __name__ == "__main__":
    steps = [
        'pipeline.run_bronze_pipeline',
        'pipeline.run_silver_pipeline',
        'pipeline.run_gold_pipeline',
    ]

    for step in steps:
        if not run_step(step):
            logging.error("Pipeline detenido por error")
            exit(1)

    logging.info("Pipeline completado exitosamente")