import pandas as pd

from dataquality.validation.required_validator import validate_required

#success test
def test_validate_required_when_required_col_has_no_nulls():
    #arranging data
    df = pd.DataFrame({
        'order_id': ['1', '2'],
        'cust_id': ['10', '11']
    })

    rules ={
        'dataset': 'orders',
        'columns': {
            'order_id': {
                'required': True 
            },
            'cust_id': {
                'required': False
            }
        }}
    
    #act
    result = validate_required(df, rules)

    #assert
    assert len(result) == 1
    print(result)
    assert result[0]['column'] == 'order_id'
    assert result[0]['status'] == 'PASSED'
    assert result[0]['severity'] == 'HIGH'
    assert result[0]['rule_name'] == 'order_id_required'

#required col has null    
def test_validate_required_when_required_col_has_nulls():
    #arranging data
    df = pd.DataFrame({
        'order_id': ['1', None],
        'cust_id': ['10', '11']
    })

    rules ={
        'dataset': 'orders',
        'columns': {
            'order_id': {
                'required': True 
            },
            'cust_id': {
                'required': False
            }
        }}
    
    #act
    result = validate_required(df, rules)

    #assert
    assert len(result) == 1
    print(result)
    assert result[0]['column'] == 'order_id'
    assert result[0]['status'] == 'FAILED'
    assert result[0]['severity'] == 'HIGH'
    assert result[0]['rule_name'] == 'order_id_required'

#required col severity    
def test_validate_required_when_required_col_severity_defined():
    #arranging data
    df = pd.DataFrame({
        'order_id': ['1', ' '],
        'cust_id': ['10', '11']
    })

    rules ={
        'dataset': 'orders',
        'columns': {
            'order_id': {
                'required': True, 
                'severity': 'LOW'
            },
            'cust_id': {
                'required': False
            }
        }}
    
    #act
    result = validate_required(df, rules)

    #assert
    assert len(result) == 1
    print(result)
    assert result[0]['column'] == 'order_id'
    assert result[0]['status'] == 'PASSED'
    assert result[0]['severity'] == 'LOW'
    assert result[0]['rule_name'] == 'order_id_required'

#required col missing in df
def test_validate_required_when_required_col_missing_in_input():
    #arranging data
    df = pd.DataFrame({
        'cust_id': ['10', '11']
    })

    rules ={
        'dataset': 'orders',
        'columns': {
            'order_id': {
                'required': True, 
                'severity': 'CRITICAL'
            },
            'cust_id': {
                'required': False
            }
        }}
    
    #act
    result = validate_required(df, rules)

    #assert
    assert len(result) == 1
    print(result)
    assert result[0]['column'] == 'order_id'
    assert result[0]['status'] == 'SKIPPED'
    assert result[0]['severity'] == 'CRITICAL'
    assert result[0]['rule_name'] == 'order_id_required'
