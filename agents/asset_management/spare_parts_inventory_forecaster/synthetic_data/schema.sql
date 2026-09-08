CREATE TABLE IF NOT EXISTS `utilities_asset_management.spare_parts_inventory_forecaster_data` (
    timestamp_column TIMESTAMP,
    asset_id STRING,
    health_score FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY asset_id;

CREATE TABLE IF NOT EXISTS `utilities_asset_management.spare_parts_inventory_forecaster_dim` (
    asset_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
