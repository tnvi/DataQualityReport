import pandas as pd

from dataquality.validation.result import build_result

def validate_duplicates(dataframe: pd.DataFrame, rules:dict) -> list[dict]:
    dataset = rules['dataset']
    
    results: list[dict] = []

    #check if there are dups in primary key and composite key
    if 'primary_key' in rules:
        primary_key = rules['primary_key']

        key_cols = [primary_key]

        rule_name = f"{primary_key}_unique"

        #severity = rules['columns'][primary_key]['severity']

        severity = (rules
                    .get('columns', {})
                    .get(primary_key, {})
                    .get('severity', 'CRITICAL'))

    elif 'composite_key' in rules:
        composite_key = rules['composite_key']

        key_cols = composite_key

        rule_name = f"{"_".join(composite_key)}_unique"

        severities = [rules.get('columns', {}).get(key, {}).get('severity', 'CRITICAL')
                      for key in composite_key]
        
        severity_order = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM':2, 'LOW':1}

        severity = max(severities, key= lambda s:severity_order.get(s,0))

    else:
        results.append(build_result(dataset, rule_name='No_unique_key_configured', 
                                    status= "SKIPPED", severity= 'Low', 
                                    expected= "Composite key or primary key should have been configured",
                                    actual= "No primary or composite key configured"))
        
        return results
    
    actual_cols = set(dataframe.columns)
    missing_cols = set(key_cols) - actual_cols

    if missing_cols:
        results.append(build_result(dataset = dataset, 
        rule_name = rule_name, 
        status = "SKIPPED" , 
        severity = severity, 
        expected=f"Key Column(s) {key_cols} should exist",
        actual=f"Key Column(s) {missing_cols} is missing"))
        
        return results

    dups_count = int(dataframe.duplicated(key_cols, keep = False).sum())

    results.append(build_result(dataset, rule_name=rule_name, 
                                status= "PASSED" if dups_count == 0 else "FAILED",
                                severity= severity,
                                expected = f"Key columns should uniquely identify rows: {key_cols}",
                                actual = f"{dups_count} duplicate key rows found",
                                details = {'key_cols': key_cols, 'duplicate_count': dups_count}
                                ))
    
    return results
