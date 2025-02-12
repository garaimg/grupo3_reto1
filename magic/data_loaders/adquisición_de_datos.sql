-- Crear tabla 'sensor_readings' para almacenar las lecturas de los sensores
CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperature FLOAT NOT NULL
);

-- Insertar datos de ejemplo en 'sensor_readings'
INSERT INTO sensor_readings (sensor_id, timestamp, temperature)
VALUES
    ('sensor_1', NOW() - INTERVAL '5 hours', 22.5),
    ('sensor_2', NOW() - INTERVAL '4 hours', 36.7), -- Anómala
    ('sensor_3', NOW() - INTERVAL '3 hours', 28.4),
    ('sensor_1', NOW() - INTERVAL '2 hours', 37.2), -- Anómala
    ('sensor_4', NOW() - INTERVAL '1 hour', 25.1),
    ('sensor_2', NOW(), 39.5); -- Anómala

-- Crear tabla 'anomalous_readings' para almacenar las lecturas anómalas detectadas
CREATE TABLE IF NOT EXISTS anomalous_readings (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperature FLOAT NOT NULL,
    temp_change FLOAT
);

