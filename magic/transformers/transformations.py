from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
from pandas import DataFrame

# Importamos los decoradores de Mage si no están definidos
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


# Transformación para detectar lecturas anómalas (temperatura > 35°C)
@transformer
def detect_anomalies(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Detecta lecturas anómalas (temperatura > 35°C).
    """
    anomalies = df[df['temperature'] > 35.0].copy()
    return anomalies

# Otra transformación: calcular la diferencia de temperatura entre lecturas consecutivas
@transformer
def calculate_temp_change(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Calcula la diferencia de temperatura con la lectura anterior por sensor.
    """
    df['temp_change'] = df.groupby('sensor_id')['temperature'].diff()
    return df
