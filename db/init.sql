CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50),
    timestamp TIMESTAMP,
    temperature FLOAT
);

-- Insertamos datos de prueba (algunas temperaturas normales y otras anómalas)
INSERT INTO sensor_readings (sensor_id, timestamp, temperature)
VALUES
    ('sensor_1', NOW() - INTERVAL '3 hours', 22.5),
    ('sensor_2', NOW() - INTERVAL '2 hours', 36.7), -- Anómala
    ('sensor_3', NOW() - INTERVAL '1 hour', 28.4),
    ('sensor_1', NOW(), 37.2); -- Anómala

-- Tabla para almacenar temperaturas anómalas
CREATE TABLE IF NOT EXISTS anomalous_readings (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50),
    timestamp TIMESTAMP,
    temperature FLOAT
);
