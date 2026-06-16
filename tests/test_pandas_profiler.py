import pandas as pd

from dataquality.profiling.pandas_profiler import profile_dataframe

def test_profile_dataframe_returns_dataset_metrics():
    #arrange
    df = pd.DataFrame({
        'order_id': ['1', '2', '3'],
        'amount': [123, 3456, 567]
    })
    #act
    records = profile_dataframe(df, 'orders', primary_key= 'order_id')

    #assert

    assert len(records) == 15

 #   metric_names = for a in records: a.metric_names
    metric_names = {a['metric_name'] for a in records}

    assert 'row_count' in metric_names
    assert 'column_count' in metric_names
    assert 'duplicate_key_count' in metric_names

    for record in records:
        if record['metric_name'] == 'row_count':
            assert record['metric_value'] == 3

        if record['metric_value'] == 'column_count':
            assert record['metric_value'] == 3

        if record['metric_value'] == 'duplicate_key_count':
            assert record['duplicate_key_count'] == 0


#incomplete soltuion
def test_profile_dataframe_returns_null_and_distinct_counts():
    df = pd.DataFrame(
        {
        'order_id': ['1', '2', '3', '3'],
        'amount': [123, None, 567, 567 ]
        }
    )

    #act
    records = profile_dataframe(df, 'orders')

    #assert
    for record in records:
        if record['column'] ==  'order_id' and record['metric_name'] == 'null_count':
            assert record['metric_value'] == 0

        if record['column'] == 'order_id' and record['metric_name'] == 'distinct_count':
            assert record['metric_value'] == 3

        if record['column'] == 'order_id' and record['metric_name'] == 'data_type':
            print(record)
            assert record['metric_value'] == 'str'

        if record['column'] ==  'amount' and record['metric_name'] == 'null_count':
            assert record['metric_value'] == 1

        if record['column'] == 'amount' and record['metric_name'] == 'distinct_count':
            assert record['metric_value'] == 2

        if record['column'] == 'amount' and record['metric_name'] == 'data_type':
            print(record)
            assert record['metric_value'] == 'float64'

        

## alternative complete solution 
# # def test_profile_dataframe_returns_null_and_distinct_counts():
#     records = profile_dataframe(df, "orders")

#     # 1. Define exactly what combinations MUST exist and their expected values
#     expected_metrics = {
#         ("order_id", "null_count"): 0,
#         ("order_id", "distinct_count"): 3,
#         ("order_id", "data_type"): "string",
#         ("amount", "null_count"): 1,
#         ("amount", "distinct_count"): 2,
#     }

#     # 2. Track which expected combinations we actually find
#     found_metrics = {}

#     for record in records:
#         col = record.get("column")
#         metric = record.get("metric_name")
#         val = record.get("metric_value")

#         # If it's a metric we care about, log its value
#         if (col, metric) in expected_metrics:
#             found_metrics[(col, metric)] = val

#     # 3. Assert that every single expected metric was found
#     assert set(expected_metrics.keys()) == set(found_metrics.keys()), (
#         f"Missing expected metrics! "
#         f"Expected: {list(expected_metrics.keys())}, "
#         f"Found: {list(found_metrics.keys())}"
#     )

#     # 4. Assert that all found metrics have the correct values
#     for metric_pair, expected_value in expected_metrics.items():
#         assert found_metrics[metric_pair] == expected_value, (
#             f"Value mismatch for {metric_pair}! "
#             f"Expected {expected_value}, got {found_metrics[metric_pair]}"
#         )

def test_profile_dataframe_returns_duplicate_primary_key_count():
#arrange
    df = pd.DataFrame(
        {
        'order_id': ['1', '2', '3', '3'],
        'amount': [123, None, 567, 567 ]
        }
    )

#act
    records = profile_dataframe(df, 'orders', primary_key= 'order_id')

    #assert
    metric_names = {a['metric_name'] for a in records}

    assert 'duplicate_key_count' in metric_names

    for record in records:
        if record['metric_name'] == 'duplicate_key_count':
            assert record['metric_value'] ==2
        

def test_profile_dataframe_returns_no_primary_key_count():
#arrange
    df = pd.DataFrame(
        {
        
        'amount': [123, None, 567, 567 ]
        }
    )

#act
    records = profile_dataframe(df, 'orders', primary_key= 'order_id')

    #assert
    metric_names = {a['metric_name'] for a in records}

    assert 'duplicate_key_count' not in metric_names



def test_profile_dataframe_returns_no_primary_key_no_composite_key():
#arrange
    df = pd.DataFrame(
        {
        
        'amount': [123, None, 567, 567 ]
        }
    )

#act
    records = profile_dataframe(df, 'orders')

    #assert
    metric_names = {a['metric_name'] for a in records}

    assert 'duplicate_key_count' not in metric_names


def test_profile_dataframe_returns_duplicate_composite_key_count():
#arrange
    df = pd.DataFrame(
        {
        'order_id': ['1', '2', '3', '3'],
        'order_item_id': [123, 123, 567, 567 ]
        }
    )

#act
    records = profile_dataframe(df, 'orders', composite_key= ['order_id', 'order_item_id'])

    #assert
    metric_names = {a['metric_name'] for a in records}

    assert 'duplicate_key_count' in metric_names

    for record in records:
        if record['metric_name'] == 'duplicate_key_count':
            assert record['metric_value'] ==2



def test_profile_dataframe_returns_no_composite_key_count():
#arrange
    df = pd.DataFrame(
        {
         'order_id': ['1', '2', '3', '3'],
        'amount': [123, None, 567, 567 ]
        }
    )

#act
    records = profile_dataframe(df, 'orders', composite_key= ['order_id', 'order_item_id'])

    #assert
    metric_names = {a['metric_name'] for a in records}

    assert 'duplicate_key_count' not in metric_names


#min max
def test_profile_dataframe_returns_min_max():
    #arrange
    df = pd.DataFrame(
        {
        'order_id': ['1', '2', '3', '3'],
        'order_item_id': [123, 123, 567, 567 ],
        'freight': [None, None, None, None],
        'price': [234, 234, 85, None]
        }
    )

#act
    records = profile_dataframe(df, 'orders')

    #assert
    for record in records:
        if record['metric_name'] == 'minimum_value' and record['column'] == 'order_id':
            assert record['metric_value'] ==  '1'

        if record['metric_name'] == 'maximum_value' and record['column'] == 'order_id':
            assert record['metric_value'] == '3'

        if record['metric_name'] == 'minimum_value' and record['column'] == 'order_item_id':
            assert record['metric_value'] ==  123

        if record['metric_name'] == 'maximum_value' and record['column'] == 'order_item_id':
            assert record['metric_value'] == 567

        if record['metric_name'] == 'minimum_value' and record['column'] == 'price':
            assert record['metric_value'] == 85

        if record['metric_name'] == 'maximum_value' and record['column'] == 'price':
            assert record['metric_value'] == 234

        if record['metric_name'] == 'minimum_value' and record['column'] == 'freight':
            assert record['metric_value'] ==  None

        if record['metric_name'] == 'maximum_value' and record['column'] == 'freight':
            assert record['metric_value'] == None

    metric_names = {a['metric_name'] for a in records if a['column'] == 'freight'}
    assert 'minimum_value' not in metric_names
    assert 'maximum_value' not in metric_names