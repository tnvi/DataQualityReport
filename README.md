# DataQuality



DataQuality is a portfolio data engineering project that builds a configurable data quality validation platform for e-commerce datasets.

## Project Goal



The goal of this project is to ingest raw e-commerce data, profile datasets, apply configurable validation rules, generate quality results, and later expose quality scorecards through APIs and deployment-ready services.



## Dataset



This project uses the Olist Brazilian E-commerce dataset from Kaggle.



In Week 1, the dataset will be used locally as CSV files.



Raw files should be placed under:



```text

data/raw/csv/

```



Raw data should not be committed to Git.



## Week 1 Scope



Week 1 focuses on building a local Python-based data quality engine.



Planned Week 1 capabilities:



* CSV ingestion

* YAML-based validation rules

* Local profiling using Pandas

* Schema validation

* Null validation

* Duplicate validation

* Range validation

* Accepted values validation

* Basic relationship validation

* Validation result output

* Basic pytest tests

* Simple CLI command



## Week 1 Folder Structure



```text

dataguard/
    README.md
    requirements.txt
    .gitignore

    data/
        raw/
            csv/

        processed/
            profile_metrics/
            validation_results/

    configs/
        datasets/

    src/
        dataguard/
            __init__.py
    
    tests/

```



## Setup

Create virtual environment:



```bash

python -m venv .venv

```



Activate on Windows:



```bash

.venv\Scripts\activate

```



Install dependencies:



```bash

pip install -r requirements.txt

```



## Current Status



Day 1: Repository and environment setup.

## Dataset Source

This project uses the Olist Brazilian E-commerce Public Dataset from Kaggle.

The dataset is used as a realistic e-commerce source system for building a data quality validation platform.

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data

## Local Data Placement

Download the dataset manually from Kaggle and place the selected CSV files under:

```text
data/raw/csv/
```

Raw data is intentionally not committed to Git.

## V1 Dataset Scope

For V1, this project uses the following Olist files:

| File | Dataset Name | Purpose |
|---|---|---|
| `olist_orders_dataset.csv` | orders | Main order lifecycle table |
| `olist_order_items_dataset.csv` | order_items | Order line items; connects orders, products, and sellers |
| `olist_order_payments_dataset.csv` | payments | Payment details for orders |
| `olist_customers_dataset.csv` | customers | Customer information |
| `olist_products_dataset.csv` | products | Product information |
| `olist_sellers_dataset.csv` | sellers | Seller information |

## Tables Not Deeply Used in V1

The following files may exist in the Kaggle dataset but are not deeply used in V1:

| File | Reason |
|---|---|
| `olist_geolocation_dataset.csv` | Useful later, but can distract from core order-quality checks |
| `olist_order_reviews_dataset.csv` | Useful later for review-quality or customer-experience analysis |
| `product_category_name_translation.csv` | Useful later for product category enrichment |

## Initial Table Relationships

```text
customers.customer_id
  → orders.customer_id

orders.order_id
  → order_items.order_id
  → payments.order_id

products.product_id
  → order_items.product_id

sellers.seller_id
  → order_items.seller_id
```

## Initial Data Quality Ideas

Based on the selected V1 tables, the first rule categories will be:

- Schema checks
- Required column checks
- Primary key uniqueness checks
- Composite key uniqueness checks
- Accepted value checks
- Numeric range checks
- Basic relationship checks

## Validation Rule Configuration

Validation rules are stored as YAML files under:

```text
configs/datasets/
```

Each dataset has its own rule file:

| Dataset | Rule File |
|---|---|
| orders | `configs/datasets/orders.yml` |
| order_items | `configs/datasets/order_items.yml` |
| payments | `configs/datasets/payments.yml` |
| customers | `configs/datasets/customers.yml` |
| products | `configs/datasets/products.yml` |
| sellers | `configs/datasets/sellers.yml` |

The rules are intentionally stored outside Python code.

This allows the same validation engine to load dataset-specific expectations from configuration instead of hardcoding checks separately for every dataset.

Current rule categories defined in YAML:

- Required column checks
- Primary key uniqueness checks
- Composite key uniqueness checks
- Accepted value checks
- Numeric minimum/range checks
- Timestamp expectations
- Basic relationship checks

## Current Engine Components

The first reusable engine components have been added.

### CSV Reader

File:

```text
src/dataguard/ingestion/csv_reader.py
```

Purpose:

* Reads CSV files into Pandas DataFrames
* Checks that the file exists
* Checks that the file has a `.csv` extension

### Rule Loader

File:

```text
src/dataquality/validation/rule_loader.py
```

Purpose:

* Loads dataset-specific YAML rules from `configs/datasets/`
* Uses the dataset name to find the matching YAML file
* Validates that the YAML file is not empty
* Validates that the dataset name inside the YAML matches the requested dataset

### Running Tests

Set `PYTHONPATH` so Python can find the `src/dataquality` package:

```powershell
$env:PYTHONPATH = "src"
```

Run Day 4 tests:

```powershell
python -m pytest tests\test_csv_reader.py tests\test_rule_loader.py -v
```

## Supported Validators 

The first validator modules have been added under: 
```text 
src/dataquality/validation/ 
``` 
Current validators:
 | Validator | File | Purpose |
  |---|---|---| 
  | Schema validator | `schema_validator.py` | Checks missing and unexpected columns | 
  | Required validator | `required_validator.py` | Checks required columns for null values | 
  | Duplicate validator | `duplicate_validator.py` | Checks primary key and composite key uniqueness | 
  | Range validator | `range_validator.py` | Checks configured min/max numeric rules |
  | Accepted values validator | `accepted_values_validator.py` | Checks categorical values against allowed lists | 
  | Relationship validator | `relationship_validator.py` | Checks referential integrity across datasets | 
  
  All validators return standardized result dictionaries using: 
  ```text 
  src/dataquality/validation/result.py 
  ``` 
  
  The result writer will be added next.
  
  ## Profiling and Output Writing 
  The local profiler and result writer have been added. 
  
  ### Pandas Profiler 
  
  File: 
  ```text
   src/dataquality/profiling/pandas_profiler.py 
  ``` 
  
  The profiler generates dataset-level and column-level metrics. 
  Current metrics: 
  - row count 
  - column count 
  - duplicate key count 
  - null count per column 
  - null percentage per column 
  - distinct count per column 
  - data type per column 
  - min/max values where safe 
  
  ### Result Writer 
  File: 
  ```text 
  src/dataquality/storage/result_writer.py 
  ``` 
  
  The writer persists records to CSV. 
  Output locations:
   ```text 
   data/processed/profile_metrics/ 
   data/processed/validation_results/ 
   ``` 
   Example output files: 
   ```text 
   data/processed/profile_metrics/orders_profile_metrics.csv 
   data/processed/validation_results/orders_validation_results.csv 
   ``` 
   These generated outputs are not committed to Git. 
   
   ### Running Tests
   ```powershell 
   $env:PYTHONPATH = "src" 
   python -m pytest tests -v 
   ```

   