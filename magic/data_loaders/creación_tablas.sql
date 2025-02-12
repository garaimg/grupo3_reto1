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

