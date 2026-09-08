import pandas as pd
import numpy as np
import os

def generate_data():
    np.random.seed(42)
    # Temporal boundaries anchored at 2026-08-28 00:00:00 UTC
    if "historical" == "historical":
        start_date = "2025-08-28 00:00:00"
        end_date = "2026-08-28 00:00:00"
    else:
        # Forecast 1 month
        start_date = "2026-08-28 00:00:00"
        end_date = "2026-09-28 00:00:00"
        
    # 15-minute intervals
    dates = pd.date_range(start=start_date, end=end_date, freq='15min', tz='UTC')
    
    ids = ['REC-001', 'REC-002', 'REC-003']
    records = []
    
    for eid in ids:
        df = pd.DataFrame()
        df['timestamp_column'] = dates
        df['record_id'] = eid
        
        # Base value
        base_val = np.random.uniform(50, 150)
        
        # Diurnal pattern (sine wave)
        diurnal = np.sin((df['timestamp_column'].dt.hour + df['timestamp_column'].dt.minute/60) * (2 * np.pi / 24)) * 20
        
        # Seasonality (higher in summer: June-August)
        # Month 6, 7, 8
        is_summer = df['timestamp_column'].dt.month.isin([6, 7, 8])
        seasonality = np.where(is_summer, 30, 0)
        
        df['metric_value'] = base_val + diurnal + seasonality + np.random.normal(0, 2, len(df))
        df['status_flag'] = 'NORMAL'
        df['anomaly_score'] = np.random.uniform(0.01, 0.05, len(df))
        
        records.append(df)
        
    final_df = pd.concat(records, ignore_index=True)
    
    # Inject exactly 5-10 specific anomalies
    num_anomalies = np.random.randint(5, 11)
    anomaly_indices = np.random.choice(final_df.index, num_anomalies, replace=False)
    
    for idx in anomaly_indices:
        final_df.loc[idx, 'metric_value'] *= np.random.choice([0.0, 3.5, 5.0]) # Massive drop or spike
        final_df.loc[idx, 'status_flag'] = 'ANOMALY'
        final_df.loc[idx, 'anomaly_score'] = np.random.uniform(0.85, 0.99)
        
    # Specific agent rules overrides
    agent_id = "puc_rate_case_testimony_drafter"
    if agent_id == "transformer_dga_health_monitor":
        # Inject trend starting July 2026
        mask = final_df['timestamp_column'] >= "2026-07-01 00:00:00+00:00"
        final_df.loc[mask, 'metric_value'] += np.linspace(0, 100, mask.sum())
    elif agent_id == "solar_irradiance_predictor":
        # 3-day cloud cover event early Sept 2026
        mask = (final_df['timestamp_column'] >= "2026-09-02") & (final_df['timestamp_column'] <= "2026-09-05")
        final_df.loc[mask, 'metric_value'] *= 0.2
    elif agent_id == "scada_breaker_trip_correlator":
        # Cascading fault on 2026-08-25
        fault_time = pd.to_datetime("2026-08-25 14:00:00+00:00")
        mask = (final_df['timestamp_column'] == fault_time)
        final_df.loc[mask, 'metric_value'] = 0.0
        final_df.loc[mask, 'status_flag'] = 'CRITICAL_TRIP'
    elif agent_id == "day_ahead_lmp_forecaster":
        mask = final_df['timestamp_column'].dt.month == 9
        final_df.loc[mask, 'metric_value'] += 15.0 # Premium
    elif agent_id == "ami_interval_data_vee_processor":
        mask = (final_df['record_id'] == "AMI-9042") & (final_df['timestamp_column'] >= "2026-08-15 10:00:00+00:00") & (final_df['timestamp_column'] <= "2026-08-15 14:00:00+00:00")
        final_df.loc[mask, 'metric_value'] = 0.0
        final_df.loc[mask, 'status_flag'] = 'MISSING_VEE'

    out_path = os.path.join(os.path.dirname(__file__), "mock_records.csv")
    final_df.to_csv(out_path, index=False)
    print(f"Generated {len(final_df)} records to {out_path}")

if __name__ == "__main__":
    generate_data()
