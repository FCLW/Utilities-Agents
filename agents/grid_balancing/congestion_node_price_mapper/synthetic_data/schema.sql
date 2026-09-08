CREATE TABLE IF NOT EXISTS `utilities_grid_balancing.congestion_node_price_mapper_data` (
    timestamp_column TIMESTAMP,
    node_id STRING,
    frequency_hz FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY node_id;

CREATE TABLE IF NOT EXISTS `utilities_grid_balancing.congestion_node_price_mapper_dim` (
    node_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
