import pandas as pd

from dataquality.validation.result import build_result

def validate_acceptable_values(dataframe: pd.DataFrame, rules: dict) ->list[dict]:
    dataset = rules['dataset']

    results: list[dict] = []

    columns = rules.get('columns', {})

    for col_name, rule in columns.items():
        if not rule.get('accepted_values', False):
            continue

        rule_name = f"{col_name}_accpetable_values"

        severity = rules.get('severity', 'HIGH')

        if col_name not in dataframe.columns:
            results.append(build_result(dataset, rule_name,
                                        status = "SKIPPED", severity = severity, column= col_name, 
                                        expected= f"{col_name} should be in {dataframe}",
                                        actual = f"{col_name} not in {dataframe}"))
            continue

        accepted_values = set(rule['accepted_values'])
        actual_values = set(dataframe[col_name].dropna())

#        missing_values = sorted(accepted_values - actual_values)
#        count_missing_values = pd.to_numeric(missing_values, errors='coerce').sum()
        unexpected_values = sorted(actual_values - accepted_values)
        count_unexpected_values = len(unexpected_values)

        results.append(build_result(dataset, rule_name, status="PASSED" if count_unexpected_values == 0 else "FAILED",
                                    severity=severity,  column= col_name, 
                                    expected= f"All the values in {col_name} should be from the accepted values list",
                                    actual=f"{count_unexpected_values} value(s) in {col_name} is not in accepted values list",
                                    details = {'count_unexpected_values': count_unexpected_values, 'unexpected_values': unexpected_values}))

    return results


