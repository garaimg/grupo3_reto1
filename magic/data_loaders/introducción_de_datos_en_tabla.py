import random
from datetime import datetime, timedelta
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data(*args, **kwargs):
    """
    Genera e inserta lecturas aleatorias en la tabla sensor_readings_ de PostgreSQL.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    # Generar datos aleatorios de sensores en un DataFrame
    data = []
    for _ in range(10):  # Insertar 10 registros
        sensor_id = f"sensor_{random.randint(1, 6)}"
        timestamp = datetime.now() - timedelta(minutes=random.randint(0, 300))
        temperature = round(random.uniform(20, 40), 2)

        data.append([sensor_id, timestamp, temperature])

    df = DataFrame(data, columns=['sensor_id', 'reading_timestamp', 'temperature'])

    # Conectar a PostgreSQL y exportar los datos
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            'public',  # Esquema en PostgreSQL
            'sensor_readings_',  # Tabla de destino
            if_exists='append',  # Agregar nuevas filas sin sobrescribir
            index=False  # No incluir el índice de Pandas en la exportación
        )

    print("Datos insertados correctamente en sensor_readings_.")
    print(df)