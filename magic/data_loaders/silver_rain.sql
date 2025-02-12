-- Vaciar la tabla sensor_readings_ y reiniciar los contadores de ID
TRUNCATE TABLE sensor_readings_ RESTART IDENTITY;

-- Vaciar la tabla anomalous_values y reiniciar los contadores de ID
TRUNCATE TABLE anomalous_values RESTART IDENTITY;

-- Docs: https://docs.mage.ai/guides/sql-blocks
