from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform_sensor_data(*args, **kwargs) -> DataFrame:
    """
    Cargar datos de PostgreSQL, detectar anomalías y calcular la temperatura en grados Fahrenheit.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    # Consulta para cargar los datos de la tabla sensor_readings
    query = 'SELECT * FROM sensor_readings_ ORDER BY sensor_id, reading_timestamp;'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        df = loader.load(query)

    # Calcular temperatura en Fahrenheit antes de filtrar
    df['temperature_fahrenheit'] = (df['temperature'] * 9/5) + 32

    # Detectar lecturas anómalas
    df_anomalous = df[df['temperature'] > 30].copy()

    print(df_anomalous.columns)  # Verifica que la columna temperature_fahrenheit está presente

    return df_anomalous



@test
def test_output(output, *args) -> None:
    """
    Verificación del resultado de la transformación.
    """
    assert output is not None, 'El resultado de la transformación es None'
    assert not output.empty, 'No se detectaron lecturas anómalas'
    assert all(output['temperature'] > 30), 'Existen lecturas no anómalas en el resultado'
    assert 'temperature_fahrenheit' in output.columns, 'La columna de temperatura en Fahrenheit no fue generada'
    assert all(output['temperature_fahrenheit'] == (output['temperature'] * 9/5) + 32), 'La conversión a Fahrenheit es incorrecta'
