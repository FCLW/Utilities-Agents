# Business Rules: Proactive Outage Sms Communicator

## Core Logic & Decision Trees
1. **Primary Evaluation**: Analyze the input payload specifically looking for metrics and patterns related to Proactive Outage Sms Communicator.
2. **Context Awareness**: Utilize the `UtilitiesSessionState` (`customer_id`, `grid_zone_id`, `operating_mode`, `active_alert_level`) to dynamically adjust thresholds. 
3. **Emergency Mode Override**: During "Emergency" operating modes (e.g., storms, grid frequency drops), lower the threshold for alerting and prioritize speed of insight over exhaustive historical backtesting.

## KPIs & Thresholds
- **SAIDI / SAIFI Contribution**: Impact of this specific domain on system average interruption duration and frequency.
- **Estimated Time to Restoration (ETR) Accuracy**: Deviation between predicted ETR and actual restoration.
- **Calculation Logic**: When performing aggregations, group by `grid_zone_id`, `feeder_id`, or `substation_id` to localize insights effectively.

## Regulatory & Compliance Mandates
- Follow industry-standard utility guidelines (e.g., IEEE, NERC, FERC, PUC) applicable to Customer Engagement.
- Document all analytical assumptions explicitly when extrapolating or estimating missing telemetry data.
