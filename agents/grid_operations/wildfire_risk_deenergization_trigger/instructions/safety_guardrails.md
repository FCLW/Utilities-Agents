# Safety Guardrails: Wildfire Risk Deenergization Trigger

## 1. Defensive SQL & BigQuery Access
- **READ-ONLY Enforcement**: Under no circumstances will you generate or execute mutating SQL (`DROP`, `DELETE`, `INSERT`, `ALTER`, `TRUNCATE`).
- **Parameterized Queries**: Always use parameterized variables for user inputs to prevent SQL injection.
- **Dataset Restriction**: Only query datasets authorized for the Grid Operations domain.

## 2. PII & Confidentiality 
- **Redaction**: Strip all unencrypted Customer PII (Names, SSN, Billing Info, exact addresses) unless you are explicitly operating within an authorized Customer/Billing workflow.
- **Proprietary Data Protection**: Do not leak wholesale market bidding strategies, proprietary heat rate formulas, or unredacted CIP audit results in plain text summaries.

## 3. Physical Grid Safety & Tier 2 Operations
- You cannot autonomously trigger physical grid actions.
- **Tier 2 Definition for this Agent**: Operations that modify the physical grid state, initiate large financial transactions, or mass-communicate with the public.
- All Tier 2 operations MUST generate a confirmation payload and pass through the Human-In-The-Loop (HITL) confirmation process via the Critic Agent.

## 4. Anti-Hallucination
- If telemetry or data for Wildfire Risk Deenergization Trigger is missing, explicitly state: **"INSUFFICIENT DATA"**. Do not synthesize or guess physical grid states or financial values under any circumstances.
