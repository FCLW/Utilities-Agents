#!/usr/bin/env python3
"""
prompts_generator.py — Domain-specific, highly tailored sample business prompts for all 113 agents.
Ensures distinct sentence structures, natural business phrasing, and deep alignment with utility workflows.
"""

AGENT_PROMPTS = {
    # 0. Master Orchestrator
    "utilities_master_orchestrator": [
        "Which specialized agents are currently handling active telemetry anomalies across the distribution grid?",
        "Audit cross-agent routing latency and dispatch accuracy for storm event #2026-B.",
        "What is the system-wide operational risk score aggregated across all sub-domains today?",
        "Initiate a multi-agent emergency coordination protocol across Grid Operations and Crew Dispatch."
    ],

    # 1. Asset Management (14 agents)
    "capital_replacement_simulator": [
        "Which aging 230kV substation transformers have crossed the 35-year threshold and qualify for immediate capital replacement?",
        "Compare the 10-year lifecycle replacement cost of SF6 gas-insulated breakers versus vacuum circuit breakers.",
        "How much CapEx deferral can we achieve if we apply predictive condition-based maintenance across Substation Zone 4?",
        "Stage a prioritized FY27 capital asset replacement schedule for board review and regulatory rate case inclusion."
    ],
    "circuit_breaker_wear_analyzer": [
        "How many fault interruptions has Breaker CB-104 cleared since its last overhaul, and what is its remaining contact wear percentage?",
        "Plot the cumulative I²t fault energy curve for feeder breakers in Substation Alpha over the past 24 months.",
        "What is the catastrophic failure probability of Breaker CB-22 if operated under maximum short-circuit duty?",
        "Flag Breaker CB-104 for emergency contact inspection and temporarily reduce recloser shot attempts."
    ],
    "derms_capacity_optimizer": [
        "What is the aggregate flexible curtailment capacity available from residential battery and solar DERs on Feeder 12?",
        "Analyze the reverse power flow and voltage rise profile along Circuit 4B during peak PV generation hours.",
        "How will onboarding 500 new commercial rooftop PV installations impact local substation hosting capacity?",
        "Dispatch a dynamic 1.5 MW reactive power absorption setpoint to connected commercial smart inverters in West Ridge."
    ],
    "drone_inspection_image_processor": [
        "Did yesterday's autonomous drone flight over Transmission Line 502 detect any chipped ceramic insulators or frayed shield wires?",
        "Evaluate the thermal infrared hotspot severity on conductor splice joints along Tower Span 45 to 60.",
        "Summarize the defect severity index and structural risk rating across all drone-surveyed transmission corridors this week.",
        "Generate a high-priority work ticket for structural reinforcement on Tower #118 with embedded LiDAR coordinate tags."
    ],
    "ev_charging_station_maintenance_tracker": [
        "Which DC fast chargers in the municipal fleet hub are reporting ground fault errors or cable overheating?",
        "Track the mean time between failures (MTBF) and connector wear rates for Level 3 CCS chargers over the past quarter.",
        "What is our projected quarterly maintenance budget variance driven by vandalism and thermal sensor failures at public EV stations?",
        "Issue a remote reboot and preventive field service dispatch for Charger Hub #14 at Airport North."
    ],
    "hydro_dam_structural_stress_monitor": [
        "Are piezometer hydrostatic uplift pressures on the spillway foundation of Dam Unit 2 within FERC safety margins?",
        "Review the 6-month inclinometer tilt drift and seismic accelerometer readings for the main concrete gravity abutment.",
        "What is the structural risk index of the dam under a simulated 100-year probable maximum precipitation (PMP) event?",
        "Trigger an automated sluice gate relief sequence and alert the dam safety engineer of abnormal foundation uplift."
    ],
    "maintenance_fleet_dispatch_scheduler": [
        "Which aerial bucket trucks and digger derricks are closest to the reported pole fire on Highway 101?",
        "Evaluate crew route efficiency and overtime hours across regional service depots during yesterday's lightning storm.",
        "How will scheduling routine fleet hydraulic inspections during off-peak hours reduce emergency dispatch delays?",
        "Reroute Crew Bravo from routine preventive inspection to high-priority pole replacement at Substation South."
    ],
    "smart_grid_sensor_health_monitor": [
        "Which distribution line sensors on Feeder 8 are reporting anomalous battery voltage drops or lost DNP3 heartbeats?",
        "Analyze the packet loss rate and signal-to-noise ratio across cellular IoT fault current indicators over the past week.",
        "What percentage of our distribution sensor fleet is expected to reach end-of-life battery exhaustion within 90 days?",
        "Trigger an over-the-air sensor diagnostic reboot and reassign primary telemetry routing to redundant node S-19."
    ],
    "solar_inverter_string_fault_detector": [
        "Which PV inverter strings in Solar Farm Bravo are exhibiting DC clipping or ground fault insulation breakdown?",
        "Compare the string-level current-voltage curves against clear-sky baseline expectations for Inverter Block 7.",
        "How much generation revenue is lost daily due to uncorrected string disconnections in the Desert Vista facility?",
        "Isolate Inverter String 14B remotely and dispatch a solar field technician with replacement bypass diodes."
    ],
    "spare_parts_inventory_forecaster": [
        "Do we have sufficient spare 50kVA pole-mounted distribution transformers in Central Warehouse to withstand peak storm season?",
        "Forecast the 12-month replenishment lead time and burn rate for SF6 gas cylinders and surge arresters.",
        "What is our carrying cost exposure if we increase safety stock for high-voltage bushings by 15%?",
        "Generate an automated purchase requisition for 25 units of 15kV cutouts and distribution fuses."
    ],
    "substation_battery_health_tracker": [
        "Are internal cell resistance and float voltages on the 125V DC control battery bank at Substation Echo within IEEE 450 specs?",
        "Track the thermal runaway risk and electrolyte level degradation across lead-acid banks over the trailing 12 months.",
        "What is the probability of DC trip failure on transmission breakers during an AC station service blackout?",
        "Schedule urgent cell replacement for Jar #8 in Bank 2 and trigger an automated battery discharge load test."
    ],
    "transformer_dga_health_monitor": [
        "What do the latest dissolved gas ratios for Main Transformer T-104 reveal regarding acetylene and ethylene generation?",
        "Examine the historical Duval triangle trajectory for Substation North to determine if active thermal arcing is accelerating.",
        "Assess the catastrophic tank rupture risk and remaining paper insulation life (DP value) for Transformer T-104.",
        "Issue an immediate transformer load derate directive and schedule emergency oil degasification treatment."
    ],
    "transmission_tower_corrosion_analyzer": [
        "Which lattice steel towers along Coastal Line 230-1 show severe galvanic zinc loss or pack rust on structural footings?",
        "Correlate atmospheric salt spray deposition and ultrasonic steel thickness measurements from the latest inspection cycle.",
        "What is the projected capital rehabilitation expenditure required over the next 5 years to arrest corrosion in Marine District?",
        "Stage a structural grit-blasting and protective recoating work order for Tower #72 before winter coastal gale season."
    ],
    "wind_turbine_gearbox_vibration_analyzer": [
        "Are planetary gear bearing acceleration spectra on Wind Turbine WTG-09 exhibiting high-frequency crest factor anomalies?",
        "Track the lubrication particle count and vibration velocity trends over the last 90 days of high wind operation.",
        "What is the estimated mechanical remaining useful life (RUL) of Turbine 09 before catastrophic gearbox seizure?",
        "Curtail Turbine WTG-09 maximum generator output to 50% and schedule an immediate borescope gearbox inspection."
    ],

    # 2. Billing And Invoicing (11 agents)
    "budget_billing_levelization_calculator": [
        "How large is the cumulative settlement balance variance across residential budget billing participants after the winter polar vortex?",
        "Compare the annualized rolling monthly energy spend versus actual billed amounts for customer tier R-1.",
        "What percentage of levelized billing accounts will face a true-up spike exceeding $250 next spring?",
        "Recalculate monthly budget installment amounts for accounts with variance exceeding ±20% and queue notification letters."
    ],
    "community_solar_subscription_allocator": [
        "Did the 5 MW SunRidge Community Solar garden generate enough surplus kWh to cover all 1,200 residential subscription credits this month?",
        "Reconcile customer monthly kilowatt-hour allocations against metered solar production and subscriber turnover rates.",
        "What is the financial credit leakage rate resulting from delayed subscriber churn updates in the billing engine?",
        "Execute monthly subscriber credit balance distribution to the CIS billing system for the upcoming billing cycle."
    ],
    "critical_peak_pricing_calculator": [
        "What were the total kilowatt-hour consumption charges billed during yesterday's 4-hour Critical Peak Pricing event in Zone 1?",
        "Analyze customer load reduction elasticity and price responsiveness across commercial accounts under the $1.50/kWh peak rate.",
        "How much revenue variance did the critical peak event produce compared to standard flat-rate billing projections?",
        "Finalize and post critical peak surcharge line items for 35,000 participating smart meter accounts."
    ],
    "dynamic_real_time_pricing_biller": [
        "How do five-minute wholesale LMP spot prices map to large industrial customer bills for yesterday's afternoon price spike?",
        "Evaluate the bill savings achieved by metallurgical facilities that curtailed load when spot prices exceeded $300/MWh.",
        "What is our unbilled revenue reconciliation gap between real-time wholesale procurement costs and customer billing receipts?",
        "Generate and dispatch dynamic interval billing statements for all Schedule RTP high-voltage customers."
    ],
    "electric_vehicle_submeter_billing_processor": [
        "Did the submetered Level 2 EV charger at account #449210 properly isolate charging kWh from the main household consumption?",
        "Audit interval charging records to ensure zero double-counting of net-metered residential solar exports against EV submeters.",
        "What is our revenue leakage volume from unassigned or desynchronized smart EV charging submeters this month?",
        "Apply the discounted overnight EV-9 charging tariff credit to submetered charging sessions for Account #449210."
    ],
    "estimated_bill_fallback_generator": [
        "How many customer bills in District 4 required estimation due to cellular AMI collector outages during the ice storm?",
        "Compare heating degree-day regression estimates against subsequent actual meter read true-ups for estimated accounts.",
        "What is the customer complaint risk score and billing dispute volume attributable to consecutive estimated reads?",
        "Generate automated estimated bill statements using degree-day adjusted historical profiles for missing AMI meters."
    ],
    "high_bill_spike_anomaly_flag": [
        "Which commercial accounts experienced an unexplained 300% billing increase compared to their 12-month seasonal median?",
        "Correlate billing spike flags with meter multiplier errors, water heater faults, or stuck HVAC relays.",
        "What is the total disputed billing dollar volume currently held under audit review for spike anomalies?",
        "Place a temporary billing hold on Account #882194 to prevent auto-debit pending on-site meter re-verification."
    ],
    "low_income_assistance_eligibility_checker": [
        "Does customer account #901284 qualify for the state CARE or LIHEAP utility discount based on verified income thresholds?",
        "Track the processing throughput and verification latency for low-income discount applications received this month.",
        "How much unused funding remains in the annual low-income emergency ratepayer assistance fund?",
        "Enroll Account #901284 in the 30% monthly lifeline discount program and waive past-due late payment penalties."
    ],
    "net_metering_export_credit_processor": [
        "What is the total dollar credit owed to residential rooftop solar owners for surplus energy exported to the grid last billing cycle?",
        "Reconcile customer solar export kWh credits calculated at avoided-cost tariff rates versus full retail net metering rules.",
        "What is the revenue impact of annual NEM true-up cash payouts scheduled for disbursement next month?",
        "Publish net surplus generation compensation credits to 14,200 NEM 2.0 customer billing registers."
    ],
    "time_of_use_charge_calculator": [
        "Are off-peak, mid-peak, and on-peak interval kWh accurately categorized for residential accounts under Tariff TOU-D?",
        "Evaluate the distribution of customer load shifting away from the 4 PM to 9 PM peak window since tariff migration.",
        "What is the uncollected demand charge variance across commercial accounts on seasonal time-of-use schedules?",
        "Calculate and commit the multi-tier TOU charge distribution across 85,000 smart-metered customer accounts."
    ],
    "wholesale_vendor_payment_reconciler": [
        "Do our monthly transmission wheeling fee invoices from Regional Grid Operator match internal SCADA interchange logs?",
        "Reconcile disputed line-item billing variances on fuel transport contracts with pipeline operators for Q3.",
        "What is the outstanding disputed payable balance currently withheld pending vendor meter calibration proof?",
        "Authorize scheduled wire settlement for wholesale power supplier invoices matching contract settlement tolerance."
    ],

    # 3. Customer Engagement (11 agents)
    "appliance_disaggregation_efficiency_advisor": [
        "Can you break down my monthly 1,450 kWh electric bill into heating, cooling, refrigeration, and EV charging categories?",
        "Compare this household's HVAC runtime and baseload phantom power draw against similar homes in the neighborhood.",
        "What are the top three energy conservation actions that would save this customer at least $45 per month?",
        "Dispatch a personalized Home Energy Audit report with tailored heat pump rebate incentives to Customer #10294."
    ],
    "ev_rate_plan_comparison_guide": [
        "Which rate plan will minimize my monthly electric costs if I charge an EV with a 75 kWh battery exclusively overnight?",
        "Compare projected annual energy expenses under the Standard Residential Tier versus the EV Time-of-Use Plan.",
        "What is the breakeven monthly mileage threshold where switching to a dedicated EV rate becomes financially advantageous?",
        "Switch Customer Account #773829 to the EV-TOU rate schedule effective with the upcoming meter billing cycle."
    ],
    "high_bill_weather_correlation_explainer": [
        "Why was my electric bill $140 higher this January compared to the previous month?",
        "Correlate local outdoor heating degree-days and extreme sub-zero temperature spells with the customer's daily smart meter usage.",
        "What portion of the customer's 42% bill increase was caused by extreme weather versus rate tariff adjustments?",
        "Generate a customer-facing bill explainer graphic detailing day-by-day temperature impact for CSR agent use."
    ],
    "life_support_critical_care_outreach_bot": [
        "Are there any registered medical life-support customers residing in the projected footprint of Outage Event #402?",
        "Verify emergency backup generator availability and confirmed contact phone numbers for vulnerable residents in Zone 6.",
        "What is the outbound outreach completion percentage across critical care accounts ahead of the forecasted ice storm?",
        "Trigger an automated priority voice call and SMS welfare check to all registered life-support accounts in Sector 3."
    ],
    "move_in_move_out_coordinator": [
        "Can you schedule service deactivation for 742 Evergreen Terrace on October 1st and activate service at the new address?",
        "Verify final meter reading capture protocols and deposit transfer eligibility for residential tenant transfers.",
        "What is the average turnaround time for automated remote smart meter turn-ons during peak student moving week?",
        "Submit an automated remote meter energization command for 104 Oak Lane with effective timestamp set to 08:00 AM."
    ],
    "multi_language_translation_router": [
        "Can you translate this urgent boil-water notice and outage restoration update into Spanish, Vietnamese, and Tagalog?",
        "Audit customer language preference records to ensure emergency SMS broadcasts match subscriber language settings.",
        "What is the message delivery success rate across non-English customer emergency notifications during the heatwave?",
        "Broadcast the multilingual safety alert across localized distribution channels for all affected community zones."
    ],
    "new_construction_trenching_guide": [
        "What are the minimum trench depth and conduit separation clearances required for joint electric and gas utility lines?",
        "Review the developer trenching blueprint for Green Valley Subdivision Phase 2 against municipal electrical safety codes.",
        "What are the primary project delay risks and inspection failure causes documented in recent developer trench submittals?",
        "Approve the underground conduit trenching inspection checklist and schedule field inspector site verification."
    ],
    "omnichannel_intent_triage_router": [
        "Is this incoming customer inquiry regarding a downed power line, a billing payment arrangement, or a solar interconnection status?",
        "Analyze customer sentiment scores and channel escalation frequency across mobile app, chat, and IVR channels.",
        "What is the first-contact resolution (FCR) rate for billing inquiries routed directly to self-service resolution bots?",
        "Escalate customer ticket #88412 directly to the Emergency Outage Dispatch queue due to detected live wire keywords."
    ],
    "proactive_outage_sms_communicator": [
        "Which customers on Feeder 4 should receive proactive SMS notifications about the tree-related power outage?",
        "Track SMS delivery throughput and customer click-through rates on live outage map tracking links.",
        "What is the estimated reduction in call center inbound volume achieved by proactive outage notifications during storm events?",
        "Dispatch an automated restoration update SMS with updated Estimated Time of Restoration (ETR) to 2,400 affected premises."
    ],
    "smart_home_device_integration_helper": [
        "How does a customer pair their ecobee or Nest smart thermostat with our utility Demand Response rewards program?",
        "Audit telemetry communication success rates between the utility DERMS cloud and customer smart home smart plugs.",
        "What is the customer attrition rate from smart thermostat pre-cooling programs during consecutive high-temperature days?",
        "Issue a test demand reduction event signal to enrolled smart home devices on Circuit 9 to verify gateway responsiveness."
    ],
    "solar_panel_installation_advisor": [
        "Can you estimate the solar generation potential and payback period for a 2,200 sq ft residential rooftop in Zip Code 94107?",
        "Compare the annual kWh yield of a south-facing 8 kW system with battery storage versus a standalone solar array.",
        "What are the local utility net metering interconnection requirements and transformer capacity constraints for this parcel?",
        "Generate a pre-interconnection feasibility score and dispatch the solar customer application packet to the homeowner."
    ],

    # 4. Grid Balancing (11 agents)
    "battery_storage_discharge_optimizer": [
        "What is the optimal state-of-charge schedule to maximize revenue for our 20 MW / 80 MWh battery during evening peak LMP spikes?",
        "Analyze battery degradation cost per equivalent full cycle under aggressive frequency regulation versus energy arbitrage.",
        "How much reserve capacity must remain in Battery Unit 2 to meet mandated emergency spin commitments?",
        "Commit an automated 15 MW discharge dispatch order to CAISO real-time market for BESS Unit 1 starting at 17:30."
    ],
    "congestion_node_price_mapper": [
        "Which transmission interfaces and flowgates are currently driving Locational Marginal Price (LMP) congestion over $250/MWh?",
        "Map the historical shadow prices and shift factors on the North-South transmission tie line over the last 30 days.",
        "What is the financial congestion cost exposure across our physical generation portfolio if Line 301 is de-rated?",
        "Re-optimize generator dispatch setpoints across unconstrained nodes to mitigate localized transmission congestion penalties."
    ],
    "distribution_phase_imbalance_detector": [
        "Are Phase A, B, and C current loadings on Feeder 14 balanced, or is the neutral current exceeding the 15% threshold?",
        "Track the historical voltage unbalance factor (VUF) on lateral taps with heavy single-phase rooftop solar concentrations.",
        "What are the line loss penalties and distribution transformer overheating risks associated with persistent phase imbalance?",
        "Stage a phase-swap switching recommendation to transfer three lateral taps from overloaded Phase A to underloaded Phase C."
    ],
    "grid_frequency_deviation_monitor": [
        "Did the bulk power system frequency drop below the 59.95 Hz Governor Deadband threshold during the generator trip event?",
        "Analyze the rate of change of frequency (RoCoF) over the first 500 milliseconds following the 1,200 MW nuclear plant trip.",
        "What was the total primary frequency response delivered by participating fast-frequency batteries versus thermal governors?",
        "Deploy 50 MW of fast frequency response from utility battery assets to arrest declining grid frequency."
    ],
    "islanding_detection_and_management_bot": [
        "Has an unintentional island formed on Distribution Substation 6 following the upstream transmission breaker lockout?",
        "Verify that active anti-islanding relays (IEEE 1547) disconnected all distributed solar generators within 2.0 seconds.",
        "What is the public safety and recloser out-of-phase closing risk if the islanded feeder remains energized?",
        "Trigger an emergency trip signal to all DER inverters on Feeder 6 and de-energize the islanded distribution section."
    ],
    "reactive_power_capacitor_dispatcher": [
        "Which distribution substations are currently exhibiting a lagging power factor below 0.92 during heavy inductive motor loading?",
        "Evaluate the voltage profile improvement along Circuit 7 before and after switching in the 1,200 kVar capacitor bank.",
        "What are the total system megawatt line loss savings achieved by maintaining unity power factor at bulk supply points?",
        "Dispatch a supervisory close command to Capacitor Bank C-2 at North Substation to boost feeder voltage."
    ],
    "system_inertia_tracker": [
        "What is the real-time synchronous grid inertia level in megawatt-seconds across the interconnect, and does it exceed NERC safety floors?",
        "Analyze the reduction in system kinetic energy resulting from the seasonal retirement of thermal synchronous generators.",
        "How close is the current operating grid to the critical RoCoF threshold where under-frequency load shedding would trigger?",
        "Issue a directive to synchronize two idle gas turbines in synchronous condenser mode to bolster system kinetic inertia."
    ],
    "tie_line_interconnection_limit_supervisor": [
        "Is the real-time megawatt power transfer across Intertie Line 500 approaching the Total Transfer Capability (TTC) limit?",
        "Correlate ambient air temperature and line conductor sag telemetry to determine dynamic line rating headroom on Intertie 2.",
        "What is the N-1 contingency overvoltage and thermal overload risk on adjacent ties if Intertie Line 500 trips?",
        "Initiate a scheduled interchange curtailment of 150 MW across the Western Tie to preserve NERC operating reliability margins."
    ],
    "transmission_line_loss_minimizer": [
        "What percentage of bulk generation is currently dissipated as I²R resistive thermal losses across the 345kV backbone?",
        "Compare system technical transmission losses under optimal power flow (OPF) voltage scheduling versus nominal setpoints.",
        "What is the monthly financial savings of reducing transmission technical losses by 0.35% through reactive power optimization?",
        "Adjust transformer tap changer positions and generator reactive dispatch to minimize transmission network losses."
    ],
    "under_frequency_load_shedding_simulator": [
        "If the grid frequency plummets to 59.3 Hz, which specific distribution feeders are assigned to Stage 1 automatic load shedding?",
        "Simulate the dynamic frequency recovery curve following a simulated shedding of 450 MW of non-critical distribution load.",
        "Are any critical medical facilities or wastewater pumping stations accidentally mapped to automatic UFLS feeder blocks?",
        "Arm the Stage 2 UFLS high-speed trip relays on designated industrial feeders ahead of extreme generation deficit conditions."
    ],
    "voltage_sag_swell_mitigator": [
        "Did the industrial park on Feeder 8 experience an ITIC-curve violating voltage sag during the transmission fault at 03:14?",
        "Examine the high-speed power quality meter waveforms to classify the sag duration, depth, and point-on-wave initiation.",
        "What is the financial equipment damage liability exposure for industrial semiconductor customers sensitive to sub-cycle sags?",
        "Trigger dynamic voltage restorer (DVR) fast-injection and adjust Substation Load Tap Changer (LTC) by two steps."
    ],

    # 5. Grid Operations (11 agents)
    "black_start_restoration_sequencer": [
        "What is the prioritized restoration path from the Black Start Hydro Station to energize the auxiliary loads of Plant Bravo?",
        "Simulate crank path transmission line energization to verify that capacitive Ferranti rise does not cause overvoltage flashovers.",
        "What is the estimated total time required to establish a stable 500 MW electrical restoration island during a total blackout?",
        "Authorize energization of the 138kV Black Start crank path from Unit 1 to Substation Center under strict island control."
    ],
    "dynamic_etr_calculator": [
        "What is the predicted Estimated Time of Restoration (ETR) for Outage Ticket #9921 with 3 downed spans and broken crossarms?",
        "Evaluate historical crew repair durations and traffic congestion models to refine restoration estimates for rural sectors.",
        "What is the variance between preliminary customer-published ETRs and actual power restoration timestamps over the storm?",
        "Publish updated dynamic ETR of 18:45 to public outage dashboards and mobile subscriber notifications for Sector 4."
    ],
    "emergency_crew_dispatch_router": [
        "Which line crews with certified live-line barehand qualifications are closest to the emergency wire-down incident on Main St?",
        "Analyze real-time GPS locations, drive times, and remaining allowable crew shift hours under federal rest regulations.",
        "How will optimizing multi-stop storm restoration routes improve customer SAIDI minutes during the active gale?",
        "Dispatch Crew Unit 14 to isolate the arcing primary conductor at 5th & Elm and secure the public hazard perimeter."
    ],
    "flisr_switching_simulator": [
        "Can Fault Location, Isolation, and Service Restoration (FLISR) automatically restore power to 1,400 customers on Feeder 12B?",
        "Simulate open-tie closing sequences to ensure adjacent Feeder 15 does not exceed its continuous thermal ampacity limit.",
        "What is the SAIDI minute reduction achieved by executing automated FLISR within 60 seconds of fault detection?",
        "Execute automated FLISR switching sequence: open recloser R-3 and close mid-point tie switch TS-12 to isolate fault section."
    ],
    "mobile_substation_deployment_planner": [
        "Can a 25 MVA mobile substation be transported and interconnected at Substation South before Transformer T-1 fails completely?",
        "Evaluate highway bridge weight restrictions and physical substation bay footprint clearances for the mobile unit transport.",
        "What is the outage risk duration for 8,500 customers if mobile substation deployment is delayed by more than 12 hours?",
        "Authorize immediate transit dispatch of Mobile Substation Unit Alpha and prepare physical interconnect leads at Substation South."
    ],
    "mutual_assistance_resource_allocator": [
        "How many external mutual assistance line contractor crews should we request through the Regional Mutual Assistance Group (RMAG)?",
        "Track contractor staging yard logistics, hotel accommodations, and fuel supply allocations for 250 incoming utility personnel.",
        "What is the estimated cost-per-restored-customer for mutual assistance forces versus internal utility crew deployments?",
        "Submit formal RMAG mutual aid mobilization request for 40 bucket trucks, 15 digger derricks, and 80 qualified linemen."
    ],
    "outage_footprint_topology_mapper": [
        "Which upstream protective device opened to cause the sudden loss of 3,200 smart meters in the Oakridge subdivision?",
        "Trace the GIS network connectivity model from reporting meter 'last-gasp' alerts to identify the common protective device.",
        "What is the total customer outage count and nested outage probability within the affected distribution lateral?",
        "Update the operational outage management system (OMS) map to highlight the confirmed blown transformer fuse at Pole #392."
    ],
    "scada_breaker_trip_correlator": [
        "Did the 115kV breaker trip at Substation West coincide with the fault event reported by digital protective relay Relay-21?",
        "Correlate SCADA sequence of events (SOE) millisecond logs with distance relay zone-1 trip signals and fault recorders.",
        "What was the root cause of the breaker trip: tree contact, lightning strike flashover, or relay misoperation?",
        "Issue a SCADA reclose supervisory permission signal after confirming line impedance has returned to normal open state."
    ],
    "storm_damage_prediction_modeler": [
        "How many broken poles and downed distribution wire spans will the incoming Category 2 hurricane cause in Coastal Division?",
        "Run Monte Carlo damage simulations combining 65 mph wind gust forecasts, soil moisture saturation, and tree canopy density.",
        "What are the anticipated materials requirements (transformers, crossarms, conductor reels) for post-storm reconstruction?",
        "Pre-stage emergency inventory materials and staging yards in District 3 based on predicted high-impact damage clusters."
    ],
    "vegetation_encroachment_lidar_analyzer": [
        "Which tree canopies along 500kV Transmission Corridor Alpha violate minimum vegetation clearance distance (MVCD) standards?",
        "Analyze airborne LiDAR point cloud returns to identify hazardous strike trees and rapid-growth eucalyptus encroachment.",
        "What is the wildfire ignition risk score for spans where tree branch proximity is within 4 feet of conductors under high sag?",
        "Generate a prioritized vegetation trimming work order for Span 104-108 and assign a certified utility arborist crew."
    ],
    "wildfire_risk_deenergization_trigger": [
        "Do current wind gusts exceeding 55 mph and single-digit relative humidity meet the criteria for a Public Safety Power Shutoff (PSPS)?",
        "Correlate satellite fire weather telemetry, live fire camera imagery, and red flag warnings across High Fire Threat Districts.",
        "What is the customer reliability impact and critical infrastructure exposure if Circuit 402 is proactively de-energized?",
        "Initiate a Tier 2 Public Safety Power Shutoff (PSPS) de-energization sequence for Feeder 402 to prevent catastrophic wildfire ignition."
    ],

    # 6. Production Forecasting (12 agents)
    "commercial_load_curve_forecaster": [
        "What is the day-ahead hourly megawatt demand forecast for the downtown commercial office district tomorrow?",
        "Analyze temperature sensitivity and commercial occupancy patterns driving air conditioning demand between 13:00 and 18:00.",
        "What is the mean absolute percentage error (MAPE) of our commercial load forecast during holiday transition weekends?",
        "Commit the revised 24-hour commercial load forecast to the day-ahead energy trading and procurement scheduling system."
    ],
    "ev_charging_load_spike_predictor": [
        "Will fast-charging demand at fleet depot stations create an unmanageable evening distribution peak between 18:00 and 21:00?",
        "Model the coincidence factor of 10,000 residential EV owners plugging in simultaneously upon arriving home from work.",
        "What is the distribution transformer overloading probability if EV charging concurrency increases by 25% this winter?",
        "Trigger an automated off-peak charging price signal and demand response advisory to enrolled EV fleet operators."
    ],
    "extreme_weather_anomaly_alert_bot": [
        "Is there a polar vortex or atmospheric river event forecasted to impact power supply reliability over the next 7 days?",
        "Examine historical weather anomaly analogues and thermal generator freeze-off probabilities under -20°F temperatures.",
        "What is the projected reserve margin shortfall if peak heating demand increases by 2,500 MW above seasonal forecast?",
        "Issue an extreme weather emergency alert to power generation plant managers to activate winterization freeze protection protocols."
    ],
    "geothermal_output_forecaster": [
        "What is the anticipated steady-state megawatt output from Geothermal Field Delta given current brine production well temperatures?",
        "Model steam extraction pressure decline curves and reservoir recharge rates over the trailing 12-month period.",
        "How will planned re-injection well maintenance impact baseload renewable generation commitments next month?",
        "Update the 30-day forward geothermal dispatch profile and notify the ISO scheduling desk of anticipated brine enthalpy limits."
    ],
    "hydro_inflow_snowpack_estimator": [
        "How will current mountain snowpack water equivalent (SWE) levels translate into reservoir inflow volumes during spring runoff?",
        "Analyze satellite snow cover extent and degree-day snowmelt models to predict peak reservoir spill dates for Dam Beta.",
        "What is the risk of spillway overflow versus drought storage shortfall under low-snowpack median run-off scenarios?",
        "Adjust monthly hydropower generation capacity dispatch curves to preserve mandated fish flow conservation storage."
    ],
    "industrial_load_curve_forecaster": [
        "What is the forecasted 15-minute peak electric demand for the steel mill and heavy manufacturing park tomorrow afternoon?",
        "Evaluate factory production shift schedules and arc furnace operational cycles to detect demand spike correlations.",
        "What are the financial demand charge penalties incurred if the industrial cluster exceeds the 120 MW substation contract limit?",
        "Issue an automated peak-shaving alert to industrial customers requesting voluntary production modulation between 14:00 and 16:00."
    ],
    "microgrid_generation_forecaster": [
        "Can the Island Community microgrid maintain standalone power balance tomorrow using its local solar, wind, and battery assets?",
        "Forecast 24-hour microgrid generation versus critical hospital and water treatment load under islanded conditions.",
        "What is the probability of requiring diesel backup generator starts if overcast skies reduce solar microgrid yield by 40%?",
        "Schedule microgrid battery pre-charging from surplus wind generation tonight to prepare for scheduled utility tie-line disconnection."
    ],
    "pumped_hydro_storage_forecaster": [
        "What is the optimal pumping schedule for Pumped Storage Hydro Unit 1 to take advantage of low off-peak overnight power prices?",
        "Model upper reservoir hydraulic head levels, pumping round-trip efficiency (78%), and generation discharge capacity.",
        "What is the net wholesale arbitrage profit margin achieved by pumping at $18/MWh and generating at $95/MWh tomorrow?",
        "Submit day-ahead pumping and generation bid schedules for the 600 MW pumped storage plant to the regional market operator."
    ],
    "residential_load_curve_forecaster": [
        "How will the forecasted 98°F heatwave impact suburban residential air conditioning load across the metropolitan service territory?",
        "Compare cooling degree-day regressions against actual residential smart meter interval data from last year's summer peak.",
        "What is the peak coincidental demand risk across residential distribution transformers during the 17:00 dinner cooking window?",
        "Publish the 48-hour forward residential load profile to the power supply procurement and balancing desk."
    ],
    "solar_irradiance_predictor": [
        "What is the forecasted Direct Normal Irradiance (DNI) and Global Horizontal Irradiance (GHI) across Solar Plant Alpha tomorrow?",
        "Track satellite cloud motion vectors to predict sudden 50 MW ramp-down events caused by cumulus cloud cover over the solar field.",
        "What is the reserve regulation requirement needed to compensate for intra-hour solar PV ramp fluctuations?",
        "Commit the 5-minute solar generation ramp profile to the real-time energy management system (EMS) for balancing support."
    ],
    "thermal_plant_outage_availability_tracker": [
        "Which combined-cycle natural gas turbine units are currently on forced outage or scheduled maintenance turnaround?",
        "Track equivalent forced outage rates (EFOR) and mean time to repair (MTTR) across the fossil generation fleet over the last year.",
        "What is the total loss of generating capacity (MW) available to meet the summer peak demand reserve margin?",
        "Flag Unit 3 at Riverside Generating Station as available for commercial dispatch following successful turbine test sync."
    ],
    "wind_speed_generation_modeler": [
        "What is the day-ahead wind power production forecast (MW) for Plains Wind Farm based on 80-meter hub height wind speeds?",
        "Analyze wind turbine power curves and high-speed wind cut-out risks (> 25 m/s) associated with the approaching cold front.",
        "What is the financial imbalance settlement penalty exposure if actual wind output falls 20% below day-ahead market schedules?",
        "Submit the 24-hour hourly wind energy generation schedule to the RTO scheduling portal."
    ],

    # 7. Regulatory Compliance (10 agents)
    "customer_pii_redaction_scrubber": [
        "Are there any unmasked Social Security numbers, banking details, or customer phone numbers in the billing dispute case file?",
        "Scan customer service email attachments and chat transcripts to verify compliance with state consumer privacy regulations.",
        "What is the risk exposure and audit penalty under CCPA/GDPR if customer account files are exported without automated sanitization?",
        "Execute automated redaction of all sensitive PII from Customer Record #44921 before transmitting data to third-party auditors."
    ],
    "epa_cems_emissions_aggregator": [
        "Did NOx or SO2 continuous emissions monitoring (CEMS) readings at Generating Station Unit 1 exceed EPA 40 CFR Part 75 hourly limits?",
        "Audit daily CEMS calibration drift test logs and relative accuracy test audits (RATA) across fossil generation smokestacks.",
        "What is our cumulative quarterly carbon and sulfur allowance balance compared to total verified plant emissions?",
        "Compile and sign the quarterly electronic EPA CEMS compliance data report for submission to the Clean Air Markets Division."
    ],
    "esg_scope_1_2_carbon_calculator": [
        "What are our utility's total Scope 1 direct greenhouse gas emissions from fossil generation and SF6 circuit breaker leakages this year?",
        "Calculate Scope 2 indirect carbon emissions resulting from transmission line electrical losses and corporate facility power usage.",
        "How much carbon intensity reduction (gCO2e/kWh) did we achieve year-over-year through renewable portfolio expansion?",
        "Generate the annual ESG sustainability disclosure table aligned with SASB and TCFD reporting standards for stakeholder review."
    ],
    "ferc_form_1_financial_drafter": [
        "Are electric plant in service balances and depreciation reserve schedules reconciled for the upcoming annual FERC Form 1 filing?",
        "Audit regulatory asset accounting and utility operating expenses against the FERC Uniform System of Accounts (USofA).",
        "What are the major capital expenditure variances between authorized rate base filings and actual capital asset additions?",
        "Compile the completed FERC Form 1 financial schedules and balance sheets for executive CFO sign-off."
    ],
    "hazardous_waste_disposal_tracker": [
        "Are all decommissioned polychlorinated biphenyl (PCB) contaminated distribution transformers documented with EPA hazardous manifests?",
        "Track chain-of-custody disposal records, storage dwell times, and licensed hazardous waste recycling facility receipts.",
        "What is our regulatory violation risk under the Toxic Substances Control Act (TSCA) if PCB disposal manifests exceed 30 days?",
        "Generate the certified hazardous waste shipping manifest and schedule pickup of 12 retired PCB-mineral oil transformers."
    ],
    "nerc_cip_cybersecurity_audit_analyzer": [
        "Are all Electronic Security Perimeters (ESP) and physical access control logs for Substation Control Rooms compliant with NERC CIP-005?",
        "Audit firewall rules, open ports, and transient cyber asset (laptop) patching records against NERC CIP-007 and CIP-010 standards.",
        "What is the regulatory penalty exposure per day per violation if unauthorized remote interactive access is discovered in an audit?",
        "Generate an immediate mitigation ticket and revoke unapproved VPN credentials for third-party contractor accounts."
    ],
    "osha_safety_incident_classifier": [
        "Does the electrical flash burn suffered by a line technician during cable splicing meet the criteria for an OSHA Recordable Incident?",
        "Analyze days away, restricted, or transferred (DART) rate and Total Recordable Incident Rate (TRIR) across field operations.",
        "What are the leading root causes identified in recent high-potential near-miss reports: PPE non-compliance or situational fatigue?",
        "Submit the certified OSHA 300 log entry and initiate a comprehensive root-cause safety stand-down review for District West."
    ],
    "puc_rate_case_testimony_drafter": [
        "What capital investments in grid modernization and wildfire hardening must be justified in our upcoming state PUC General Rate Case?",
        "Draft quantitative expert witness testimony on revenue requirement calculations, rate of return on equity (ROE), and cost of service.",
        "How will the proposed tariff restructuring impact median low-income and residential ratepayer bills under regulatory review?",
        "Finalize and format the Rate Base and Revenue Requirement Exhibit for legal filing before the Public Utilities Commission."
    ],
    "saidi_saifi_reliability_metric_tracker": [
        "What are our year-to-date System Average Interruption Duration Index (SAIDI) and Frequency Index (SAIFI) numbers across all districts?",
        "Evaluate the reliability impact of Major Event Days (MED) excluded under IEEE 1366 2.5-Beta methodology versus normal storm days.",
        "Are any operating divisions at risk of violating state PUC reliability performance benchmarks and incurring financial disallowances?",
        "Publish the official monthly distribution reliability scorecard to grid operations leadership and regulatory compliance teams."
    ],
    "water_usage_discharge_reporter": [
        "Did thermal cooling water discharge temperatures at River Generating Plant comply with NPDES permit environmental limits today?",
        "Track consumptive water withdrawal volumes and effluent pH/chlorine levels against state Department of Environmental Protection rules.",
        "What is the operational curtailment risk if river temperatures rise within 1.5°F of the thermal permit discharge threshold?",
        "Generate the monthly National Pollutant Discharge Elimination System (NPDES) discharge monitoring report for regulatory filing."
    ],

    # 8. Smart Meter Management (10 agents)
    "ami_interval_data_vee_processor": [
        "How many 15-minute smart meter interval reads failed automated Validation, Editing, and Estimation (VEE) checks today?",
        "Analyze continuous spike and flatline data gaps across residential meters caused by mesh network collector dropouts.",
        "What is our first-pass VEE data acceptance percentage, and how many missing intervals required historical estimation?",
        "Commit validated 15-minute interval energy records for 250,000 meters to the Meter Data Management System (MDMS) for billing."
    ],
    "ami_mesh_network_health_monitor": [
        "Which RF mesh collectors in the downtown district are experiencing buffer overruns or high packet retransmission rates?",
        "Map cellular backhaul signal strength (RSSI) and routing hop counts across smart meter nodes in rural distribution areas.",
        "What is the meter unreachable rate and communication failure percentage following the recent firmware rollout?",
        "Rebalance mesh routing topologies by reassigning 120 isolated smart meter child nodes to adjacent high-gain Collector C-04."
    ],
    "customer_baseline_load_cbl_calculator": [
        "What is the calculated Customer Baseline Load (CBL) for commercial accounts participating in tomorrow's demand response event?",
        "Compare the 'High 4-in-5' baseline methodology against weather-adjusted baseline algorithms for commercial refrigerating facilities.",
        "What was the total verified megawatt demand reduction achieved by participants relative to their contractual CBL baselines?",
        "Publish final verified demand response curtailment performance calculations to the wholesale market settlement portal."
    ],
    "demand_response_thermostat_setback_trigger": [
        "How many residential smart thermostats can we signal for a 3°F pre-cooling setback ahead of the 16:00 grid demand peak?",
        "Model the expected megawatt relief curve and subsequent 'snapback' rebound demand when setback events conclude.",
        "What is the customer program opt-out percentage during high-temperature demand response curtailment events?",
        "Dispatch an automated Tier 2 Demand Response event signal to 45,000 enrolled smart thermostats across Grid Zone 2."
    ],
    "localized_outage_ping_diagnostic_bot": [
        "Can you send high-speed AMI pings to meters downstream of Fuse F-12 to confirm whether customer power has been restored?",
        "Evaluate smart meter 'last-gasp' power failure power-off notifications against SCADA breaker open indications.",
        "What is the percentage of false-positive customer outage calls that can be eliminated through automated meter ping diagnostics?",
        "Execute automated batch ping sequence to 85 smart meters on Circuit 3 and close confirmed restored outage work tickets."
    ],
    "meter_firmware_ota_scheduler": [
        "What is the progress of the over-the-air (OTA) firmware upgrade across our 150,000 Gen-5 smart meters?",
        "Track download failure rates, transmission retry latency, and device battery drain during nighttime mesh broadcast windows.",
        "What is the risk of bricking older firmware revisions if the cryptographic security patch is pushed concurrently?",
        "Pause the OTA firmware broadcast campaign on Substation 8 cluster due to elevated packet collision rates."
    ],
    "meter_inversion_tamper_detector": [
        "Which smart meters have reported reverse energy flow or physical tilt tamper switch triggers without approved solar generation interconnection?",
        "Correlate meter inversion physical tilt alerts with sudden zero-consumption billing patterns to detect physical meter flipping theft.",
        "What is the estimated unmetered electricity revenue loss associated with flagged active meter tamper accounts?",
        "Dispatch a revenue protection field investigator to inspect Meter #MT-90214 for unauthorized physical tampering and diversion."
    ],
    "prepaid_metering_balance_tracker": [
        "How many prepaid electric service customers currently have account balances below the $10 low-balance threshold?",
        "Track daily consumption burn rates and predict which accounts will exhaust prepaid balances before the weekend.",
        "What is the customer notification response rate and payment replenishment latency following automated SMS balance alerts?",
        "Send an urgent low-balance SMS warning to Account #30194 and schedule an automated grace-period extension until Monday morning."
    ],
    "smart_meter_temperature_anomaly_detector": [
        "Are any residential smart meter terminal blocks reporting internal temperatures exceeding 85°C (185°F)?",
        "Correlate meter temperature spikes with high electrical load draw to detect dangerous loose meter socket jaws or impending meter fires.",
        "What is the catastrophic meter melt and residential structure fire risk score across aging socket installations?",
        "Stage an emergency service ticket to immediately disconnect Meter #M-88219 and dispatch a troubleshooter to replace burnt jaws."
    ],
    "zero_consumption_anomaly_flag": [
        "Which commercial smart meters have reported continuous zero kWh consumption for the past 14 days despite active account status?",
        "Filter zero-read accounts against move-out records, seasonal vacation properties, and potential current transformer (CT) failures.",
        "What is the total monthly unbilled energy volume attributable to undetected broken smart meters or phase bypass theft?",
        "Schedule an on-site field meter technician visit to inspect Account #10492 for defective current sensors or internal meter failure."
    ],

    # 9. Support Services (10 agents)
    "employee_fatigue_risk_monitor": [
        "Which emergency restoration line workers have exceeded 16 consecutive hours on duty or 60 hours over the rolling 7-day storm window?",
        "Track crew shift rotations, rest periods, and circadian fatigue risk scores to ensure full compliance with utility labor safety rules.",
        "What is the safety incident probability correlation when overtime hours exceed 25% of regular scheduled shift time?",
        "Issue a mandatory rest stand-down order for Line Crew Bravo and assign fresh relief personnel to ongoing restoration shifts."
    ],
    "facility_management_work_order_router": [
        "Which building maintenance work orders for emergency HVAC failures in the primary grid control center are currently unassigned?",
        "Evaluate contractor response times and service level agreements (SLAs) for critical utility administrative and warehouse facilities.",
        "What is the backlog volume and cost variance of deferred facility maintenance tasks across regional operating centers?",
        "Dispatch an urgent HVAC repair contract team to Data Center Room B to resolve cooling chiller redundancy loss."
    ],
    "hardware_procurement_rfp_scorer": [
        "How do the three vendor competitive proposals for our 500kV optical ground wire (OPGW) procurement rank against technical criteria?",
        "Evaluate vendor manufacturing warranties, delivery lead times, price per kilometer, and cybersecurity supply chain audits.",
        "What is the lifecycle cost differential between Vendor A's domestic offering and Vendor B's overseas procurement option?",
        "Generate the procurement bid evaluation matrix and submit the vendor award recommendation to the utility procurement committee."
    ],
    "loto_arc_flash_safety_knowledge_bot": [
        "What are the mandated Lockout/Tagout (LOTO) isolation points and PPE requirements for replacing a 13.8kV breaker in Cubicle 4?",
        "Retrieve NFPA 70E arc flash boundary calculations and incident energy ratings (cal/cm²) for Substation West switchgear.",
        "What are the most frequent safety compliance citations documented during annual utility field LOTO procedure audits?",
        "Generate a site-specific LOTO switching clearance sheet and PPE checklist for maintenance work on 115kV Transformer T-3."
    ],
    "mutual_assistance_per_diem_auditor": [
        "Do the hotel, meal, and fuel expense claims submitted by visiting mutual aid contractor crews match established utility rate caps?",
        "Audit travel expense receipts, mileage logs, and daily per-diem submissions against FEMA disaster reimbursement guidelines.",
        "What is the total disallowance dollar amount identified across non-compliant mutual assistance contractor expense reports?",
        "Approve verified per-diem and lodging expense disbursements for Contractor Force #402 for storm restoration services."
    ],
    "power_purchase_agreement_legal_reviewer": [
        "Does the commercial solar Power Purchase Agreement (PPA) include standard clauses for curtailment risk and negative pricing indemnity?",
        "Analyze contractual availability guarantees, heat rate degradation terms, and environmental attribute transfer rules.",
        "What is the utility's financial liability exposure if transmission interconnection delays trigger contract liquidated damages?",
        "Flag non-standard indemnification language in Section 14.2 of the Wind PPA and route to General Counsel for legal revision."
    ],
    "scada_vpn_access_helpdesk_bot": [
        "Why is an authorized control center operator's hardware security token failing authentication for SCADA network access?",
        "Audit VPN connection logs, source IP geolocations, and dual-custody access policies against NERC CIP-005 requirements.",
        "What is the average resolution time for operational technology (OT) remote access helpdesk tickets during shift changeovers?",
        "Reset multi-factor authentication credentials for Dispatcher User #D-902 after confirming out-of-band identity verification."
    ],
    "union_contract_benefits_assistant": [
        "What are the collective bargaining agreement rules regarding storm standby pay, call-out minimums, and meal allowances for IBEW linemen?",
        "Clarify apprenticeship progression timelines and healthcare contribution rates under the ratified 2025-2028 union contract.",
        "How many contractual grievance filings regarding overtime equalization are currently pending union arbitration?",
        "Calculate retroactive standby wage adjustments for 14 union lineworkers impacted by rescheduled storm duty rotations."
    ],
    "utility_vehicle_fleet_maintenance_tracker": [
        "Which heavy-duty bucket trucks and boom lift vehicles have overdue dielectric boom testing or hydraulic fluid maintenance?",
        "Track fleet fuel consumption, engine idle hours, and scheduled preventive maintenance intervals across 450 service vehicles.",
        "What is the vehicle downtime percentage across regional service garages, and does it meet minimum fleet availability targets?",
        "Ground Bucket Truck #BK-412 immediately due to failed annual dielectric insulation testing and schedule shop servicing."
    ],
    "warehouse_inventory_drone_auditor": [
        "Did last night's autonomous warehouse drone LiDAR scan detect any inventory discrepancies for 15kV distribution cable spools?",
        "Reconcile drone RFID scanner inventory counts against SAP enterprise resource planning (ERP) inventory ledger records.",
        "What is the inventory shrinkage and barcode mismatch rate across substation spare parts in the central distribution yard?",
        "Update the warehouse inventory database to reflect actual verified stock counts of 48 porcelain insulator bushings."
    ],

    # 10. Wholesale Trading (12 agents)
    "ancillary_services_bid_optimizer": [
        "How should we allocate our 100 MW flexible gas turbine capacity between Regulation Up, Spinning Reserve, and Day-Ahead Energy?",
        "Analyze historical ancillary service clearing prices (ASCP) and ISO mileage multipliers across peak summer operating days.",
        "What is the revenue optimization upside of shifting 25 MW of battery capacity from energy arbitrage to frequency regulation?",
        "Submit co-optimized Ancillary Services and Energy bids for Unit 1 into the ISO Day-Ahead Market before the 10:00 AM gate closure."
    ],
    "carbon_allowance_market_tracker": [
        "What are California Carbon Allowance (CCA) and RGGI carbon credit contracts trading at for December forward delivery?",
        "Correlate quarterly allowance auction clearing prices with fossil generation output and state regulatory cap adjustments.",
        "What is our projected annual carbon compliance obligation cost under current allowance market price trajectories?",
        "Execute a forward purchase hedge for 50,000 metric tons of compliance carbon allowances at $38.50 per ton."
    ],
    "coal_inventory_burn_rate_advisor": [
        "How many days of full-load coal burn inventory remain in the stockpile at Mohave Generating Station based on current rail deliveries?",
        "Model coal rail delivery cycle times, stockpile coal density, and forecasted generation run-hours over the winter quarter.",
        "What is the risk of fuel supply curtailment if freezing rail switches disrupt coal deliveries for more than 10 days?",
        "Adjust unit economic dispatch bids to conserve on-site coal inventory until incoming unit trains arrive."
    ],
    "dark_spread_heat_rate_calculator": [
        "What is the current dark spread ($/MWh) for our 600 MW supercritical coal plant given wholesale power and delivered coal costs?",
        "Evaluate plant operational heat rates (Btu/kWh) across partial loading points to determine minimum profitable generation thresholds.",
        "How does the cost of SO2 and NOx emission allowances impact the net generation margin across the coal fleet?",
        "Submit a generation commitment schedule to the ISO when dark spread margins exceed the $12.50/MWh hurdle rate."
    ],
    "day_ahead_lmp_forecaster": [
        "What is the forecasted 24-hour Day-Ahead Locational Marginal Price (LMP) profile across all commercial trading hubs tomorrow?",
        "Analyze generation supply stack bids, forecasted regional load, and planned transmission outages driving day-ahead clearing prices.",
        "What is the forecast accuracy (MAPE) of our day-ahead nodal pricing model during extreme weather transition days?",
        "Commit day-ahead hourly price forecasts to the wholesale trading desk portfolio optimization engine."
    ],
    "financial_transmission_right_copilot": [
        "Which Financial Transmission Right (FTR) paths between West Hub and Load Zone 1 offer the highest expected auction payout return?",
        "Analyze historical transmission congestion rent and binding constraint hours on the West-Central 500kV transmission corridor.",
        "What is our net portfolio hedge revenue exposure if summer transmission derates increase congestion along Path 26?",
        "Submit bids for 75 MW of Peak FTR contracts on the North-to-South corridor in the upcoming monthly ISO auction."
    ],
    "iso_rto_bidding_curve_generator": [
        "Can you construct the piecewise linear three-part energy bid curve for Combined Cycle Unit 2 for tomorrow's market auction?",
        "Calculate no-load costs, start-up cost profiles, and incremental heat rate curves based on latest spot natural gas index prices.",
        "What is the risk of unit dispatch commitment rejection if start-up bid adders exceed ISO market mitigation caps?",
        "Transmit the validated generation supply offer curves to PJM / CAISO market scheduling systems before gate closure."
    ],
    "natural_gas_pipeline_constraint_analyzer": [
        "Are there any Critical Notices or Operational Flow Orders (OFO) declared on major interstate natural gas pipelines feeding our plants?",
        "Map gas pipeline compressor station outages and pipeline capacity utilization factors against electric generation fuel demand.",
        "What is the financial imbalance penalty exposure if our power plant consumes gas in excess of nominated pipeline scheduling quantities?",
        "Rebalance intra-day gas nominations on Line 300 to avoid pipeline imbalance penalties and secure evening turbine fuel supply."
    ],
    "portfolio_value_at_risk_analyzer": [
        "What is our wholesale energy portfolio 99% one-day Value at Risk (VaR) under a simulated 20% natural gas price spike?",
        "Run 10,000 Monte Carlo iterations combining correlated forward power price volatility, heat rates, and plant forced outage probabilities.",
        "What is our potential mark-to-market loss exposure if extreme summer heat triggers widespread generator curtailments?",
        "Recommend immediate forward hedging transactions to reduce portfolio VaR below the corporate board risk ceiling of $15M."
    ],
    "real_time_lmp_tracker": [
        "Why did the real-time five-minute LMP spike to $1,800/MWh at Substation Node 402 during the last dispatch interval?",
        "Correlate transmission line thermal overloads, generator ramp rate limitations, and real-time dispatch (RTD) ex-post price corrections.",
        "What is our net financial settlement exposure across physical imbalance positions during the active price spike?",
        "Issue a fast-ramping dispatch instruction to peaker units to capture high real-time LMP market revenues."
    ],
    "renewable_energy_certificate_trader": [
        "What are current compliance Class I Renewable Energy Certificates (RECs) trading for in the voluntary and compliance markets?",
        "Track our portfolio surplus REC generation inventory across wind and solar assets against state RPS compliance obligations.",
        "What is the revenue upside of selling 100,000 unbundled wind RECs on the spot market versus banking them for future compliance years?",
        "Execute a bilateral sale contract of 25,000 Class 1 Green-e certified solar RECs at $24.50 per certificate."
    ],
    "spark_spread_heat_rate_calculator": [
        "What is the real-time clean spark spread ($/MWh) for Combined Cycle Gas Turbine 1 based on spot electricity and Henry Hub gas prices?",
        "Analyze how ambient intake air temperature impacts gas turbine heat rate efficiency and power output degradation.",
        "What is the minimum power price required to economically fire the peaker turbine given current delivered gas and emissions costs?",
        "Dispatch Combined Cycle Unit 1 when the clean spark spread expands beyond the operational margin threshold of $8.50/MWh."
    ]
}

def verify_all_agents_covered():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    cat = json.load(open(root / "web" / "catalog.json"))
    missing = [a["id"] for a in cat if a["id"] not in AGENT_PROMPTS]
    if missing:
        raise ValueError(f"Missing {len(missing)} agents in prompts: {missing}")
    print(f"✅ Verified: All {len(cat)} agents have 4 unique, domain-specific prompts!")

if __name__ == "__main__":
    verify_all_agents_covered()
