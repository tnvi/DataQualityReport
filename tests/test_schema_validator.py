from dataquality.validation.schema_validator import validate_schema

import pandas as pd

def test_validate_schema_when_col_match():
    #arranging data
    df = pd.DataFrame(
        {
            "order_id": ['1', '2', '3', '4'],
            "customer_id": ['551321', '87346', '65423132', '643215']
        }
    )

    rules = {
        'dataset': "orders",
        'columns': {
            "order_id": {
                'required': True,
                'unique': True
            },
            "customer_id": {
                'required': True
            }
        }
    }
    #act
    result = validate_schema(df, rules)

    #assert
    assert len(result) == 2
    
    assert result[0]['status'] == "PASSED"
    assert result[0]['rule_name'] == 'schema_expected_cols_present'
    assert result[0]['severity'] == "CRITICAL"

    assert result[1]['status'] == "PASSED"
    assert result[1]['rule_name'] == 'schema_unexpected_cols_present'
    assert result[1]['severity'] == "LOW"


def test_validate_schema_when_cols_missing():
    #arrange data
    df = pd.DataFrame(
        {
            "order_id": ['1', '2', '3', '4']
        }
    )

    rules = {
        'dataset': "orders",
        'columns': {
            "order_id": {            },
            "customer_id": {            }
        }
    }
    #act
    result = validate_schema(df, rules)

    #assert
    assert len(result) == 2
    assert result[0]['status'] == "FAILED"
    assert result[0]['rule_name'] == 'schema_expected_cols_present'
    assert result[0]['severity'] == "CRITICAL"

    assert result[1]['status'] == "PASSED"
    assert result[1]['rule_name'] == 'schema_unexpected_cols_present'
    assert result[1]['severity'] == "LOW"

def test_validate_schema_when_unexpected_cols_df():
 #arranging data
    df = pd.DataFrame(
        {
            "order_id": ['1', '2', '3', '4'],
            "customer_id": ['551321', '87346', '65423132', '643215']
        }
    )

    rules = {
        'dataset': "orders",
        'columns': {
            "order_id": {
                'required': True,
                'unique': True
            }
        }
    }
    #act
    result = validate_schema(df, rules)

    #assert
    assert len(result) == 2
    assert result[0]['status'] == "PASSED"
    assert result[0]['rule_name'] == 'schema_expected_cols_present'
    assert result[0]['severity'] == "CRITICAL"

    assert result[1]['status'] == "WARNING"
    assert result[1]['rule_name'] == 'schema_unexpected_cols_present'
    assert result[1]['severity'] == "LOW"

def test_validate_schema_when_col_rename():
#arranging data
    df = pd.DataFrame(
        {
            "order_id": ['1', '2', '3', '4'],
            "customer_gfcid": ['551321', '87346', '65423132', '643215']
        }
    )

    rules = {
        'dataset': "orders",
        'columns': {
            "order_id": {
                'required': True,
                'unique': True
            }, 
            "customer_id": {            }
        }
    }
    #act
    result = validate_schema(df, rules)

    #assert
    assert len(result) == 2
    assert result[0]['status'] == "FAILED"
    assert result[0]['rule_name'] == 'schema_expected_cols_present'
    assert result[0]['severity'] == "CRITICAL"

    assert result[1]['status'] == "WARNING"
    assert result[1]['rule_name'] == 'schema_unexpected_cols_present'
    assert result[1]['severity'] == "LOW"
