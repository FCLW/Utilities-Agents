import os
from pathlib import Path

def load_prompt_layer(layer_name: str) -> str:
    instructions_dir = Path(os.path.dirname(__file__)).parent / "instructions"
    file_path = instructions_dir / f"{layer_name}.md"
    
    if not file_path.exists():
        return f"[{layer_name}.md not found]"
        
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
