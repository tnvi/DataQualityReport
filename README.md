# DataQuality

Dataquality is a configurable data-quality validation platform built around the Olist Brazilian E-commerce dataset.

The project begins as a local Python validation engine and will expand into a broader data engineering pipeline using Avro, Spark, Databricks, Parquet, Airflow, dbt, FastAPI, Docker, Kubernetes, Azure storage, and GitHub Actions.

## Current Capabilities

The completed Week 1 engine can:

- Read local CSV datasets using Pandas
- Load dataset-specific validation rules from YAML
- Generate dataset and column profile metrics
- Validate schema
- Validate required/non-null fields
- Validate primary-key and composite-key uniqueness
- Validate numeric minimum and maximum rules
- Validate categorical accepted values
- Validate cross-table relationships
- Write profile metrics to CSV
- Write validation results to CSV
- Run through a command-line interface
- Run automated tests using pytest

## Local Pipeline

text
Olist CSV file
  ↓
CSV reader
  ↓
Pandas DataFrame
  ↓
Pandas profiler
  ↓
YAML rule loader
  ↓
Validation engine
  ├── Schema checks
  ├── Null checks
  ├── Duplicate checks
  ├── Range checks
  ├── Accepted-value checks
  └── Relationship checks
  ↓
Profile metrics CSV
Validation results CSV


## Dataset

Dataquality uses the Olist Brazilian E-commerce dataset from Kaggle.

Raw CSV files must be downloaded separately and placed under:

text
data/raw/olist/


Raw and processed data are intentionally excluded from Git.

### V1 Datasets

| Dataset | Source file | Purpose |
|---|---|---|
| orders | olist_orders_dataset_plus_1000.csv | Main order lifecycle |
| order_items | olist_order_items_dataset.csv | Items within orders |
| payments | olist_order_payments_dataset.csv | Payment records |
| customers | olist_customers_dataset.csv | Customer reference data |
| products | olist_products_dataset.csv | Product reference data |
| sellers | olist_sellers_dataset.csv | Seller reference data |

Geolocation, reviews, and product-category translation are not deeply used in V1.

## Main Relationships

text
customers.customer_id
  ← orders.customer_id

orders.order_id
  ← order_items.order_id
  ← payments.order_id

products.product_id
  ← order_items.product_id

sellers.seller_id
  ← order_items.seller_id


## Project Structure

text
Dataquality/
  README.md
  requirements.txt
  .gitignore

  data/
    raw/
      olist/
    processed/
      profile_metrics/
      validation_results/

  configs/
    datasets/
      orders.yml
      order_items.yml
      payments.yml
      customers.yml
      products.yml
      sellers.yml

  src/
    Dataquality/
      cli.py

      ingestion/
        csv_reader.py

      profiling/
        pandas_profiler.py

      validation/
        result.py
        rule_loader.py
        schema_validator.py
        required_validator.py
        duplicate_validator.py
        range_validator.py
        accepted_values_validator.py
        relationship_validator.py

      storage/
        result_writer.py

  tests/
  tools/


## Setup

### 1. Clone the repository

powershell
git clone https://github.com/<username>/Dataquality.git
cd Dataquality


### 2. Create a virtual environment

powershell
python -m venv .venv


### 3. Activate it on Windows

powershell
.venv\Scripts\activate


### 4. Install dependencies

powershell
pip install -r requirements.txt


### 5. Set the Python source path

powershell
$env:PYTHONPATH = "src"


### 6. Add the Olist files

Place the selected CSV files under:

text
data/raw/olist/


Do not commit these files.

## Usage

### Show CLI help

powershell
python -m Dataquality.cli --help


### Show validation command help

powershell
python -m Dataquality.cli validate --help


### Validate a configured dataset

powershell
python -m Dataquality.cli validate --dataset orders


When --input is omitted, Dataquality uses the source_file value from:

text
configs/datasets/orders.yml


### Validate an explicit input file

powershell
python -m Dataquality.cli validate `
  --dataset orders `
  --input data\raw\olist\olist_orders_dataset_plus_1000.csv


### Validate other V1 datasets

powershell
python -m Dataquality.cli validate --dataset customers
python -m Dataquality.cli validate --dataset order_items
python -m Dataquality.cli validate --dataset payments
python -m Dataquality.cli validate --dataset products
python -m Dataquality.cli validate --dataset sellers


## Output

Profile metrics are written to:

text
data/processed/profile_metrics/<dataset>_profile_metrics.csv


Validation results are written to:

text
data/processed/validation_results/<dataset>_validation_results.csv


Example:

text
data/processed/profile_metrics/orders_profile_metrics.csv
data/processed/validation_results/orders_validation_results.csv


Generated outputs are intentionally excluded from Git.

## Profile Metrics

Current profile metrics include:

- Row count
- Column count
- Duplicate key count
- Null count per column
- Null percentage per column
- Distinct count per column
- Pandas data type
- Minimum value where supported
- Maximum value where supported

## Supported Validation Rules

| Rule type | Description |
|---|---|
| Schema | Detects missing and unexpected columns |
| Required/null | Checks required columns for null values |
| Duplicate | Checks primary and composite key uniqueness |
| Range | Checks configured numeric min and max values |
| Accepted values | Checks categorical values against configured lists |
| Relationship | Checks referential integrity across datasets |

Rules are stored in YAML under:

text
configs/datasets/


The Python validators are generic and do not hardcode dataset-specific checks.

## Validation Statuses

| Status | Meaning |
|---|---|
| PASSED | The rule was evaluated successfully and passed |
| FAILED | The rule was evaluated and found invalid data |
| WARNING | A non-blocking issue was detected |
| SKIPPED | The rule could not run because a prerequisite was unavailable |

## CLI Exit Codes

| Exit code | Meaning |
|---|---|
| 0 | Execution completed with no failed validation rules |
| 1 | Execution failed because of a file, config, or parsing error |
| 2 | Execution completed, but one or more validation rules failed |

## Run Tests

Run the complete test suite:

powershell
$env:PYTHONPATH = "src"
python -m pytest tests -v


The tests use small temporary files and DataFrames, so they do not depend on the local Kaggle dataset.

## Design Decisions

### Configuration-driven validation

Dataset-specific rules live in YAML instead of Python code. This allows the same engine to validate multiple datasets.

### Separation of responsibilities

- Ingestion reads data
- Profiling describes data
- Validation evaluates rules
- Storage writes outputs
- CLI orchestrates the workflow

### Raw-data preservation

Raw CSV files are kept unchanged and excluded from Git.

### Local-first implementation

Week 1 uses Pandas to prove validation behavior locally before adding distributed processing and orchestration.

## Current Limitations

- The local engine loads full CSV files into memory
- Data types are currently inferred by Pandas
- Advanced timestamp comparisons are not yet implemented
- Conditional-null rules are defined but not yet executed
- Results do not yet include batch IDs or run timestamps
- CSV is used for local output
- The project is not yet orchestrated
- The API and dashboard are not yet implemented

## Roadmap

### Week 2

- Avro conversion and ingestion
- Local PySpark profiling
- Databricks notebooks
- Bronze Parquet
- Silver Parquet
- Airflow DAG
- Docker Compose for Airflow

### Week 3

- dbt quality models and marts
- Quality-score calculation
- FastAPI JSON endpoints
- Optional dashboard
- Docker images
- GitHub Actions CI/CD

### Week 4

- Kubernetes deployment
- Azure Blob/ADLS integration
- Databricks execution evidence
- Architecture documentation
- Cost-control documentation
- Final demo and resume positioning