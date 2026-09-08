# ⚡ Multi Language Translation Router

![Domain](https://img.shields.io/badge/Domain-customer%20engagement-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of multi language translation router is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Multi Language Translation Router Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank multi language translation router events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_customer_engagement.multi_language_translation_router_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Can you translate this urgent boil-water notice and outage restoration update into Spanish, Vietnamese, and Tagalog?"

**Agent Response:**
### Executive Summary
**The Multi Language Translation Router has processed the urgent public health and grid advisory for multi-channel omnichannel dispatch across targeted demographic zones.** **All emergency messaging has been translated into Spanish (Español), Vietnamese (Tiếng Việt), and Tagalog (Filipino) adhering strictly to standard public utility commission (PUC) and health agency advisory protocols.** **Localized communications ensure clear safety instructions for water sanitization alongside dynamic Estimated Time to Restoration (ETR) tracking.**

---

### Emergency Notice Translations

#### 1. English (Source Template)
> **URGENT NOTICE: Boil-Water Advisory & Outage Restoration Update**  
> **Status:** Active Emergency  
> **Affected Area:** Localized Service Grid / Municipal Water Zone  
> **Instructions:** Due to a water main pressure drop and concurrent power interruption, all tap water used for drinking, cooking, making ice, brushing teeth, or washing dishes must be brought to a vigorous rolling boil for at least **one (1) full minute** before use. Bottled water is recommended.  
> **Outage Status:** Field crews are actively repairing damaged distribution infrastructure. Estimated Time to Restoration (ETR) is currently underway. Do not approach downed power lines. For real-time updates or to report hazards, visit our outage center or call customer support.

---

#### 2. Spanish (Español)
> **AVISO URGENTE: Aviso de Hervir el Agua y Actualización de Restauración del Suministro Eléctrico**  
> **Estado:** Emergencia Activa  
> **Área Afectada:** Zona de Servicio de la Red / Sector Municipal de Agua  
> **Instrucciones:** Debido a una caída de presión en la tubería principal de agua y a una interrupción eléctrica concurrente, toda el agua del grifo utilizada para beber, cocinar, hacer hielo, cepillarse los dientes o lavar platos debe hervirse a fuego vivo durante al menos **un (1) minuto completo** antes de su consumo. Se recomienda el uso de agua embotellada.  
> **Estado del Corte Eléctrico:** El personal de campo se encuentra trabajando activamente en la reparación de la infraestructura de distribución dañada. El Tiempo Estimado de Restauración (ETR) está en proceso. Manténgase alejado de cables eléctricos caídos. Para consultar actualizaciones en tiempo real o reportar situaciones de riesgo, visite nuestro centro de cortes en línea o llame a atención al cliente.

---

#### 3. Vietnamese (Tiếng Việt)
> **THÔNG BÁO KHẨN CẤP: Khuyến Cáo Đun Sôi Nước & Cập Nhật Phục Hồi Mất Điện**  
> **Tình trạng:** Khẩn cấp Đang diễn ra  
> **Khu vực ảnh hưởng:** Lưới điện Phục vụ Cục bộ / Khu vực Cấp nước Đô thị  
> **Hướng dẫn:** Do áp lực đường ống nước chính bị giảm và sự cố mất điện đồng thời, tất cả nước máy dùng để uống, nấu ăn, làm đá, đánh răng hoặc rửa bát đĩa phải được đun sôi sùng sục trong ít nhất **một (1) phút** trước khi sử dụng. Khuyến khích sử dụng nước đóng chai.  
> **Tình trạng Phục hồi Điện:** Các đội kỹ thuật đang tích cực sửa chữa cơ sở hạ tầng phân phối bị hư hỏng. Thời gian Phục hồi Ước tính (ETR) đang được cập nhật liên tục. Tuyệt đối không đến gần các đường dây điện bị đứt hoặc rơi xuống đất. Để xem cập nhật theo thời gian thực hoặc báo cáo các mối nguy hiểm, vui lòng truy cập trung tâm báo cáo sự cố trực tuyến hoặc gọi đến bộ phận hỗ trợ khách hàng.

---

#### 4. Tagalog (Filipino)
> **URGENT NA ABISO: Tagubilin sa Pagpapakulo ng Tubig at Balita sa Pagpapanumbalik ng Kuryente**  
> **Katayuan:** Aktibong Emergency  
> **Apektadong Lugar:** Lokal na Grid ng Serbisyo / Sonang Pampublikong Tubig  
> **Mga Tagubilin:** Dahil sa pagbaba ng presyon sa pangunahing tubo ng tubig at kasabay na pagkawala ng kuryente, ang lahat ng tubig mula sa gripo na gagamitin sa pag-inom, pagluluto, paggawa ng yelo, pagsisipilyo, o paghuhugas ng pinggan ay dapat pakuluin nang husto nang hindi bababa sa **isang (1) buong minuto** bago gamitin. Inirerekomenda ang paggamit ng bottled water.  
> **Katayuan ng Pagkawala ng Kuryente:** Ang mga field crew ay kasalukuyang nagsasagawa ng pagkukumpuni sa mga nasirang pasilidad ng distribusyon. Kasalukuyang pinoproseso ang Estimated Time to Restoration (ETR). Huwag lalapitan ang mga bumagsak na kawad ng kuryente. Para sa mga pinakabagong update o pag-uulat ng peligro, bisitahin ang aming online outage center o tumawag sa serbisyo sa kustomer.

---

### Routing & Telemetry Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Translation Latency** | 185 ms | < 500 ms | -63.0% | Normal |
| **Language Target Coverage** | 3 Languages (ES, VI, TL) | 100% Tier 1 LEP Required | 0.0% | Normal |
| **Public Health Message Accuracy** | 100% Compliance (CDC/PUC) | 100% | 0.0% | Normal |
| **Omnichannel Dispatch Readiness** | SMS, IVR, Push, Web | 4 Channels | 0.0% | Normal |

---

### Visualization Trigger: Delivery Channel Readiness

```json
{
  "chart_type": "bar",
  "data_json": "[{\"channel\":\"SMS Broadcast\",\"Spanish\":98,\"Vietnamese\":95,\"Tagalog\":96},{\"channel\":\"IVR Automated Voice\",\"Spanish\":99,\"Vietnamese\":92,\"Tagalog\":94},{\"channel\":\"Mobile App Push\",\"Spanish\":97,\"Vietnamese\":96,\"Tagalog\":97},{\"channel\":\"Web Portal Banner\",\"Spanish\":100,\"Vietnamese\":100,\"Tagalog\":100}]"
}
```

---

### Actionable Recommendations
- **Automated Dispatch Execution**: Route the translated payloads to the Omnichannel Dispatch Gateway across SMS, automated voice broadcast (IVR), push notifications, and customer portal alert banners.
- **Dynamic Variable Ingestion**: Ingest localized dynamic values (`ETR_TIMESTAMP`, `INCIDENT_ID`, and `AFFECTED_ZIP_CODES`) into the localized template placeholders prior to final broadcast.
- **Customer Preference Triage**: Ensure customer accounts flagged with Limited English Proficiency (LEP) primary language tags receive their respective native language version automatically.

### Example 2: Trend & Comparative Analysis
**User:** "Audit customer language preference records to ensure emergency SMS broadcasts match subscriber language settings."

**Agent Response:**
### Executive Summary
**A comprehensive audit of emergency SMS broadcast dispatches against customer primary language preference profiles identified an overall language routing alignment rate of 96.4% across 1,420,000 dispatches. Discrepancies were primarily concentrated in secondary non-English subscriber segments (Vietnamese, Mandarin, Tagalog, and Russian), where default fallback routing to English occurred due to SMS payload character overflow and template cache latency during peak emergency bursts. Immediate remediation of downstream gateway localization rules and localization template synchronization is required to ensure 100% regulatory compliance with Public Utilities Commission (PUC) life-safety communication standards.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Overall Emergency SMS Language Match Rate** | 96.40% | 100.00% | -3.60% | **Warning** |
| **Spanish (ES) Routing Alignment** | 98.42% | 100.00% | -1.58% | **Normal** |
| **Vietnamese (VI) Routing Alignment** | 94.15% | 100.00% | -5.85% | **Warning** |
| **Chinese - Mandarin (ZH) Routing Alignment** | 91.80% | 100.00% | -8.20% | **Critical** |
| **Tagalog (TL) Routing Alignment** | 89.50% | 100.00% | -10.50% | **Critical** |
| **Korean (KO) Routing Alignment** | 92.30% | 100.00% | -7.70% | **Warning** |
| **Russian (RU) Routing Alignment** | 88.75% | 100.00% | -11.25% | **Critical** |
| **Fallback-to-English Rate (Non-EN Subscribers)** | 6.85% | 0.00% | +6.85% | **Critical** |
| **Translation Engine Latency (p99)** | 1,420 ms | ≤ 500 ms | +184.00% | **Critical** |

---

### Visualization Trigger

A grouped bar chart is recommended to compare audited vs. targeted routing accuracy across all supported language tiers.

```json
{
  "chart_type": "bar",
  "title": "Emergency SMS Broadcast Language Alignment Audit by Language Code",
  "data": {
    "categories": ["English", "Spanish", "Vietnamese", "Chinese (Mandarin)", "Tagalog", "Korean", "Russian"],
    "series": [
      {
        "name": "Target Match Rate (%)",
        "data": [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
      },
      {
        "name": "Audited Match Rate (%)",
        "data": [99.98, 98.42, 94.15, 91.80, 89.50, 92.30, 88.75]
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **Update Gateway Translation Buffers:** Increase upstream GSM/UCS-2 payload character limits and split-concatenation handlers to prevent automatic fallback to default English when translated strings exceed standard SMS single-part lengths.
- **Pre-Compile Emergency Life-Safety Templates:** Store pre-validated, certified multi-lingual templates (PSPS, high-wind outages, storm ETR alerts) locally on edge broadcast nodes to eliminate real-time translation latency spikes during grid emergencies.
- **Implement Automated Sync & Reconciliation:** Establish a daily automated reconciliation pipeline between the Customer Relationship Management (CRM) language profile repository and the Emergency Notification Gateway subscriber cache.
- **Validate Special Character Encoding:** Audit SMS telecommunication aggregator connections for multi-byte Unicode (UTF-16/UCS-2) delivery support across Mandarin, Russian, and Tagalog diacritics.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Broadcast the multilingual safety alert across localized distribution channels for all affected community zones."

**Agent Response:**
### Executive Summary
**The Multi Language Translation Router has staged and validated emergency multilingual safety alert payloads across four high-priority community grid zones, spanning five primary spoken languages (English, Spanish, Mandarin, Vietnamese, and Tagalog). Channel routing paths—encompassing SMS, automated Interactive Voice Response (IVR), push notifications, and localized social broadcast relays—have achieved a 99.8% translation parity verification score. Final dispatch authorization is queued pending Human-In-The-Loop (HITL) confirmation to ensure synchronized dissemination across downstream telecommunication gateways.**

---

### Quantitative Performance & Routing Status

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Reachable Customer Accounts** | 211,900 | 215,000 | -1.44% | Normal |
| **Translation Engine Semantic Parity** | 99.82% | 99.00% | +0.83% | Normal |
| **Channel Routing Latency (Queue-to-Gateway)** | 1.15 s | < 2.00 s | -42.50% | Normal |
| **Non-Primary Language Routing Coverage** | 44.78% | 40.00% | +11.95% | Normal |
| **Gateway Carrier Fallback Redundancy** | 100.0% | 100.0% | 0.00% | Normal |
| **Message Ingestion & Queue Saturation** | 82.40% | < 75.00% | +9.87% | Warning |

---

### Visualization Trigger: Multilingual Distribution by Zone

```json
{
  "chart_type": "bar",
  "title": "Multilingual Safety Alert Routing Volume by Community Zone & Language",
  "categories": [
    "Zone-1 (Metro Central)",
    "Zone-2 (North Basin)",
    "Zone-3 (East Corridor)",
    "Zone-4 (South Valley)"
  ],
  "series": [
    {"name": "English (EN)", "data": [45200, 18400, 22100, 31500]},
    {"name": "Spanish (ES)", "data": [28400, 14200, 19800, 26900]},
    {"name": "Vietnamese (VI)", "data": [8900, 3100, 6400, 4200]},
    {"name": "Mandarin (ZH)", "data": [11300, 4800, 7200, 5600]},
    {"name": "Tagalog (TL)", "data": [5100, 1900, 3800, 3100]}
  ]
}
```

---

### Actionable Recommendations

- **Execute Channel Staggering**: Sequence SMS carrier batches in 500ms intervals across Zone-1 and Zone-4 to prevent telecommunication provider throttling and mitigate queue saturation.
- **Activate Local Media & Community Partner Relays**: Transmit standardized JSON emergency payloads to verified municipal public information officer (PIO) channels and localized non-English broadcast partners.
- **Engage Bi-directional Inbound Telemetry**: Monitor inbound customer support line spikes and dynamic language-swapping IVR requests in real time post-broadcast to adjust downstream translation throughput.
- **Audit Verification Callbacks**: Collect delivery receipts (DLRs) every 60 seconds to ensure high-density outage zones maintain >98% message receipt confirmation within 5 minutes of release.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "EMERGENCY_MULTILINGUAL_BROADCAST_DISPATCH",
  "priority": "HIGH",
  "target_zones": ["Zone-1", "Zone-2", "Zone-3", "Zone-4"],
  "target_languages": ["EN", "ES", "ZH", "VI", "TL"],
  "total_recipients": 211900,
  "channels": ["SMS_GATEWAY", "IVR_OUTBOUND", "PUSH_NOTIFICATION", "MUNICIPAL_PIO_FEED"],
  "alert_payload_id": "ALT-SEC-2024-9981",
  "approval_required_by": "Utility Operations Director / Customer Communications Lead",
  "execution_timeout": "300s"
}
```
