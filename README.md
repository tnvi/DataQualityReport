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

.venv\\Scripts\\activate

```



Install dependencies:



```bash

pip install -r requirements.txt

```



## Current Status



Day 1: Repository and environment setup.

