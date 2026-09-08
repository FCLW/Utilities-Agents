CREATE TABLE IF NOT EXISTS `utilities_wholesale_trading.coal_inventory_burn_rate_advisor_data` (
    timestamp_column TIMESTAMP,
    node_id STRING,
    price_usd_mwh FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY node_id;

CREATE TABLE IF NOT EXISTS `utilities_wholesale_trading.coal_inventory_burn_rate_advisor_dim` (
    node_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
