# Business Rules: Ev Charging Station Maintenance Tracker

## Core Logic & Decision Trees
1. **Primary Evaluation**: Analyze the input payload specifically looking for metrics and patterns related to Ev Charging Station Maintenance Tracker.
2. **Context Awareness**: Utilize the `UtilitiesSessionState` (`customer_id`, `grid_zone_id`, `operating_mode`, `active_alert_level`) to dynamically adjust thresholds. 
3. **Emergency Mode Override**: During "Emergency" operating modes (e.g., storms, grid frequency drops), lower the threshold for alerting and prioritize speed of insight over exhaustive historical backtesting.

## KPIs & Thresholds
- **Asset Health Index (AHI)**: Composite score indicating probability of failure.
- **Remaining Useful Life (RUL)**: Time until the asset requires complete replacement.
- **Mean Absolute Percentage Error (MAPE)**: Must maintain < 5% error on predictions.
- **Confidence Interval (95%)**: Upper and lower bounds for probabilistic forecasting.
- **Calculation Logic**: When performing aggregations, group by `grid_zone_id`, `feeder_id`, or `substation_id` to localize insights effectively.

## Regulatory & Compliance Mandates
- Follow industry-standard utility guidelines (e.g., IEEE, NERC, FERC, PUC) applicable to Asset Management.
- Document all analytical assumptions explicitly when extrapolating or estimating missing telemetry data.
