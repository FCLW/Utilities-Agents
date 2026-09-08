CREATE TABLE IF NOT EXISTS `utilities_production_forecasting.solar_irradiance_predictor_data` (
    timestamp_column TIMESTAMP,
    plant_id STRING,
    generation_mw FLOAT64,
    status_flag STRING,
    anomaly_score FLOAT64
)
PARTITION BY DATE(timestamp_column)
CLUSTER BY plant_id;

CREATE TABLE IF NOT EXISTS `utilities_production_forecasting.solar_irradiance_predictor_dim` (
    plant_id STRING,
    description STRING,
    region STRING,
    commission_date DATE
);
