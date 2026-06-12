from dataquality.validation.accepted_values_validator import validate_acceptable_values

import pandas as pd

# success test 
def test_validate_acceptable_values_when_all_values_are_defined():
        #arranging data
    df = pd.DataFrame({
        'order_id': ['1', '2', '3', '4'],
        'customer_id': ['2234','5673', '2341', '1412'],
        'order_status': ['delivered', 'shipped', 'unavailable', 'processing']
    })

    rules = {
        'dataset': 'order',
        'primary_key': 'order_id',
        'columns': {
            'order_id': {
                'required': True,
                'unique': True
            },
            'customer_id':{
                'required': True
            },
            'order_status': {
                'required': True, 
                'severity': 'HIGH', 
                'accepted_values':['delivered', 'shipped', 'unavailable', 'processing']
        } }    }
    
    #act
    result = validate_acceptable_values(df, rules)

    #assert
    assert len(result) == 1
    print(result)

    assert result[0]['status'] == 'PASSED'
    assert result[0]['rule_name'] == 'order_status_accpetable_values'
    assert result[0]['severity'] == 'HIGH'


#failed cases - value other than one in the list, NA values to pass, severity and missing col
def test_validate_acceptable_values_when_unexpected_values_in_input():
        #arranging data
    df = pd.DataFrame({
        'order_id': ['1', '2', '3', '4'],
        'customer_id': ['2234','5673', '2341', '1412'],
        'order_status': ['delivered', 'shipped', None, 'process']
    })

    rules = {
        'dataset': 'order',
        'primary_key': 'order_id',
        'columns': {
            'order_id': {
                'required': True,
                'unique': True
            },
            'customer_id':{
                'required': True
            },
            'order_status': {'required': True, 
                             'severity': 'HIGH', 
                             'accepted_values':['delivered', 'shipped', 'unavailable', 'processing']
        } }    }
    
    #act
    result = validate_acceptable_values(df, rules)

    #assert
    assert len(result) == 1
    print(result)

    assert result[0]['status'] == 'FAILED'
    assert result[0]['rule_name'] == 'order_status_accpetable_values'
    assert result[0]['severity'] == 'HIGH'
    assert result[0]['details']['count_unexpected_values'] == 1


#missing values
def test_validate_acceptable_values_when_col_missssssing():
        #arranging data
    df = pd.DataFrame({
        'order_id': ['1', '2', '3', '4'],
        'customer_id': ['2234','5673', '2341', '1412']
   #     'order_status': ['delivered', 'shipped', '  ', 'process']
    })

    rules = {
        'dataset': 'order',
        'primary_key': 'order_id',
        'columns': {
            'order_id': {
                'required': True,
                'unique': True
            },
            'customer_id':{
                'required': True
            },
            'order_status': {'required': True, 
                             'severity': 'HIGH', 
                             'accepted_values':['delivered', 'shipped', 'unavailable', 'processing']
        } }    }
    
    #act
    result = validate_acceptable_values(df, rules)

    #assert
    assert len(result) == 1
    print(result)

    assert result[0]['status'] == 'SKIPPED'
    assert result[0]['rule_name'] == 'order_status_accpetable_values'
    assert result[0]['severity'] == 'HIGH'
