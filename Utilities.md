# Enterprise Utilities Agent Fleet Specification

This document defines the architectural principles, operational standards, and full agent portfolio for the Google Cloud Energy & Utilities Multi-Agent Fleet built with Google ADK (`google-adk[gcp]>=2.0.0`), BigQuery, and FastAPI.

---

### Core Architecture & MAS Operating Principles

1. **The Global Orchestrator Pattern:** 
   - A single, top-level **`utilities_master_orchestrator`** agent resides in `agents/master_orchestrator/`. 
   - This agent acts as the universal entry point, handling global intent classification, dynamic task decomposition, and dispatching tasks to specialized sub-domain agents via the Agent-to-Agent (A2A) protocol.

2. **Strict Single-Purpose Scope:**
   - Every agent enforces the Single Responsibility Principle: Atomic, focused tasks (e.g., separating solar generation prediction from wholesale bidding curve optimization).
   - The fleet spans 113 production agents across 11 sub-domains, covering the complete operational footprint of a modern energy & water utility.

3. **Standardized Agent Package & Sub-Agent Structure (Worker + Critic):** 
   - Every specialized agent contains:
     - `agent.py`: Declarative ADK root agent assembling modular prompts.
     - `manifest.yaml`: Metadata, domain, tools, and BigQuery table dependencies.
     - `instructions/`: Modular prompts (`persona.md`, `business_rules.md`, `output_format.md`, `safety_guardrails.md`, `sample_prompts.yaml`).
     - `tools/`: Specialized tools (`bigquery_tool.py`, `search_tool.py`, `visualizer.py`, `delegation_tool.py`).
     - `sub_agents/`:
       - **Execution Sub-Agent (`execution_agent.py`)**: Executes domain logic, scenario modeling, and read-only BigQuery SQL queries.
       - **Critic Sub-Agent (`critic_agent.py`)**: Independent evaluator gatekeeper. Intercepts execution output, verifies adherence to `safety_guardrails.md`, checks for hallucinations or PII leaks, and formats final markdown tables before returning control.
     - `synthetic_data/`: BigQuery DDL schema (`schema.sql`), seed data (`seed_data.sql`), and sample CSV fixtures (`mock_records.csv`).
     - `tests/`: Golden evaluation dataset (`golden-dataset.json`), metric thresholds (`eval_config.yaml`), and integration/unit tests.

---

### Fleet Roster: Global Orchestrator & 10 Industry Sub-Domains (113 Agents Total)

#### Master Orchestrator (1 Agent)
- **`utilities_master_orchestrator`** (Autonomous): Universal entrypoint, natural language intent triage, multi-agent decomposition, and A2A dispatching.

#### 1. Asset Management (14 Agents)
- **`capital_replacement_simulator`** (Advisory): Simulates asset replacement schedules based on age, degradation curves, and capital budget constraints.
- **`circuit_breaker_wear_analyzer`** (Autonomous): Analyzes trip telemetry and contact wear indices to predict remaining useful life (RUL).
- **`derms_capacity_optimizer`** (Advisory): Models distributed energy resource management system (DERMS) hosting capacity and curtailment.
- **`drone_inspection_image_processor`** (Autonomous): Evaluates drone visual/thermal telemetry for transmission line and insulator defects.
- **`ev_charging_station_maintenance_tracker`** (Autonomous): Monitors EVSE uptime, connector thermals, and OCPP fault codes for proactive maintenance.
- **`hydro_dam_structural_stress_monitor`** (Autonomous): Analyzes piezometer, tiltmeter, and acoustic sensors to monitor hydroelectric dam structural integrity.
- **`maintenance_fleet_dispatch_scheduler`** (Advisory): Optimizes crew dispatch routes, tooling, and priority work orders across utility field depots.
- **`smart_grid_sensor_health_monitor`** (Autonomous): Tracks telemetry latency, heartbeat loss, and calibration drift across grid-edge IoT sensors.
- **`solar_inverter_string_fault_detector`** (Autonomous): Identifies string-level MPPT clipping, DC ground faults, and diode failures across PV arrays.
- **`spare_parts_inventory_forecaster`** (Advisory): Forecasts critical substation transformer, breaker, and switchgear component inventories.
- **`substation_battery_health_tracker`** (Autonomous): Tracks DC station battery bank internal resistance, temperature, and float voltage health.
- **`transformer_dga_health_monitor`** (Autonomous): Computes Duval Triangle and Roger's ratios on dissolved gas analysis (DGA) to detect transformer arcing and overheating.
- **`transmission_tower_corrosion_analyzer`** (Autonomous): Correlates atmospheric salinity, age, and coating inspection data to forecast structural corrosion.
- **`wind_turbine_gearbox_vibration_analyzer`** (Autonomous): Analyzes high-frequency accelerometer spectrograms to detect turbine planetary gear and bearing wear.

#### 2. Production Forecasting (12 Agents)
- **`commercial_load_curve_forecaster`** (Autonomous): Forecasts commercial HVAC and retail power demand curves using occupancy and weather data.
- **`ev_charging_load_spike_predictor`** (Autonomous): Predicts localized EV fast-charging cluster demand spikes on feeder circuits.
- **`extreme_weather_anomaly_alert_bot`** (Autonomous): Ingests NOAA/ECMWF weather feeds to flag severe temperature, freeze, or heatwave anomalies.
- **`geothermal_output_forecaster`** (Autonomous): Forecasts geothermal steam enthalpy, brine flow rates, and net MW output.
- **`hydro_inflow_snowpack_estimator`** (Autonomous): Predicts seasonal reservoir watershed inflow from SNOTEL snowpack and runoff data.
- **`industrial_load_curve_forecaster`** (Autonomous): Forecasts energy demand for high-load industrial plants, smelters, and manufacturing facilities.
- **`microgrid_generation_forecaster`** (Autonomous): Forecasts islanded and grid-connected microgrid generation balancing solar, battery, and CHP.
- **`pumped_hydro_storage_forecaster`** (Autonomous): Predicts optimal pumping and generation schedules based on reservoir elevation and off-peak spreads.
- **`residential_load_curve_forecaster`** (Autonomous): Forecasts aggregate neighborhood residential load profiles across seasonal regimes.
- **`solar_irradiance_predictor`** (Autonomous): Predicts global horizontal irradiance (GHI) and direct normal irradiance (DNI) from satellite cloud-cover vectors.
- **`thermal_plant_outage_availability_tracker`** (Autonomous): Tracks equivalent forced outage rates (EFOR) and maintenance turnarounds across combined-cycle units.
- **`wind_speed_generation_modeler`** (Autonomous): Converts hub-height wind speed and atmospheric density forecasts into turbine power curve generation forecasts.

#### 3. Grid Balancing (11 Agents)
- **`battery_storage_discharge_optimizer`** (Advisory): Optimizes BESS state-of-charge (SoC), charging during negative pricing and discharging during net-peak.
- **`congestion_node_price_mapper`** (Autonomous): Maps transmission constraint shadow prices and nodal LMP spreads across ISO pricing nodes.
- **`distribution_phase_imbalance_detector`** (Autonomous): Analyzes feeder three-phase current imbalance to prevent neutral overheating and transformer derating.
- **`grid_frequency_deviation_monitor`** (Autonomous): Monitors interconnection frequency deviations (ROCOF) and triggers synthetic inertia / FFR reserves.
- **`islanding_detection_and_management_bot`** (Autonomous): Detects unintended islanding of DER clusters and coordinates anti-islanding protection.
- **`reactive_power_capacitor_dispatcher`** (Advisory): Schedules capacitor bank switching and STATCOM VAR injection to maintain power factor within unity boundaries.
- **`system_inertia_tracker`** (Autonomous): Calculates kinetic rotational inertia across synchronous generation fleets to ensure grid stability.
- **`tie_line_interconnection_limit_supervisor`** (Autonomous): Monitors thermal and voltage stability limits across regional intertie transmission lines.
- **`transmission_line_loss_minimizer`** (Advisory): Models I²R copper and corona transmission losses, recommending optimal power routing.
- **`under_frequency_load_shedding_simulator`** (Advisory): Simulates multi-stage UFLS relay tripping to prevent cascading wide-area grid blackouts.
- **`voltage_sag_swell_mitigator`** (Autonomous): Detects voltage excursions outside ANSI C84.1 Range A and orchestrates tap changer (LTC) actions.

#### 4. Wholesale Trading (12 Agents)
- **`ancillary_services_bid_optimizer`** (Advisory): Formulates bidding curves for regulation up/down, spinning, and supplemental reserves in wholesale markets.
- **`carbon_allowance_market_tracker`** (Autonomous): Tracks compliance carbon offset prices (EUA, CCA) and greenhouse gas credit valuations.
- **`coal_inventory_burn_rate_advisor`** (Advisory): Optimizes coal stockpile burn rates, rail delivery scheduling, and fuel switching economics.
- **`dark_spread_heat_rate_calculator`** (Autonomous): Calculates coal plant dark spreads, clean dark spreads, and operating generation margins.
- **`day_ahead_lmp_forecaster`** (Autonomous): Predicts day-ahead locational marginal pricing across regional wholesale hub nodes.
- **`financial_transmission_right_copilot`** (Advisory): Evaluates FTR auction strategies to hedge basis congestion risk between sink and source nodes.
- **`iso_rto_bidding_curve_generator`** (Advisory): Synthesizes three-part generator supply offer curves (start-up, no-load, energy increment).
- **`natural_gas_pipeline_constraint_analyzer`** (Autonomous): Evaluates interstate gas pipeline flow nominations, maintenance notices, and Henry Hub basis spreads.
- **`portfolio_value_at_risk_analyzer`** (Advisory): Calculates portfolio VaR, Conditional VaR (CVaR), and mark-to-market risk exposure under market volatility.
- **`real_time_lmp_tracker`** (Autonomous): Ingests 5-minute real-time market dispatch pricing, flagging anomalous basis divergence.
- **`renewable_energy_certificate_trader`** (Advisory): Tracks compliance and voluntary REC pricing, vintage banking, and retirement verification.
- **`spark_spread_heat_rate_calculator`** (Autonomous): Computes natural gas spark spreads and heat rate conversion efficiency metrics.

#### 5. Grid Operations (11 Agents)
- **`black_start_restoration_sequencer`** (Advisory): Formulates cranking path energization sequences from black-start diesel/hydro units to transmission islands.
- **`dynamic_etr_calculator`** (Autonomous): Calculates dynamic estimated time to restoration (ETR) based on crew location, hazard conditions, and travel times.
- **`emergency_crew_dispatch_router`** (Advisory): Routes emergency line and tree crews during storm events to maximize restoration velocity.
- **`flisr_switching_simulator`** (Advisory): Simulates fault location, isolation, and service restoration (FLISR) switching sequences to isolate feeder faults.
- **`mobile_substation_deployment_planner`** (Advisory): Plans logistical transport, permit requirements, and electrical tie-in for mobile substations.
- **`mutual_assistance_resource_allocator`** (Advisory): Orchestrates external utility mutual-aid crew lodging, staging site logistics, and truck fleet staging.
- **`outage_footprint_topology_mapper`** (Autonomous): Correlates AMI last-gasp pings and SCADA telemetry with GIS network connectivity models to pinpoint outage boundaries.
- **`scada_breaker_trip_correlator`** (Autonomous): Correlates relay target alarms, oscillography, and SCADA trips to differentiate permanent faults from temporary recloses.
- **`storm_damage_prediction_modeler`** (Autonomous): Predicts broken poles, downed wires, and transformer damage using hurricane/wind gust modeling.
- **`vegetation_encroachment_lidar_analyzer`** (Autonomous): Analyzes aerial LiDAR point-cloud surveys to identify tree growth encroaching on transmission clearance zones.
- **`wildfire_risk_deenergization_trigger`** (Advisory): Evaluates red flag warnings, fuel moisture, and wind gusts to recommend Public Safety Power Shutoffs (PSPS).

#### 6. Smart Meter Management (10 Agents)
- **`ami_interval_data_vee_processor`** (Autonomous): Validates, edits, and estimates (VEE) 15-minute and hourly interval consumption data.
- **`ami_mesh_network_health_monitor`** (Autonomous): Monitors RF mesh collector hops, packet delivery rates, and gateway latency across AMI collectors.
- **`customer_baseline_load_cbl_calculator`** (Advisory): Calculates 10-in-10 baseline customer load profiles for demand response curtailment verification.
- **`demand_response_thermostat_setback_trigger`** (Autonomous): Orchestrates automated demand response events, sending setback signals to smart thermostats.
- **`localized_outage_ping_diagnostic_bot`** (Autonomous): Executes targeted AMI on-demand meter pings to verify nested outage boundaries and post-storm restoration.
- **`meter_firmware_ota_scheduler`** (Advisory): Schedules staged over-the-air (OTA) firmware deployment batches across smart meter fleets.
- **`meter_inversion_tamper_detector`** (Autonomous): Flags physical meter inversion, magnetic tampering, and bypassed current sensors.
- **`prepaid_metering_balance_tracker`** (Autonomous): Tracks prepaid utility account balances, sending low-balance notifications and coordinating disconnect warnings.
- **`smart_meter_temperature_anomaly_detector`** (Autonomous): Detects meter socket overheating, arcing jaw terminals, and loose service entrance conductors.
- **`zero_consumption_anomaly_flag`** (Autonomous): Detects occupied premises exhibiting consecutive zero consumption readings indicative of meter failure.

#### 7. Billing and Invoicing (11 Agents)
- **`budget_billing_levelization_calculator`** (Autonomous): Recalculates 12-month rolling budget billing installments to prevent large year-end settle-up true-ups.
- **`community_solar_subscription_allocator`** (Autonomous): Allocates monthly solar farm generation credits to enrolled offsite residential and commercial subscriber accounts.
- **`critical_peak_pricing_calculator`** (Autonomous): Computes critical peak pricing event surcharges for enrolled dynamic tariff participants.
- **`dynamic_real_time_pricing_biller`** (Autonomous): Bills high-usage industrial accounts on hourly wholesale pass-through index pricing.
- **`electric_vehicle_submeter_billing_processor`** (Autonomous): Isolates dedicated EV submeter intervals to apply specialized overnight EV charging tariffs.
- **`estimated_bill_fallback_generator`** (Autonomous): Generates regulatory-compliant estimated bills when smart meter telemetry is temporarily unreachable.
- **`high_bill_spike_anomaly_flag`** (Autonomous): Flags uncharacteristic bill spikes prior to invoice generation, triggering automated pre-bill audit workflows.
- **`low_income_assistance_eligibility_checker`** (Advisory): Cross-references state assistance program criteria (LIHEAP, CARE/FERA) to evaluate rate discount qualification.
- **`net_metering_export_credit_processor`** (Autonomous): Calculates NEM 2.0 / NEM 3.0 solar net billing credits and annual true-up settlements.
- **`time_of_use_charge_calculator`** (Autonomous): Applies multi-tier time-of-use (TOU) on-peak, mid-peak, and off-peak rating schedules.
- **`wholesale_vendor_payment_reconciler`** (Advisory): Reconciles wholesale energy delivery invoices, transmission wheeling fees, and ISO settlement statements.

#### 8. Customer Engagement (11 Agents)
- **`appliance_disaggregation_efficiency_advisor`** (Advisory): Uses energy disaggregation (NILM) to provide breakdowns of HVAC, water heating, and refrigeration usage.
- **`ev_rate_plan_comparison_guide`** (Advisory): Analyzes smart meter charging patterns to recommend optimal EV electric rate tariffs.
- **`high_bill_weather_correlation_explainer`** (Advisory): Generates natural language customer bill explanations correlating cooling/heating degree days with consumption spikes.
- **`life_support_critical_care_outreach_bot`** (Advisory): Coordinates proactive outreach and verification for medical baseline and life-support designated customer accounts.
- **`move_in_move_out_coordinator`** (Advisory): Orchestrates seamless move-in/move-out requests, service transfer dates, and final meter reads.
- **`multi_language_translation_router`** (Autonomous): Translates customer service inquiries and emergency storm alerts across multiple languages with regulatory accuracy.
- **`new_construction_trenching_guide`** (Advisory): Guides developers and contractors through utility service application, trenching specs, and inspection steps.
- **`omnichannel_intent_triage_router`** (Autonomous): Routes customer inquiries across SMS, web, mobile app, and call center channels to appropriate specialized bots.
- **`proactive_outage_sms_communicator`** (Autonomous): Generates personalized outbound SMS outage notifications, estimated restoration updates, and confirmation pings.
- **`smart_home_device_integration_helper`** (Advisory): Guides customers through connecting smart thermostats, home batteries, and Level 2 EV chargers.
- **`solar_panel_installation_advisor`** (Advisory): Analyzes roof solar potential, historical consumption, and estimated payback economics for prospective solar customers.

#### 9. Regulatory Compliance (10 Agents)
- **`customer_pii_redaction_scrubber`** (Autonomous): Detects and redacts sensitive customer PII, payment info, and SSNs from public regulatory filings and logs.
- **`epa_cems_emissions_aggregator`** (Autonomous): Aggregates continuous emissions monitoring systems (CEMS) data for SO₂, NOₓ, and CO₂ Part 75 reporting.
- **`esg_scope_1_2_carbon_calculator`** (Advisory): Quantifies Scope 1 direct generation emissions and Scope 2 transmission loss emissions for annual ESG disclosure.
- **`ferc_form_1_financial_drafter`** (Advisory): Drafts standardized regulatory balance sheets, income statements, and plant schedules for FERC Form 1 filings.
- **`hazardous_waste_disposal_tracker`** (Autonomous): Tracks transformer PCB dielectric fluid disposal, battery recycling, and RCRA compliance manifests.
- **`nerc_cip_cybersecurity_audit_analyzer`** (Advisory): Audits electronic security perimeters (ESP), firewall access rules, and transient cyber asset logs against NERC CIP standards.
- **`osha_safety_incident_classifier`** (Autonomous): Classifies field safety incidents and near-misses according to OSHA recordable criteria.
- **`puc_rate_case_testimony_drafter`** (Advisory): Synthesizes rate-base capital additions, revenue requirements, and O&M expenses for state utility commission filings.
- **`saidi_saifi_reliability_metric_tracker`** (Autonomous): Calculates IEEE 1366 reliability indices including SAIDI, SAIFI, CAIDI, and MAIFI.
- **`water_usage_discharge_reporter`** (Autonomous): Monitors thermal power plant cooling water intake and thermal discharge effluent limits under NPDES permits.

#### 10. Support Services (10 Agents)
- **`employee_fatigue_risk_monitor`** (Autonomous): Monitors field lineworker shift hours, emergency call-outs, and mandatory rest periods to prevent fatigue incidents.
- **`facility_management_work_order_router`** (Autonomous): Routes maintenance work orders across utility operational service centers, substations, and dispatch buildings.
- **`hardware_procurement_rfp_scorer`** (Advisory): Evaluates and scores vendor proposals for transformers, switchgear, smart meters, and grid hardware.
- **`loto_arc_flash_safety_knowledge_bot`** (Advisory): Delivers lockout/tagout (LOTO) procedures, arc flash boundary PPE requirements, and switching clearances.
- **`mutual_assistance_per_diem_auditor`** (Autonomous): Audits travel expenses, equipment rental fees, and per diem invoices submitted by incoming mutual-aid crews.
- **`power_purchase_agreement_legal_reviewer`** (Advisory): Reviews renewable power purchase agreements (PPA) for curtailment liability, index pricing, and default terms.
- **`scada_vpn_access_helpdesk_bot`** (Autonomous): Automates role-based MFA provisioning, OT network access verification, and session timeout auditing for SCADA engineers.
- **`union_contract_benefits_assistant`** (Advisory): Interprets IBEW collective bargaining agreements regarding overtime bidding, seniority, and travel allowances.
- **`utility_vehicle_fleet_maintenance_tracker`** (Autonomous): Monitors bucket truck telematics, hydraulic boom dielectric testing dates, and DOT chassis inspections.
- **`warehouse_inventory_drone_auditor`** (Autonomous): Reconciles physical inventory scans from automated drone flights across utility central pole yards and staging depots.

---

### System-Wide Guardrails & The Critic Protocol

1. **The Critic Gate (Mandatory):**
   - The internal `CriticSubAgent` within *every* specialized agent enforces strict Markdown table output formatting, audits mathematical calculations, ensures zero PII leaks, and checks compliance with `safety_guardrails.md`.
2. **Tiered Authorization (Human-in-the-Loop):**
   - *Tier 1 (Read / Simulate):* Autonomous execution for analytical queries, forecasting, and data retrieval.
   - *Tier 2 (Grid Mutative / Financial):* Physical switching operations (e.g., FLISR) and financial transactions (e.g., wholesale ISO bidding) generate explicit human-in-the-loop (HITL) confirmation payloads requiring operator authorization.
3. **Shared Session State Machine:**
   - The Master Orchestrator propagates a unified `UtilitiesSessionState` carrying `customer_id`, `grid_zone_id`, `operating_mode` (Normal/Emergency), and `alert_level`.
4. **Defensive BigQuery Tooling:**
   - All quantitative SQL tools execute parameterized read-only queries with regex validation rejecting `DROP`, `DELETE`, `INSERT`, `ALTER`, or `TRUNCATE`. The Critic sub-agent reviews generated SQL before execution.
