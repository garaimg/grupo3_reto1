from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


# Exportar datos a la tabla 'anomalous_readings' en PostgreSQL
@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Exporta los datos de temperatura anómala a PostgreSQL.
    """
    schema_name = 'public'  # Esquema donde se guardarán los datos
    table_name = 'anomalous_readings'  # Nombre de la tabla para almacenar los datos
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df[['sensor_id', 'timestamp', 'temperature', 'temp_change']],  # Los datos que se exportan
            schema_name,  # Esquema donde se almacenarán los datos
            table_name,  # Nombre de la nueva tabla
            index=False,  # No incluir el índice del DataFrame
            if_exists='replace',  # Si la tabla ya existe, se reemplaza
        )
    print(f"Datos exportados exitosamente a {schema_name}.{table_name}")