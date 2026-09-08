CREATE TABLE IF NOT EXISTS `utilities_wholesale_trading.portfolio_value_at_risk_analyzer_data` (
    timestamp_column TIMESTAMP,
    node_id STRING,
    price_usd_mwh FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY node_id;

CREATE TABLE IF NOT EXISTS `utilities_wholesale_trading.portfolio_value_at_risk_analyzer_dim` (
    node_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
