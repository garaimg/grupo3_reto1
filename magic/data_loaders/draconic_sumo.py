from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def clean_database(*args, **kwargs):
    """
    Elimina las tablas 'sensor_readings_' y 'anomalous_values' por completo.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        # Eliminar las tablas por completo
        loader.execute("DROP TABLE IF EXISTS sensor_readings_;")
        loader.execute("DROP TABLE IF EXISTS anomalous_values;")

    print("Las tablas han sido eliminadas.")
