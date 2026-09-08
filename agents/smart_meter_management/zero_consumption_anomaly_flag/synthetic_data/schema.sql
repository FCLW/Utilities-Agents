CREATE TABLE IF NOT EXISTS `utilities_smart_meter_management.zero_consumption_anomaly_flag_data` (
    timestamp_column TIMESTAMP,
    meter_id STRING,
    consumption_kwh FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY meter_id;

CREATE TABLE IF NOT EXISTS `utilities_smart_meter_management.zero_consumption_anomaly_flag_dim` (
    meter_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
