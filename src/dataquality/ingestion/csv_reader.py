import pandas as pd
from pathlib import Path

def read_csv(file_path: str | Path) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Csv file not found at: {file_path}")
    
    if path.suffix.lower() !=".csv":
        raise ValueError(f"Expected a .csv file, {path}")

    return pd.read_csv(path)

def read_olist_csv(file_name: str, raw_dir: Path) -> pd.DataFrame:
    file_path = raw_dir / file_name
    return read_csv(file_path)