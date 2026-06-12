import pandas as pd
import numpy as np

from dataquality.validation.result import build_result

#check min and max range for the columns where min and max mentioned
def validate_range(dataframe: pd.DataFrame, rules: dict) -> list[dict]:
    dataset = rules['dataset']
    column_rules = rules.get('columns',{})

    results: list[dict] = []

#loop through cols to find min in col list
    for col_name, rule in column_rules.items():
        expected_min_value = rule.get('min', -(np.inf))
        expected_max_value = rule.get('max', (np.inf))

        if not expected_min_value and not expected_max_value:
            continue
            
        rule_name = f"{col_name}_range"

        severity = rules.get('severity', 'HIGH')

        
        if col_name not in dataframe.columns:
            results.append(build_result(dataset = dataset, 
            rule_name = rule_name, 
            column= col_name,
            status = "SKIPPED" , 
            severity = severity, 
            expected=f"Column {col_name} should exist and not contain null values",
            actual=f"Column {col_name} is missing, so null check was skipped"))
            continue

        less_than_min_value = (pd.to_numeric(dataframe[col_name], errors='coerce') < expected_min_value).sum()

        greater_than_max_value = (pd.to_numeric(dataframe[col_name], errors='coerce')> expected_max_value).sum()

        results.append(build_result(dataset = dataset, 
        rule_name = rule_name, column= col_name,
        status = "PASSED" if less_than_min_value == 0 and greater_than_max_value == 0 else "FAILED", 
        severity = severity, 
        expected=f"Column {col_name} should have values greater than {expected_min_value} and less than {expected_max_value}",
        actual=f"Column {col_name} has {less_than_min_value} rows less than minimum value expected and {greater_than_max_value} rows greater than maximum allowed value"))

    return results