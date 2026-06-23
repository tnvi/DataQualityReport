from pathlib import Path
from typing import Any

import yaml

DEFAULT_RULES_DIR = Path("configs/datasets")

def load_rules(dataset_name: str, rules_dir: str | Path = DEFAULT_RULES_DIR) -> dict[str, Any]:
    """
    read yml file and return in the form of dictionary and handle possible error situation     
    """
    rules_path = Path(rules_dir)/ f"{dataset_name}.yml"

    if not rules_path.exists():
        raise FileNotFoundError(f"Rule config not found: {rules_path}")
    
    #read the yml file into a dictionary
    with rules_path.open("r", encoding="utf-8") as file:
        rules = yaml.safe_load(file)

    if not rules:
        raise ValueError(f"Rule config is empty: {rules_path}")
    
    configured_dataset = rules.get("dataset")

    if configured_dataset != dataset_name:
        raise ValueError(
            f"Dataset mismatch in {rules_path}"
            f"Expected '{dataset_name}', found '{configured_dataset}'."
        )
    
    return rules