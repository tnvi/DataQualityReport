import pandas as pd

from dataquality.validation.relationships_validator import validate_table_relationships

#succees
def test_validate_table_relationships_when_all_relations_mapped_correctly():
    #arranging data
    df1 = pd.DataFrame({
        'order_id': ['1', '2', '3'],
        'customer_id': ['2234','5673', '2341']
    })

    df2 = pd.DataFrame({
        'cust_name': ['a', 'b', 'c', 'd'],
        'customer_id': ['2234','5673', '2341', '1412']
    })

    rules = {
        'dataset': 'order',       
        'relationships':
        [{
            'column': 'customer_id' ,
            'references': {'dataset': 'customers', 'column': 'customer_id'}, 
            'severity': 'HIGH'
        }]
    }

    #act
    result = validate_table_relationships(df1, rules, {'customers':df2})

    #assert
    assert len(result) == 1

    assert result[0]['rule_name'] == 'customer_id_references_customers_customer_id'
    assert result[0]['status'] == "PASSED"
    assert result[0]['severity'] == "HIGH"

#fail test - value not in referrenced dataset, col not in referrenced df, referrenced df doesn't exsits, 
# foreign key col doen't exsist in original df
def test_validate_table_relationships_when_foreign_key_col_not_in_df():
    #arranging data
    df1 = pd.DataFrame({
        'order_id': ['1', '2', '3']
        })

    df2 = pd.DataFrame({
        'cust_name': ['a', 'b', 'c', 'd'],
        'customer_id': ['2234','5673', '2341', '1412']
    })

    rules = {
        'dataset': 'order',       
        'relationships':
        [{
            'column': 'customer_id' ,
            'references': {'dataset': 'customers', 'column': 'customer_id'}, 
            'severity': 'HIGH'
        }]
    }

    #act
    result = validate_table_relationships(df1, rules, {'customers':df2})

    #assert
    assert len(result) == 1

    assert result[0]['rule_name'] == 'customer_id_references_customers_customer_id'
    assert result[0]['status'] == "SKIPPED"
    assert result[0]['severity'] == "HIGH"

#referrenced df doesn't exsits
def test_validate_table_relationships_when_referrenced_df_not_found():
    #arranging data
    df1 = pd.DataFrame({
        'order_id': ['1', '2', '3'],
        'customer_id': ['2234','5673', '2341']
    })

    df2 = pd.DataFrame({
        'cust_name': ['a', 'b', 'c', 'd'],
        'customer_id': ['2234','5673', '2341', '1412']
    })

    rules = {
        'dataset': 'order',       
        'relationships':
        [{
            'column': 'customer_id' ,
            'references': {'dataset': 'customers', 'column': 'customer_id'}, 
            'severity': 'HIGH'
        }]
    }

    #act
    result = validate_table_relationships(df1, rules, {'cust':df2})

    #assert
    assert len(result) == 1

    assert result[0]['rule_name'] == 'customer_id_references_customers_customer_id'
    assert result[0]['status'] == "SKIPPED"
    assert result[0]['severity'] == "HIGH"

#referrenced col doesn't exsits in ref df
def test_validate_table_relationships_when_referrenced_key_not_found():
    #arranging data
    df1 = pd.DataFrame({
        'order_id': ['1', '2', '3'],
        'customer_id': ['2234','5673', '2341']
    })

    df2 = pd.DataFrame({
        'cust_name': ['a', 'b', 'c', 'd']
    })

    rules = {
        'dataset': 'order',       
        'relationships':
        [{
            'column': 'customer_id' ,
            'references': {'dataset': 'customers', 'column': 'customer_id'}, 
            'severity': 'HIGH'
        }]
    }

    #act
    result = validate_table_relationships(df1, rules, {'customers':df2})

    #assert
    assert len(result) == 1

    assert result[0]['rule_name'] == 'customer_id_references_customers_customer_id'
    assert result[0]['status'] == "SKIPPED"
    assert result[0]['severity'] == "HIGH"

#ref value not in ref df
def test_validate_table_relationships_when_referrenced_value_not_found():
    #arranging data
    df1 = pd.DataFrame({
        'order_id': ['1', '2', '3'],
        'customer_id': ['2234','5673', '2342']
    })

    df2 = pd.DataFrame({
        'cust_name': ['a', 'b', 'c', 'd'],
        'customer_id': ['2234','5673', '2341', '1412']
    })

    rules = {
        'dataset': 'order',       
        'relationships':
        [{
            'column': 'customer_id' ,
            'references': {'dataset': 'customers', 'column': 'customer_id'}, 
            'severity': 'HIGH'
        }]
    }

    #act
    result = validate_table_relationships(df1, rules, {'customers':df2})

    #assert
    assert len(result) == 1

    assert result[0]['rule_name'] == 'customer_id_references_customers_customer_id'
    assert result[0]['status'] == "FAILED"
    assert result[0]['severity'] == "HIGH"
