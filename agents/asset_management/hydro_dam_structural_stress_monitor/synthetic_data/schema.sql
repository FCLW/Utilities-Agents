CREATE TABLE IF NOT EXISTS `utilities_asset_management.hydro_dam_structural_stress_monitor_data` (
    timestamp_column TIMESTAMP,
    asset_id STRING,
    health_score FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY asset_id;

CREATE TABLE IF NOT EXISTS `utilities_asset_management.hydro_dam_structural_stress_monitor_dim` (
    asset_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
