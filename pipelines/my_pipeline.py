from mage_ai.data_preparation.decorators import data_loader, transformer, data_exporter
import pandas as pd
from sqlalchemy import create_engine
import os

# Leer las variables de entorno
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
PG_HOST_PORT = os.getenv('PG_HOST_PORT', 5432)  # Valor por defecto 5432 si no está definido

# Construir la URL de conexión usando las variables de entorno
db_url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{PG_HOST_PORT}/{POSTGRES_DB}'
engine = create_engine(db_url)

# Paso 1: Leer datos de la tabla 'sensor_readings'
@data_loader
def load_sensor_data(*args, **kwargs):
    query = "SELECT * FROM sensor_readings;"
    df = pd.read_sql_query(query, engine)
    return df

# Paso 2: Detectar lecturas anómalas (temperatura > 35°C)
@transformer
def detect_anomalies(df, *args, **kwargs):
    anomalies = df[df['temperature'] > 35.0].copy()
    return anomalies

# Paso 3: Calcular la diferencia de temperatura con la lectura anterior
@transformer
def calculate_temp_change(df, *args, **kwargs):
    df['temp_change'] = df.groupby('sensor_id')['temperature'].diff()
    return df

# Paso 4: Guardar lecturas anómalas en la tabla 'anomalous_readings'
@data_exporter
def export_anomalies_with_change(df, *args, **kwargs):
    if df.empty:
        print("No se detectaron anomalías.")
        return

    df[['sensor_id', 'timestamp', 'temperature', 'temp_change']].to_sql(
        'anomalous_readings',
        engine,
        if_exists='append',
        index=False
    )
    print(f"{len(df)} anomalías guardadas en la base de datos.")
