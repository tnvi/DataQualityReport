from typing import Any
from pathlib import Path
import pandas as pd

def write_to_csv(records: list[dict[str,Any]], output_path: str | Path) -> Path:
    path = Path(output_path)

    path.parent.mkdir(parents= True, exist_ok= True)

    records_df = pd.DataFrame(records)

    records_df.to_csv(path, index= False)

    return path


def write_profile_metrics(records: list[dict[str,Any]], dataset: str, output_path: str | Path = "data/processed/profile_metrics") -> Path:
    output_path = Path(output_path) / f"{dataset}_profile_metrics.csv"

    return write_to_csv(records, output_path)

def write_validation_results(results: list[dict], dataset: str, output_path: str | Path ="data/processed/validation_results" ) -> Path:
    output_path = Path(output_path) / f"{dataset}_validation_results.csv"

    return write_to_csv(results, output_path)

