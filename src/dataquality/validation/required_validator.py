import pandas as pd

from dataquality.validation.result import build_result

def validate_required(dataframe: pd.DataFrame, rules: dict) -> list[dict]:
    dataset = rules['dataset']

    column_rules = rules.get('columns', {})

    results: list[dict] = []

    for col_name, rule in column_rules.items():
        if not rule.get('required', False):
            continue
    
        severity_rule = rule.get('severity', 'HIGH')

        rule_name = f"{col_name}_required"

        if col_name not in dataframe.columns:
            results.append(build_result(dataset = dataset, 
            rule_name = rule_name, 
            column= col_name,
            status = "SKIPPED" , 
            severity = severity_rule, 
            expected=f"Column {col_name} should exist and not contain null values",
            actual=f"Column {col_name} is missing, so null check was skipped"))
            continue

        null_counter = int(dataframe[col_name].isna().sum())

        results.append(build_result(dataset = dataset, 
        rule_name = rule_name, 
        column= col_name,
        status = "PASSED" if null_counter == 0 else "FAILED", 
        severity = severity_rule, 
        expected=f"Column {col_name} should not contain null values",
        actual=f"Column {col_name} has {null_counter} null values"))

    return results