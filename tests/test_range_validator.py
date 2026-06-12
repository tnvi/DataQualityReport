import pandas as pd

from dataquality.validation.range_validator import validate_range

#success test
def test_validate_range_when_all_values_above_min():
    df = pd.DataFrame({
        'cust_id': ['10', '11'],
        'price': [34, 25]
        })

    rules ={
        'dataset': 'orders',
        'columns': {
            'price': {
                'required': True,
                'min': 10, 
                'severity': 'CRITICAL'
            }
        }}
    
    #act
    result = validate_range(df,rules)

    #assert
    assert len(result) == 1
    print(result)

    assert result[0]['column'] == 'price'
    assert result[0]['status'] == 'PASSED'
    assert result[0]['severity'] == 'HIGH'
    assert result[0]['rule_name'] == 'price_range'


def test_validate_range_when_all_values_less_max():
    df = pd.DataFrame({
        'cust_id': ['10', '11'],
        'price': [34, 25]
        })

    rules ={
        'dataset': 'orders',
        'columns': {
            'price': {
                'required': True,
                'max': 100, 
                'severity': 'CRITICAL'
            }
        }}
    
    #act
    result = validate_range(df,rules)

    #assert
    assert len(result) == 1
    print(result)

    assert result[0]['column'] == 'price'
    assert result[0]['status'] == 'PASSED'
    assert result[0]['severity'] == 'HIGH'
    assert result[0]['rule_name'] == 'price_range'


#min and max both
def test_validate_range_when_all_values_within_range():
    df = pd.DataFrame({
        'cust_id': ['10', '11'],
        'price': [34, 25]
        })

    rules ={
        'dataset': 'orders',
        'columns': {
            'price': {
                'required': True,
                'min': 10,
                'max': 100, 
                'severity': 'CRITICAL'
            }
        }}
    
    #act
    result = validate_range(df,rules)

    #assert
    assert len(result) == 1
    print(result)

    assert result[0]['column'] == 'price'
    assert result[0]['status'] == 'PASSED'
    assert result[0]['severity'] == 'HIGH'
    assert result[0]['rule_name'] == 'price_range'    


#failed: values<min, values>max, col not found, value not number
def test_validate_range_when_all_values_less_than_min():
    df = pd.DataFrame({
        'cust_id': ['10', '11'],
        'price': [4, 25]
        })

    rules ={
        'dataset': 'orders',
        'columns': {
            'price': {
                'required': True,
                'min': 10, 
                'severity': 'CRITICAL'
            }
        }}
    
    #act
    result = validate_range(df,rules)

    #assert
    assert len(result) == 1
    print(result)

    assert result[0]['column'] == 'price'
    assert result[0]['status'] == 'FAILED'
    assert result[0]['severity'] == 'HIGH'
    assert result[0]['rule_name'] == 'price_range'


def test_validate_range_when_all_values_greater_max():
    df = pd.DataFrame({
        'cust_id': ['10', '11'],
        'price': [34, 125]
        })

    rules ={
        'dataset': 'orders',
        'columns': {
            'price': {
                'required': True,
                'max': 100, 
                'severity': 'CRITICAL'
            }
        }}
    
    #act
    result = validate_range(df,rules)

    #assert
    assert len(result) == 1
    print(result)

    assert result[0]['column'] == 'price'
    assert result[0]['status'] == 'FAILED'
    assert result[0]['severity'] == 'HIGH'
    assert result[0]['rule_name'] == 'price_range'


#min and max both
def test_validate_range_when_all_values_within_range():
    df = pd.DataFrame({
        'cust_id': ['10', '11'],
        'price': [4, 125]
        })

    rules ={
        'dataset': 'orders',
        'columns': {
            'price': {
                'required': True,
                'min': 10,
                'max': 100, 
                'severity': 'CRITICAL'
            }
        }}
    
    #act
    result = validate_range(df,rules)

    #assert
    assert len(result) == 1
    print(result)

    assert result[0]['column'] == 'price'
    assert result[0]['status'] == 'FAILED'
    assert result[0]['severity'] == 'HIGH'
    assert result[0]['rule_name'] == 'price_range'    

#col not found
def test_validate_range_when_col_not_found():
    df = pd.DataFrame({
        'cust_id': ['10', '11']
       # 'price': [4, 25]
        })

    rules ={
        'dataset': 'orders',
        'columns': {
            'price': {
                'required': True,
                'min': 10, 
                'severity': 'CRITICAL'
            }
        }}
    
    #act
    result = validate_range(df,rules)

    #assert
    assert len(result) == 1
    print(result)

    assert result[0]['column'] == 'price'
    assert result[0]['status'] == 'SKIPPED'
    assert result[0]['severity'] == 'HIGH'
    assert result[0]['rule_name'] == 'price_range'

#value not string
# def test_validate_range_when_all_values_not_number():
#     df = pd.DataFrame({
#         'cust_id': ['10', '11'],
#         'price': ["aksj", 25]
#         })

#     rules ={
#         'dataset': 'orders',
#         'columns': {
#             'price': {
#                 'required': True,
#                 'min': 10, 
#                 'severity': 'CRITICAL'
#             }
#         }}
    
#     #act
#     result = validate_range(df,rules)

#     #assert
#     assert len(result) == 1
#     print(result)

#     assert result[0]['column'] == 'price'
#     assert result[0]['status'] == 'FAILED'
#     assert result[0]['severity'] == 'HIGH'
#     assert result[0]['rule_name'] == 'price_range'


