CREATE TABLE IF NOT EXISTS `utilities_grid_operations.flisr_switching_simulator_data` (
    timestamp_column TIMESTAMP,
    feeder_id STRING,
    voltage_kv FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY feeder_id;

CREATE TABLE IF NOT EXISTS `utilities_grid_operations.flisr_switching_simulator_dim` (
    feeder_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
