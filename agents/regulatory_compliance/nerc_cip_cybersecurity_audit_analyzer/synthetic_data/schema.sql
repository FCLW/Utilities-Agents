CREATE TABLE IF NOT EXISTS `utilities_regulatory_compliance.nerc_cip_cybersecurity_audit_analyzer_data` (
    timestamp_column TIMESTAMP,
    record_id STRING,
    metric_value FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY record_id;

CREATE TABLE IF NOT EXISTS `utilities_regulatory_compliance.nerc_cip_cybersecurity_audit_analyzer_dim` (
    record_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
