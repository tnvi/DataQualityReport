from pathlib import Path

import pandas as pd


RAW_CSV_DIR = Path("data/raw/olist")
SUMMARY_OUTPUT_PATH = Path("data/processed/profile_metrics/day2_raw_file_summary.csv")

V1_FILES = [
    "olist_orders_dataset_plus_1000.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
]


def inspect_csv_file(file_path: Path) -> dict:
    """
    Inspect a raw CSV file and return basic discovery metadata.

    This is a Day 2 discovery utility, not the final profiler.
    The production-style profiler will be built later under src/dataguard/profiling.
    """
    df = pd.read_csv(file_path)

    return {
        "file_name": file_path.name,
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": ", ".join(df.columns),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def main() -> None:
    RAW_CSV_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    summary_records = []

    print("Inspecting selected Olist V1 CSV files")
    print("=" * 80)

    for file_name in V1_FILES:
        file_path = RAW_CSV_DIR / file_name

        if not file_path.exists():
            print(f"Missing file: {file_path}")
            continue

        metadata = inspect_csv_file(file_path)
        summary_records.append(metadata)

        print(f"File: {metadata['file_name']}")
        print(f"Rows: {metadata['row_count']}")
        print(f"Columns: {metadata['column_count']}")
        print(f"Missing cells: {metadata['missing_cells']}")
        print(f"Duplicate rows: {metadata['duplicate_rows']}")
        print(f"Column names: {metadata['columns']}")
        print("-" * 80)

    if not summary_records:
        raise FileNotFoundError(
            f"No selected V1 CSV files were found under {RAW_CSV_DIR}. "
            "Download the Olist dataset and place selected CSV files there."
        )

    summary_df = pd.DataFrame(summary_records)
    summary_df.to_csv(SUMMARY_OUTPUT_PATH, index=False)

    print(f"Summary written to: {SUMMARY_OUTPUT_PATH}")


if __name__ == "__main__":
    main()