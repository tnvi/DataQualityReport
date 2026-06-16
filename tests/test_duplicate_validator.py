import pandas as pd

from dataquality.validation.duplicate_validator import validate_duplicates

#success test primary key - duplicate, severity, col missing
def test_validate_duplicates_when_primary_key_has_no_dups():
    #arranging data
    df = pd.DataFrame({
        'order_id': ['1', '2', '3', '4'],
        'customer_id': ['2234','5673', '2341', '1412']
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
            }
        }    }
    
    #act
    result = validate_duplicates(df, rules)

    #assert
    assert len(result) ==1

    assert result[0]['details']['key_cols'] == ['order_id']
    assert result[0]['status'] == 'PASSED'
    assert result[0]['rule_name'] == 'order_id_unique'
    assert result[0]['severity'] == 'CRITICAL'

#failure test - duplicate check
def test_validate_duplicates_when_primary_key_has_dups():
    #arranging data
    df = pd.DataFrame({
        'order_id': ['1', '2', '3', '3'],
        'customer_id': ['2234','5673', '2341', '1412']
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
            }
        }    }
    
    #act
    result = validate_duplicates(df, rules)

    #assert
    assert len(result) ==1

    assert result[0]['details']['key_cols'] == ['order_id']
    assert result[0]['status'] == 'FAILED'
    assert result[0]['rule_name'] == 'order_id_unique'
    assert result[0]['severity'] == 'CRITICAL'

#### failure test - severity check
def test_validate_duplicates_primary_key_severity_check():
    #arranging data
    df = pd.DataFrame({
        'order_id': ['1', '2', '3', '4'],
        'customer_id': ['2234','5673', '2341', '1412']
    })

    rules = {
        'dataset': 'order',
        'primary_key': 'order_id',
        'columns': {
            'order_id': {
                'required': True,
                'severity': 'HIGH'
            },
            'customer_id':{
                'required': True
            }
        }    }
    
    #act
    result = validate_duplicates(df, rules)

    #assert
    assert len(result) ==1

    assert result[0]['details']['key_cols'] == ['order_id']
    assert result[0]['status'] == 'PASSED'
    assert result[0]['rule_name'] == 'order_id_unique'
    assert result[0]['severity'] == 'HIGH'

### failure test - col missing
def test_validate_duplicates_primary_key_col_missing():
    #arranging data
    df = pd.DataFrame({
        'customer_id': ['2234','5673', '2341', '1412']
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
            }
        }    }
    
    #act
    result = validate_duplicates(df, rules)

    #assert
    assert len(result) ==1
    assert result[0]['status'] == 'SKIPPED'
    assert result[0]['rule_name'] == 'order_id_unique'
    assert result[0]['severity'] == 'CRITICAL'


#composite key
def test_validate_duplicates_composite_key_has_no_dups():
    #arranging data
    df = pd.DataFrame({
        'order_id': ['1', '2', '2', '4'],
        'order_items_id': ['2234','5673', '2341', '1412']
    })

    rules = {
        'dataset': 'order',
        'composite_key': ['order_id', 'order_items_id'],
        'columns': {
            'order_id': {
                'required': True
            },
            'order_items_id':{
                'required': True
            }
        }    }
    
    #act
    result = validate_duplicates(df, rules)

    #assert
    assert len(result) ==1

    assert result[0]['details']['key_cols'] == ['order_id', 'order_items_id']
    assert result[0]['status'] == 'PASSED'
    assert result[0]['rule_name'] == 'order_id_order_items_id_unique'
    assert result[0]['severity'] == 'CRITICAL'

#failure test - duplicate check
def test_validate_duplicates_when_composite_key_has_dups():
    #arranging data
    df = pd.DataFrame({
        'order_id': ['1', '2', '3', '3'],
        'order_items_id': ['2234','5673', '2341', '2341']
    })

    rules = {
        'dataset': 'order',
        'composite_key': ['order_id', 'order_items_id'],
        'columns': {
            'order_id': {
                'required': True,
                'unique': True
            },
            'order_items_id':{
                'required': True
            }
        }    }
    
    #act
    result = validate_duplicates(df, rules)

    #assert
    assert len(result) ==1

    assert result[0]['details']['key_cols'] == ['order_id','order_items_id']
    assert result[0]['status'] == 'FAILED'
    assert result[0]['rule_name'] == 'order_id_order_items_id_unique'
    assert result[0]['severity'] == 'CRITICAL'

#### failure test - severity check
def test_validate_duplicates_composite_key_severity_check():
    #arranging data
    df = pd.DataFrame({
        'order_id': ['1', '2', '3', '4'],
        'order_item_id': ['2234','5673', '2341', '1412']
    })

    rules = {
        'dataset': 'order',
        'composite_key': ['order_id', 'order_item_id'],
        'columns': {
            'order_id': {
                'required': True,
                'severity': 'HIGH'
            },
            'order_item_id':{
                'required': True
            }
        }    }
    
    #act
    result = validate_duplicates(df, rules)

    #assert
    assert len(result) ==1
    print(result)
    assert result[0]['details']['key_cols'] == ['order_id', 'order_item_id']
    assert result[0]['status'] == 'PASSED'
    assert result[0]['rule_name'] == 'order_id_order_item_id_unique'
    assert result[0]['severity'] == 'CRITICAL'

### failure test - col missing
def test_validate_duplicates_composite_key_col_missing():
    #arranging data
    df = pd.DataFrame({
        'order_item_id': ['2234','5673', '2341', '1412']
    })

    rules = {
        'dataset': 'order',
        'composite_key': ['order_id','order_item_id'],
        'columns': {
            'order_id': {
                'required': True,
                'unique': True
            },
            'order_item_id':{
                'required': True
            }
        }    }
    
    #act
    result = validate_duplicates(df, rules)

    #assert
    assert len(result) ==1
    assert result[0]['status'] == 'SKIPPED'
    assert result[0]['rule_name'] == 'order_id_order_item_id_unique'
    assert result[0]['severity'] == 'CRITICAL'

