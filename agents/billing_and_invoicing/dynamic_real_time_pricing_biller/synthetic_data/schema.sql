CREATE TABLE IF NOT EXISTS `utilities_billing_and_invoicing.dynamic_real_time_pricing_biller_data` (
    timestamp_column TIMESTAMP,
    customer_id STRING,
    amount_billed FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY customer_id;

CREATE TABLE IF NOT EXISTS `utilities_billing_and_invoicing.dynamic_real_time_pricing_biller_dim` (
    customer_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
