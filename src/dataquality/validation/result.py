from typing import Any

def build_result(
        dataset: str, 
        rule_name: str, 
        status: str, 
        severity: str, 
        expected: str, 
        actual: str, 
        column: str | None = None, 
        details: dict[str, Any] | None = None
    ) -> dict[str,Any]:
    return {
        'dataset': dataset, 
        'rule_name': rule_name,
        'column': column,
        'status': status,
        'severity': severity,
        'expected': expected,
        'actual': actual,
        'details': details or {}
    }