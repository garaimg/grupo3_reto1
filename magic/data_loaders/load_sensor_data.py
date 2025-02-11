from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
import pandas as pd

# Si no están definidos, importamos los decoradores de Mage
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data(*args, **kwargs):
    # Ejecutar el script de Python para insertar datos aleatorios
    run(['python', 'scripts/insert_random_data.py'])
    print("Datos aleatorios insertados con éxito.")
    
# Cargar datos de la tabla 'sensor_readings' desde PostgreSQL
@data_loader
def load_sensor_data(*args, **kwargs):
    """
    Carga los datos de la tabla 'sensor_readings' en PostgreSQL.
    """
    query = 'SELECT * FROM sensor_readings;'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)
