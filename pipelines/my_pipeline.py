-- Crear tabla 'sensor_readings' para almacenar las lecturas de los sensores
CREATE TABLE IF NOT EXISTS sensor_readings_ (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    reading_timestamp TIMESTAMP NOT NULL,
    temperature FLOAT NOT NULL
);

-- Crear tabla 'anomalous_values' para almacenar las lecturas anómalas detectadas
CREATE TABLE IF NOT EXISTS anomalous_values (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    reading_timestamp TIMESTAMP NOT NULL,
    temperature FLOAT NOT NULL,
    temperature_fahrenheit FLOAT NOT NULL
);




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
        df['temperature_fahrenheit'] = (df['temperature'] * 9 / 5) + 32

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
        assert all(output['temperature_fahrenheit'] == (
                    output['temperature'] * 9 / 5) + 32), 'La conversión a Fahrenheit es incorrecta'



from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_anomalous_data(df: DataFrame, **kwargs) -> None:
    """
    Exportar las lecturas anómalas detectadas a la tabla anomalous_readings en PostgreSQL.
    """
    schema_name = 'public'  # Esquema en PostgreSQL
    table_name = 'anomalous_values'  # Tabla de destino
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # No incluir el índice de pandas en la exportación
            if_exists='append',  # Agregar las nuevas anomalías a la tabla existente
        )
