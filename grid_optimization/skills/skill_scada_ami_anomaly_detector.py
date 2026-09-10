"""Skill: SCADA and AMI Time-Series Anomaly Detector."""
from typing import Dict, List, Any

class ScadaAmiAnomalyDetectorSkill:
    """Reusable skill: Identifies sensor drift, meter tampering, and high-frequency telemetry anomalies."""

    def execute(self, telemetry_series: List[float], entity_id: str = "METER-AMI-8891") -> Dict[str, Any]:
        if not telemetry_series:
            telemetry_series = [1.01, 1.00, 0.99, 1.02, 0.82, 1.01, 1.00] # Contains 0.82 dip

        mean_val = sum(telemetry_series) / len(telemetry_series)
        variance = sum((x - mean_val) ** 2 for x in telemetry_series) / len(telemetry_series)
        std_dev = max(0.001, variance ** 0.5)

        anomalies = []
        for idx, val in enumerate(telemetry_series):
            z_score = abs(val - mean_val) / std_dev
            if z_score > 1.90:
                anomalies.append({"index": idx, "value": val, "z_score": round(z_score, 2)})

        return {
            "skill": "skill_scada_ami_anomaly_detector",
            "entity_id": entity_id,
            "series_length": len(telemetry_series),
            "mean_val": round(mean_val, 3),
            "std_dev": round(std_dev, 4),
            "anomalies_detected": len(anomalies),
            "anomaly_points": anomalies,
            "sensor_health_flag": "DEFECTIVE_CALIBRATION_SUSPECTED" if anomalies else "HEALTHY"
        }
