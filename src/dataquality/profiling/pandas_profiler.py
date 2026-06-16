from typing import Any
import pandas as pd

def profile_dataframe(df: pd.DataFrame, dataset: str, primary_key: str | None = None, composite_key: list[str] | None = None)-> list[dict[str,Any]]:
    result: list[dict] = []

    row_count = len(df)
    col_count = len(df.columns)

    result.append({
        'dataset': dataset,
        'metric_scope': 'dataset',
        'column': None,
        'metric_name': 'row_count',
        'metric_value': row_count
    })

    result.append({
        'dataset': dataset,
        'metric_scope': 'dataset',
        'column': None,
        'metric_name': 'column_count',
        'metric_value': col_count
    })

    duplicate_key_count = _calculate_duplicate_key_count(df, primary_key, composite_key)

    if duplicate_key_count is not None:
        result.append({
            'dataset': dataset,
            'metric_scope': 'dataset',
            'column': None,
            'metric_name': 'duplicate_key_count',
            'metric_value': duplicate_key_count
        })

    for col in df.columns:
        column = df[col]

        null_count = int(column.isna().sum())

        null_percentage = round((null_count/row_count)*100,2) if row_count > 0 else 0

        distinct_count = column.nunique(dropna = True)

        result.extend(
            [
                {
                    'dataset': dataset,
                    'metric_scope': 'column',
                    'column': col,
                    'metric_name': 'null_count',
                    'metric_value': null_count
                },
                {
                    'dataset': dataset,
                    'metric_scope': 'column',
                    'column': col,
                    'metric_name': 'null_percentage',
                    'metric_value': null_percentage
                },
                {
                    'dataset': dataset,
                    'metric_scope': 'column',
                    'column': col,
                    'metric_name': 'distinct_count',
                    'metric_value': distinct_count
                },
                {
                    'dataset': dataset,
                    'metric_scope': 'column',
                    'column': col,
                    'metric_name': 'data_type',
                    'metric_value': pd.api.types.infer_dtype(column) if column.dtype == 'object' else str(column.dtype) 
                }
            ]
        )

        min,max = _safe_min_max(column)

        if min is not None:
            result.append(
                {
                    'dataset': dataset,
                    'metric_scope': 'column',
                    'column': col,
                    'metric_name': 'minimum_value',
                    'metric_value': min
                }
            )

        if max is not None:
            result.append(
                {
                    'dataset': dataset,
                    'metric_scope': 'column',
                    'column': col,
                    'metric_name': 'maximum_value',
                    'metric_value': max
                }
            )

    return result



def _calculate_duplicate_key_count(df:pd.DataFrame, primary_key: str | None = None, composite_key: list[str] | None = None) -> int | None:
    if primary_key:
        key_cols = [primary_key]
    elif composite_key:
        key_cols = composite_key
    else:
        return None
    
    missing_cols = [col for col in key_cols if col not in df.columns]

    if missing_cols:
        return None
    
    return df.duplicated(subset = key_cols, keep= False).sum()
 
def _safe_min_max(column: pd.Series) -> (tuple[int | None, int | None]):
    column  = column.dropna()

    if column.empty:
        return None, None
    
    try:
        min = _to_output_value(column.min())
        max = _to_output_value(column.max())

        return min, max

    except TypeError:
        return None, None
    
def _to_output_value(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()
    return value