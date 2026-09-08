CREATE TABLE IF NOT EXISTS `utilities_production_forecasting.residential_load_curve_forecaster_data` (
    timestamp_column TIMESTAMP,
    plant_id STRING,
    generation_mw FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY plant_id;

CREATE TABLE IF NOT EXISTS `utilities_production_forecasting.residential_load_curve_forecaster_dim` (
    plant_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
