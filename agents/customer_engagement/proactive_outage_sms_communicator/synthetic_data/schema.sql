CREATE TABLE IF NOT EXISTS `utilities_customer_engagement.proactive_outage_sms_communicator_data` (
    timestamp_column TIMESTAMP,
    customer_id STRING,
    amount_billed FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY customer_id;

CREATE TABLE IF NOT EXISTS `utilities_customer_engagement.proactive_outage_sms_communicator_dim` (
    customer_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
