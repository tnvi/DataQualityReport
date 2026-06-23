from dataquality.validation.result import build_result
import pandas as pd

def validate_table_relationships(dataframe:pd.DataFrame, rules:dict, referential_dataframes: dict[str,pd.DataFrame]) -> list[dict]:
    dataset = rules['dataset']

    relationships = rules.get('relationships', [])
    results: list[dict] =[]

    for relation in relationships:
        foreign_key = relation['column']

        referenced_dataset = relation['references']['dataset']
        referenced_column = relation['references']['column']
        severity = relation.get('severity', 'HIGH')

        rule_name = f"{foreign_key}_references_{referenced_dataset}_{referenced_column}"

        if foreign_key not in dataframe.columns:
            results.append(build_result(dataset=dataset, rule_name=rule_name,
                                        status="SKIPPED", severity=severity,
                                        expected= f"{foreign_key} should be available in {dataframe}",
                                        actual = f"{foreign_key} not available in {dataframe}"
                                        ))
            continue
            
        if referenced_dataset not in referential_dataframes:
            results.append(build_result(dataset=dataset, rule_name=rule_name,
                                        status = "SKIPPED", severity = severity,
                                        expected = f"{referenced_dataset} should be in {referential_dataframes}",
                                        actual = f"{referenced_dataset} is not avialble in {referential_dataframes}"))
            continue

        referenced_dataframe = referential_dataframes[referenced_dataset]

        if referenced_column not in referenced_dataframe.columns:
            results.append(build_result(dataset=dataset, rule_name=rule_name,
                                        status = "SKIPPED", severity = severity,
                                        expected = f"{referenced_column} should be in {referenced_dataframe}",
                                        actual = f"{referenced_column} is not avialble in {referenced_dataframe}"))
            continue

        local_col_values = dataframe[foreign_key].dropna()
        reference_col_values = set(referenced_dataframe[referenced_column].dropna())

        missing_col_values = ~local_col_values.isin(reference_col_values)
        missing_values_count = int((missing_col_values).sum())

        sample_missing_values = local_col_values[missing_col_values].astype(str).drop_duplicates().head().tolist()

        results.append(build_result(dataset, rule_name, status="PASSED" if missing_values_count == 0 else "FAILED",
                                    severity=severity,
                                    expected= f"All values of {referenced_column} should be available in {referenced_column} of {referenced_dataframe}",
                                    actual = f"{missing_values_count} are not available in {referenced_column} of {referenced_dataframe}",
                                    details = f"Sample of missing values: {sample_missing_values}"))

    return results