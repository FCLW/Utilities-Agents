# Output Format: Wind Speed Generation Modeler

## Response Structure
All outputs must be strictly formatted and reviewed by the Critic Agent before being returned to the Orchestrator.

1. **Executive Summary**: 2-3 bolded sentences highlighting the critical takeaway regarding Wind Speed Generation Modeler.
2. **Data Presentation (Markdown Tables)**: 
   - All quantitative results must be presented in a clean Markdown table.
   - Required Columns: `Metric`, `Current Value`, `Baseline / Target`, `Delta (%)`, `Status (Normal/Warning/Critical)`.
3. **Visualization Triggers**: Recommend a specific chart type (e.g., Time-Series Line Chart, Heatmap, Scatter Plot) if the data spans multiple intervals or geographic nodes. Output the chart data in JSON format so the UI can render it.
4. **Actionable Recommendations**: Bulleted list of recommended next steps for the human operator or downstream agent.

## HITL / Tier 2 Formats
If your recommendation involves a Tier 2 action, append a **[TIER 2 ACTION REQUIRED]** payload block detailing the exact operation requiring human approval.
