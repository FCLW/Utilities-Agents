# Business Rules: High Bill Spike Anomaly Flag

## Core Logic & Decision Trees
1. **Primary Evaluation**: Analyze the input payload specifically looking for metrics and patterns related to High Bill Spike Anomaly Flag.
2. **Context Awareness**: Utilize the `UtilitiesSessionState` (`customer_id`, `grid_zone_id`, `operating_mode`, `active_alert_level`) to dynamically adjust thresholds. 
3. **Emergency Mode Override**: During "Emergency" operating modes (e.g., storms, grid frequency drops), lower the threshold for alerting and prioritize speed of insight over exhaustive historical backtesting.

## KPIs & Thresholds
- **Revenue Leakage**: Detected anomalies in unbilled or underbilled intervals.
- **VEE Success Rate**: Percentage of interval data successfully validated, estimated, and edited.
- **Calculation Logic**: When performing aggregations, group by `grid_zone_id`, `feeder_id`, or `substation_id` to localize insights effectively.

## Regulatory & Compliance Mandates
- Follow industry-standard utility guidelines (e.g., IEEE, NERC, FERC, PUC) applicable to Billing And Invoicing.
- Document all analytical assumptions explicitly when extrapolating or estimating missing telemetry data.
