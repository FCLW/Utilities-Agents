import json
from typing import Any, Dict, List, Union

class VisualizerTool:
    """A tool for generating backend chart configurations or visualizations."""
    def __init__(self):
        self.name = "VisualizerTool"
        self.__name__ = self.name

    def __call__(self, data_json: Union[str, List[Dict[str, Any]], Dict[str, Any]], chart_type: str = "line") -> str:
        """Generates structured visualization specifications for charts.
        
        Args:
            data_json: JSON string or serializable structure containing the data points to visualize.
            chart_type: Type of chart (e.g. line, bar, scatter, pie, area).
        """
        try:
            if isinstance(data_json, str):
                parsed = json.loads(data_json)
            else:
                parsed = data_json
        except Exception as e:
            return f"Error: Invalid JSON format for visualization data: {e}"

        if isinstance(parsed, dict):
            values = parsed.get("data") or parsed.get("values") or [parsed]
        elif isinstance(parsed, list):
            values = parsed
        else:
            values = [{"value": parsed}]

        c_type = chart_type.lower()
        mark_map = {
            "line": "line",
            "bar": "bar",
            "scatter": "point",
            "pie": "arc",
            "area": "area"
        }
        mark = mark_map.get(c_type, "bar")

        x_field = "timestamp"
        y_field = "value"
        if values and isinstance(values[0], dict):
            keys = list(values[0].keys())
            if len(keys) >= 2:
                x_field, y_field = keys[0], keys[1]
            elif len(keys) == 1:
                y_field = keys[0]

        spec = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": f"Utilities Dynamic {chart_type.title()} Chart",
            "data": {"values": values},
            "mark": mark,
            "encoding": {
                "x": {"field": x_field, "type": "nominal"},
                "y": {"field": y_field, "type": "quantitative"}
            }
        }

        return f"[RENDER: {chart_type.upper()}] chart generated. Specification: {json.dumps(spec)}"
