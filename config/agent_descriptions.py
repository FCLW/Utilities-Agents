"""
Centralized business purpose descriptions for all 113 Energy & Utilities agents.
Provides tailored, domain-specific descriptions representing the true business role and operational value.
"""

AGENT_DESCRIPTIONS = {
    # 1. Master Orchestrator (1)
    "utilities_master_orchestrator": "Serves as the enterprise AI master coordinator, intelligently routing domain queries, orchestrating multi-agent workflows, and aggregating telemetry insights across all 10 utility operational sub-domains.",

    # 2. Asset Management (14)
    "capital_replacement_simulator": "Simulates CapEx allocation, asset health degradation trajectories, and optimal replacement cycles for aging substation transformers and switchgear to minimize lifecycle costs and avoid catastrophic failures.",
    "circuit_breaker_wear_analyzer": "Tracks cumulative fault interruption currents, mechanical duty cycles, and SF6 gas pressure to predict breaker remaining useful life and schedule condition-based overhauls.",
    "derms_capacity_optimizer": "Analyzes distributed energy resource management system (DERMS) telemetry to optimize hosting capacity, prevent feeder overvoltage, and minimize renewable curtailment.",
    "drone_inspection_image_processor": "Processes high-resolution aerial drone imagery using computer vision to detect structural rust, insulator flashovers, and conductor fraying on high-voltage transmission lines.",
    "ev_charging_station_maintenance_tracker": "Monitors public and fleet EV charging station telemetry, power electronics temperatures, and connector duty cycles to schedule predictive maintenance and maximize charger uptime.",
    "hydro_dam_structural_stress_monitor": "Audits piezometer pore pressures, uplift forces, and concrete crest displacement telemetry to monitor dam structural integrity and ensure regulatory dam safety compliance.",
    "maintenance_fleet_dispatch_scheduler": "Optimizes bucket truck and utility maintenance crew routing, travel routes, and work order assignments based on emergency priority and technician skill certifications.",
    "smart_grid_sensor_health_monitor": "Monitors battery health, signal-to-noise ratios, calibration drift, and reporting latency across distribution grid IoT sensors to guarantee reliable telemetry streams.",
    "solar_inverter_string_fault_detector": "Detects DC string ground faults, thermal clipping anomalies, and MPPT tracking efficiency degradation across utility-scale solar photovoltaic plants.",
    "spare_parts_inventory_forecaster": "Forecasts critical substation transformer bushings, circuit breaker spares, and relay inventory demands using predictive failure rates and supply chain lead times.",
    "substation_battery_health_tracker": "Analyzes internal cell resistance, float voltages, and thermal runaway risks on 125VDC station battery banks powering critical protection and control relays.",
    "transformer_dga_health_monitor": "Interprets Dissolved Gas Analysis (DGA) ppm ratios (Duval Triangle, Rogers Ratios) to detect arcing, partial discharges, and thermal hotspots in power transformers before catastrophic failure.",
    "transmission_tower_corrosion_analyzer": "Evaluates atmospheric salinity, zinc galvanization loss, and steel structural thickness to prioritize protective recoating schedules for high-voltage transmission towers.",
    "wind_turbine_gearbox_vibration_analyzer": "Analyzes high-frequency accelerometer vibration spectra and oil particle counts to detect early bearing spalling and gear tooth pitting in wind turbine drivetrains.",

    # 3. Billing and Invoicing (11)
    "budget_billing_levelization_calculator": "Computes rolling 12-month budget billing settlement balances and recalculates levelized monthly installments to prevent year-end true-up bill shock for residential customers.",
    "community_solar_subscription_allocator": "Calculates virtual net metering generation credits and subscriber bill allocations from community solar projects against monthly utility customer tariffs.",
    "critical_peak_pricing_calculator": "Computes dynamic event-day hourly surcharges and baseline credits during utility-declared critical peak pricing events to incentivize demand response.",
    "dynamic_real_time_pricing_biller": "Calculates interval billing charges indexed to real-time locational marginal prices (LMP) and capacity demand curves for commercial and industrial customers.",
    "electric_vehicle_submeter_billing_processor": "Disaggregates dedicated EV charging submeter interval data from whole-home smart meters to apply specialized off-peak EV charging rate tariffs.",
    "estimated_bill_fallback_generator": "Generates weather-normalized, algorithmically sound fallback usage estimations for unread smart meters to maintain billing schedules without revenue leakage.",
    "high_bill_spike_anomaly_flag": "Detects anomalous consumption spikes relative to historical weather-adjusted usage before invoice dispatch to prevent customer billing disputes and billing errors.",
    "low_income_assistance_eligibility_checker": "Evaluates customer income thresholds and assistance criteria for LIHEAP, state rate discounts, and arrearage management programs to streamline subsidy enrollment.",
    "net_metering_export_credit_processor": "Reconciles bidirectional AMI solar export kilowatt-hours against retail grid consumption to calculate tariff-accurate net energy metering (NEM) bill credits.",
    "time_of_use_charge_calculator": "Partitions interval smart meter consumption into on-peak, mid-peak, and off-peak rate tiers to accurately apply complex multi-tier time-of-use tariffs.",
    "wholesale_vendor_payment_reconciler": "Reconciles power purchase agreement generation invoices, bilateral energy contracts, and transmission pass-through fees against ISO/RTO settlement statements.",

    # 4. Customer Engagement (11)
    "appliance_disaggregation_efficiency_advisor": "Decomposes smart meter interval data into appliance-level consumption profiles (HVAC, water heating, refrigeration) to deliver personalized energy efficiency recommendations.",
    "ev_rate_plan_comparison_guide": "Simulates customer annual charging costs across available residential and whole-home TOU tariffs based on personalized EV commuting and home charging patterns.",
    "high_bill_weather_correlation_explainer": "Correlates heating and cooling degree days against customer interval energy usage to generate clear, transparent explanations for monthly utility bill fluctuations.",
    "life_support_critical_care_outreach_bot": "Manages priority registry communications and proactive outreach workflows for medical baseline and life-support customers during planned and unplanned outages.",
    "move_in_move_out_coordinator": "Automates meter reading transfers, final bill settlement, and service activation workflows for residential and commercial customer move-in and move-out requests.",
    "multi_language_translation_router": "Provides real-time, culturally attuned multilingual translation of customer service inquiries, outage alerts, and billing explanations across multiple languages.",
    "new_construction_trenching_guide": "Guides contractors and builders through utility trenching specifications, joint-use clearances, and service connection inspection milestones for new construction projects.",
    "omnichannel_intent_triage_router": "Classifies incoming customer inquiries across voice, web chat, and mobile channels, routing complex technical or billing issues to specialized domain agents or live representatives.",
    "proactive_outage_sms_communicator": "Generates real-time, circuit-specific SMS outage notifications with estimated restoration times, cause updates, and field crew status for impacted customers.",
    "smart_home_device_integration_helper": "Guides residential customers through connecting smart thermostats, home batteries, and EV chargers to utility demand response and energy management programs.",
    "solar_panel_installation_advisor": "Evaluates rooftop solar irradiance potential, historical consumption offsets, and net metering payback periods for customers exploring solar photovoltaic installations.",

    # 5. Grid Balancing (11)
    "battery_storage_discharge_optimizer": "Schedules battery energy storage system (BESS) charge and discharge cycles to maximize wholesale market revenue while minimizing battery cell degradation.",
    "congestion_node_price_mapper": "Maps transmission congestion bottlenecks and shadow prices across nodal pricing nodes to identify grid redispatch constraints and power flow bottlenecks.",
    "distribution_phase_imbalance_detector": "Analyzes three-phase current and voltage telemetry on distribution feeders to identify and remediate phase load unbalance and reduce neutral conductor heating.",
    "grid_frequency_deviation_monitor": "Tracks real-time area control error (ACE) and sub-second frequency deviations to automatically trigger primary and secondary frequency response reserves.",
    "islanding_detection_and_management_bot": "Detects unintentional islanding conditions on microgrids and feeder segments, executing safe decoupling or coordinating stable microgrid islanding operations.",
    "reactive_power_capacitor_dispatcher": "Coordinates switched shunt capacitor banks and static VAR compensators to optimize power factor and maintain feeder voltage stability across transmission and distribution networks.",
    "system_inertia_tracker": "Calculates real-time online synchronous rotational inertia and synthetic inertia headroom to assess grid vulnerability to sudden generation loss contingencies.",
    "tie_line_interconnection_limit_supervisor": "Monitors thermal and transient stability limits across regional balancing authority interties to enforce NERC reliability standards and prevent tie-line overloads.",
    "transmission_line_loss_minimizer": "Optimizes transmission power flow dispatch and transformer tap positions to minimize resistive I²R line losses across the bulk electric transmission system.",
    "under_frequency_load_shedding_simulator": "Simulates multi-stage UFLS relay trip schemes and feeder load-shed priorities to prevent system-wide blackout during extreme generation contingency events.",
    "voltage_sag_swell_mitigator": "Detects and classifies transient voltage sags and swells caused by faults or heavy industrial switching, coordinating fast-acting volt-VAR controls to protect sensitive customer equipment.",

    # 6. Grid Operations (11)
    "black_start_restoration_sequencer": "Formulates safe, step-by-step restoration sequences from black-start cranking units through transmission corridors to re-energize critical substations and customer loads.",
    "dynamic_etr_calculator": "Calculates dynamic Estimated Time of Restoration (ETR) based on incoming storm severity, damage assessment reports, travel conditions, and field crew allocations.",
    "emergency_crew_dispatch_router": "Optimizes emergency troubleman and lineworker dispatch routing to high-priority hazard locations, wire-down reports, and critical infrastructure circuits during storm events.",
    "flisr_switching_simulator": "Simulates Fault Location, Isolation, and Service Restoration (FLISR) switching sequences to isolate faulted feeder sections and automatically restore power to healthy segments.",
    "mobile_substation_deployment_planner": "Plans transport routing, bridge clearances, and electrical connection logistics for mobile substation transformers during catastrophic substation transformer failures.",
    "mutual_assistance_resource_allocator": "Coordinates inter-utility mutual aid crew staging, lodging logistics, and equipment allocations ahead of major severe weather and hurricane restoration events.",
    "outage_footprint_topology_mapper": "Correlates smart meter last-gasp pings and SCADA breaker trips against GIS electrical connectivity to map nested outage footprints accurately.",
    "scada_breaker_trip_correlator": "Correlates high-speed SCADA digital fault recorder events, protective relay targets, and breaker operations to identify fault locations and root causes.",
    "storm_damage_prediction_modeler": "Predicts utility pole breakage, conductor wire-down counts, and customer outage volumes based on incoming wind gust, ice accretion, and soil saturation forecasts.",
    "vegetation_encroachment_lidar_analyzer": "Processes aerial LiDAR point clouds and satellite vegetation indices to prioritize hazardous tree trimming along transmission and distribution rights-of-way.",
    "wildfire_risk_deenergization_trigger": "Evaluates real-time wind speeds, fuel moisture levels, and red flag warnings to model risk thresholds for Public Safety Power Shutoff (PSPS) decisions.",

    # 7. Production Forecasting (12)
    "commercial_load_curve_forecaster": "Forecasts 24-hour and day-ahead electricity demand profiles for commercial building portfolios using weather forecasts and business occupancy schedules.",
    "ev_charging_load_spike_predictor": "Models peak power demand surges and coincidence factors across public DC fast-charging plazas and commercial fleet charging depots.",
    "extreme_weather_anomaly_alert_bot": "Alerts grid forecasting operators to sudden temperature plunges, polar vortex anomalies, and extreme heatwaves that trigger unprecedented demand spikes.",
    "geothermal_output_forecaster": "Forecasts megawatt output for geothermal power plants based on production well enthalpy, brine temperatures, and reinjection reservoir pressures.",
    "hydro_inflow_snowpack_estimator": "Estimates seasonal river inflows and reservoir water volumes using satellite snowpack depth measurements and melting degree-day hydrological models.",
    "industrial_load_curve_forecaster": "Forecasts electricity load profiles for heavy industrial manufacturing, arc furnaces, and chemical processing facilities based on production schedules and shift changes.",
    "microgrid_generation_forecaster": "Forecasts behind-the-meter solar PV, combined heat and power (CHP), and battery storage availability for resilient campus and hospital microgrids.",
    "pumped_hydro_storage_forecaster": "Optimizes upper reservoir pumping schedules during low-cost renewable hours and generation dispatch during high-priced peak demand periods.",
    "residential_load_curve_forecaster": "Forecasts aggregate residential feeder electricity demand by modeling weather sensitivity, rooftop solar adoption, and seasonal heating/cooling dynamics.",
    "solar_irradiance_predictor": "Predicts global horizontal irradiance (GHI) and direct normal irradiance (DNI) using satellite cloud-cover vectors and numerical weather prediction models.",
    "thermal_plant_outage_availability_tracker": "Tracks scheduled maintenance outages, forced outage rates (EFOR), and heat rate efficiency across combined-cycle natural gas and peaking turbine fleets.",
    "wind_speed_generation_modeler": "Converts hub-height wind speed and direction forecasts into turbine power curves to generate hourly wind farm generation forecasts.",

    # 8. Regulatory Compliance (10)
    "customer_pii_redaction_scrubber": "Autonomously detects and redacts customer personally identifiable information (PII) from work orders, billing dispute transcripts, and public regulatory filings.",
    "epa_cems_emissions_aggregator": "Aggregates continuous emissions monitoring system (CEMS) telemetry to verify utility compliance with EPA Clean Air Act SO2, NOx, and CO2 limits.",
    "esg_scope_1_2_carbon_calculator": "Computes Scope 1 direct generation emissions and Scope 2 transmission loss emissions for annual ESG regulatory disclosures and sustainability reports.",
    "ferc_form_1_financial_drafter": "Assembles standardized utility financial accounts, plant investment schedules, and operational expenses for annual FERC Form 1 regulatory submissions.",
    "hazardous_waste_disposal_tracker": "Tracks manifest compliance, storage limits, and certified disposal documentation for transformer PCB oils, SF6 gas cylinders, and substation chemical waste.",
    "nerc_cip_cybersecurity_audit_analyzer": "Audits access control logs, electronic security perimeters (ESP), and patch management schedules for NERC Critical Infrastructure Protection (CIP) compliance.",
    "osha_safety_incident_classifier": "Classifies workplace injuries, near-misses, and OSHA recordable incidents while tracking Days Away, Restricted, or Transferred (DART) safety metrics.",
    "puc_rate_case_testimony_drafter": "Drafts technical exhibits, revenue requirement schedules, and cost-of-service testimony for state Public Utility Commission general rate cases.",
    "saidi_saifi_reliability_metric_tracker": "Calculates system reliability indices including SAIDI, SAIFI, and CAIDI with IEEE 1366 Major Event Day (MED) exclusions for regulatory reporting.",
    "water_usage_discharge_reporter": "Tracks thermal power plant cooling water withdrawal volumes, consumptive usage, and National Pollutant Discharge Elimination System (NPDES) thermal limits.",

    # 9. Smart Meter Management (10)
    "ami_interval_data_vee_processor": "Executes automated Validation, Editing, and Estimation (VEE) on raw 15-minute smart meter interval datasets to guarantee billing-quality data streams.",
    "ami_mesh_network_health_monitor": "Monitors radio frequency (RF) mesh network latency, collector throughput, and node hopping hops across the AMI communication backhaul.",
    "customer_baseline_load_cbl_calculator": "Computes customer baseline load (CBL) profiles using standard 10-in-10 or weather-matched algorithms to verify demand response curtailment performance.",
    "demand_response_thermostat_setback_trigger": "Dispatches automated temperature setback signals to enrolled smart thermostats during grid emergency peak load reduction events.",
    "localized_outage_ping_diagnostic_bot": "Sends targeted on-demand ping interrogations to smart meters on suspect feeder lateral branches to confirm whether service has been restored.",
    "meter_firmware_ota_scheduler": "Schedules over-the-air (OTA) firmware update batches across smart meter fleets while managing mesh network bandwidth and preventing communication bottlenecks.",
    "meter_inversion_tamper_detector": "Detects reverse energy flow, tilt sensor trips, and anomalous zero-current events indicating physical meter tampering or unmetered energy theft.",
    "prepaid_metering_balance_tracker": "Computes real-time kilowatt-hour drawdowns, daily balances, and automated low-balance warning alerts for enrolled prepaid electricity customers.",
    "smart_meter_temperature_anomaly_detector": "Monitors internal meter collar terminal temperature telemetry to identify high-resistance electrical connections and prevent meter fires.",
    "zero_consumption_anomaly_flag": "Flags meters reporting consecutive zero-consumption intervals for occupied premises to diagnose meter failures or unauthorized bypasses.",

    # 10. Support Services (10)
    "employee_fatigue_risk_monitor": "Tracks cumulative field lineworker shift hours, rest intervals, and overtime limits during emergency storm duty to enforce safety fatigue standards.",
    "facility_management_work_order_router": "Triages and dispatches HVAC, electrical, and physical security maintenance work orders across utility operational service centers and substations.",
    "hardware_procurement_rfp_scorer": "Scores vendor proposals for utility hardware procurement against technical specifications, warranty terms, and pricing matrices.",
    "loto_arc_flash_safety_knowledge_bot": "Provides instant retrieval of Lockout/Tagout (LOTO) procedures, arc flash incident energy boundary calculations, and NFPA 70E PPE requirements.",
    "mutual_assistance_per_diem_auditor": "Audits visiting mutual aid contractor timesheets, meal per diems, and equipment rental rates against industry mutual assistance guidelines.",
    "power_purchase_agreement_legal_reviewer": "Analyzes renewable energy Power Purchase Agreements (PPAs) for curtailment liability terms, performance guarantees, and credit security provisions.",
    "scada_vpn_access_helpdesk_bot": "Automates authentication troubleshooting, MFA token verification, and role-based access approval for authorized engineers accessing SCADA networks.",
    "union_contract_benefits_assistant": "Answers worker queries regarding collective bargaining agreement provisions, overtime seniority rules, and utility retirement benefits.",
    "utility_vehicle_fleet_maintenance_tracker": "Tracks telematics, engine diagnostic fault codes, hydraulic aerial lift inspections, and preventive maintenance for utility service bucket trucks.",
    "warehouse_inventory_drone_auditor": "Coordinates autonomous indoor warehouse drone flights to scan barcode and RFID tags on high-bay utility equipment racks.",

    # 11. Wholesale Trading (12)
    "ancillary_services_bid_optimizer": "Formulates optimal co-optimized bid curves for spinning reserves, regulation up/down, and non-spinning reserves in wholesale ISO markets.",
    "carbon_allowance_market_tracker": "Tracks spot prices, trading volumes, and forward price trends for regional carbon compliance allowances and voluntary carbon offsets.",
    "coal_inventory_burn_rate_advisor": "Models coal pile inventory levels, daily plant burn rates, and railcar delivery schedules to optimize stockpile replenishment economics.",
    "dark_spread_heat_rate_calculator": "Calculates clean and dirty dark spreads for coal generation units factoring fuel costs, plant heat rates, and carbon emissions prices.",
    "day_ahead_lmp_forecaster": "Forecasts day-ahead Locational Marginal Prices (LMP) across ISO pricing hubs by modeling load forecasts, generation supply stacks, and transmission bottlenecks.",
    "financial_transmission_right_copilot": "Analyzes historical congestion patterns and auction clearing prices to optimize Financial Transmission Right (FTR) and Congestion Revenue Right (CRR) portfolios.",
    "iso_rto_bidding_curve_generator": "Generates multi-segment incremental energy offer curves for generation resources submitted to day-ahead and real-time ISO wholesale markets.",
    "natural_gas_pipeline_constraint_analyzer": "Monitors interstate pipeline flow notices, compressor outages, and basis spreads to model fuel supply risks for gas-fired generation fleets.",
    "portfolio_value_at_risk_analyzer": "Calculates Portfolio Value at Risk (VaR), stress tests extreme weather price shocks, and monitors counterparty credit exposure across trading books.",
    "real_time_lmp_tracker": "Monitors 5-minute real-time LMP price spikes, scarcity pricing triggers, and reserve shortage events across wholesale market nodes.",
    "renewable_energy_certificate_trader": "Tracks compliance and voluntary Renewable Energy Certificate (REC) inventory, vintage eligibility, and market transaction settlements.",
    "spark_spread_heat_rate_calculator": "Calculates spark spreads and clean spark spreads for combined-cycle and combustion turbine natural gas plants against real-time power and gas prices."
}

def get_agent_description(agent_id: str, default: str = "") -> str:
    """Retrieve the business-purpose description for a given agent_id."""
    return AGENT_DESCRIPTIONS.get(agent_id, default)
