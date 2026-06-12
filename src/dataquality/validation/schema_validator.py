import pandas as pd

from dataquality.validation.result import build_result

def validate_schema(dataframe: pd.DataFrame, rules: dict) -> list[dict]:
    dataset = rules['dataset']

#    rules['columns'].keys()
    expected_columns = set(rules.get('columns', {}).keys())
    actual_columns = set(dataframe.columns)

    missing_cols = sorted(expected_columns - actual_columns)
    unexpected_cols = sorted(actual_columns - expected_columns)

    results: list[dict] = []

    # if missing_cols: 
    #     results.append(build_result(dataset = dataset, 
    #     rule_name = 'schema_expected_cols_present', 
    #     status = 'FAILED', 
    #     severity = "CRITICAL", 
    #     expected = f"Expected columns: {expected_columns}", 
    #     actual = f"Missing columns: {missing_cols}"  ))
    
    # else:
    #     results.append(build_result(dataset = dataset, 
    #     rule_name = 'schema_expected_cols_present', 
    #     status = 'PASSED', 
    #     severity = "CRITICAL", 
    #     expected = f"Expected columns: {expected_columns}", 
    #     actual = "All expected columns are present" ))
    

    results.append(build_result(dataset = dataset, 
    rule_name = 'schema_expected_cols_present', 
    status = ('FAILED' if missing_cols else 'PASSED'), 
    severity = "CRITICAL", 
    expected = f"Expected columns: {expected_columns}", 
    actual = f"Missing columns: {missing_cols}"  ))

    results.append(build_result(dataset = dataset, 
    rule_name = 'schema_unexpected_cols_present', 
    status = ('WARNING' if unexpected_cols else 'PASSED'), 
    severity = "LOW", 
    expected = f"Expected columns: {expected_columns}", 
    actual = f"Unexpected columns: {unexpected_cols}"  ))

    return results
