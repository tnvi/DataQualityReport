from dataquality.cli import (
    build_parser, 
    validate_dataset, 
    run_validators, 
    load_referential_dataframe, 
    summarize_validation_results, 
    resolve_input_path,
    print_validation_summary,
    main
)

import pandas as pd 
import pytest

def test_build_parser_parses_command():
    parser = build_parser()

    assert parser is not None
    args = parser.parse_args([
        'validate', '--dataset', 'orders'
    ])
    assert args is not None
    assert args.command == 'validate'
    assert args.dataset == 'orders'

def test_validate_dataset_generates_output(tmp_path):
      
    dataset = 'orders' 
    input_path = None
    raw_data_dir = tmp_path/'raw_data_path'
    rules_dir= tmp_path/'rules_path'
    profile_output_dir= tmp_path/'profile_output_path'
    validation_output_dir = tmp_path/'validation_output_path'

    raw_data_dir.mkdir()
    rules_dir.mkdir()
    
    orders_csv = raw_data_dir/'orders.csv'
    orders_csv.write_text(
        (
            "order_id,customer_id,order_status\n"
            "123,234,delivered\n"
            "4356,234,shipped"
        ),
        encoding= "utf-8"
    )

    cust_csv = raw_data_dir/'customers.csv'
    cust_csv.write_text((
        "cust_id,cust_name \n"
        "234,sdffq \n"
        "5786,asdjj"
    ), encoding= "utf-8"
    )

    orders_rules = rules_dir/'orders.yml'
    orders_rules.write_text(
        """
dataset: orders
source_file: orders.csv
primary_key: order_id
columns:
    order_id:
        required: true
        unique: true
        severity: CRITICAL
    customer_id:
        required: true
        severity: HIGH
    order_status:
        required: true
        accepted_values:
            - delivered
            - shipped
            - available
        severity: HIGH
relationships:
    - column: customer_id
      references:
        dataset: customers
        column: cust_id
      severity: HIGH
""".strip(),encoding= 'utf-8'
    )

    customer_rules = rules_dir/'customers.yml'
    customer_rules.write_text(
        """
dataset: customers
source_file: customers.csv
primary_key: cust_id
columns:
    cust_id:
        required: true
        unique: true
        severity: CRITICAL
    cust_name:
        required: true
        severity: HIGH
""".strip(),encoding= 'utf-8'
    )

    result = validate_dataset(dataset, input_path, raw_data_dir, rules_dir, profile_output_dir, validation_output_dir)

    profile_df = pd.read_csv(result['profile_output_path'])
    validation_df = pd.read_csv(result['validation_output_path'])
    print(validation_df.to_string())
    
    assert result["dataset"] == dataset
    assert result["row_count"] == 2
    print(result["validation_summary"])
    assert result["validation_summary"]["failed"] == 0
    assert result["profile_output_path"].exists()
    assert result["validation_output_path"].exists()
    
    

    assert not profile_df.empty
    assert not validation_df.empty

def test_main_returns_2_when_valiadtion_fails(tmp_path):
    dataset = 'orders' 
    input_path = None
    raw_data_dir = tmp_path/'raw_data_path'
    rules_dir= tmp_path/'rules_path'
    profile_output_dir= tmp_path/'profile_output_path'
    validation_output_dir = tmp_path/'validation_output_path'

    raw_data_dir.mkdir()
    rules_dir.mkdir()
    
    orders_csv = raw_data_dir/'orders.csv'
    orders_csv.write_text(
        (
            "order_id,order_status\n"
            "123,delivered\n"
            "4356,ship"
        ),
        encoding= "utf-8"
    )

    cust_csv = raw_data_dir/'customers.csv'
    cust_csv.write_text((
        "cust_id,cust_name \n"
        "234,sdffq \n"
        "5786,asdjj"
    ), encoding= "utf-8"
    )

    orders_rules = rules_dir/'orders.yml'
    orders_rules.write_text(
        """
dataset: orders
source_file: orders.csv
primary_key: order_id
columns:
    order_id:
        required: true
        unique: true
        severity: CRITICAL
    order_status:
        required: true
        accepted_values:
            - delivered
            - shipped
            - available
        severity: HIGH
""".strip(),encoding= 'utf-8'
    )

    result = main([
            'validate', 
            '--dataset',
            'orders',
            '--raw_data_dir',
            str(raw_data_dir),
            '--rules_data_dir',
            str(rules_dir),
            '--profile_output_dir',
            str(profile_output_dir),
            '--validation_output_dir',
            str(validation_output_dir)
            ])
    
    assert result == 2
    assert (validation_output_dir/'orders_validation_results.csv').exists()
    assert (profile_output_dir/'orders_profile_metrics.csv').exists()

def test_main_returns_1_when_unsupported_command():
    with pytest.raises(SystemExit) as truth:
        main(['parse'])

    assert truth.value.code == 2


def test_main_returns_1_when_file_not_found(tmp_path):
    dataset = 'orders' 
    input_path = None
    raw_data_dir = tmp_path/'raw_data_path'
    rules_dir= tmp_path/'rules_path'
    profile_output_dir= tmp_path/'profile_output_path'
    validation_output_dir = tmp_path/'validation_output_path'

    raw_data_dir.mkdir()
    rules_dir.mkdir()
    
    orders_csv = raw_data_dir/'order.csv'
    orders_csv.write_text(
        (
            "order_id,order_status\n"
            "123,delivered\n"
            "4356,ship"
        ),
        encoding= "utf-8"
    )

    cust_csv = raw_data_dir/'customers.csv'
    cust_csv.write_text((
        "cust_id,cust_name \n"
        "234,sdffq \n"
        "5786,asdjj"
    ), encoding= "utf-8"
    )

    orders_rules = rules_dir/'orders.yml'
    orders_rules.write_text(
        """
dataset: orders
source_file: orders.csv
primary_key: order_id
columns:
    order_id:
        required: true
        unique: true
        severity: CRITICAL
    order_status:
        required: true
        accepted_values:
            - delivered
            - shipped
            - available
        severity: HIGH
""".strip(),encoding= 'utf-8'
    )

    result = main([
            'validate', 
            '--dataset',
            'orders',
            '--raw_data_dir',
            str(raw_data_dir),
            '--rules_data_dir',
            str(rules_dir),
            '--profile_output_dir',
            str(profile_output_dir),
            '--validation_output_dir',
            str(validation_output_dir)
            ])
    
    assert result == 1
