import pandas as pd
import pytest
from dataquality.storage.result_writer import write_to_csv, write_profile_metrics, write_validation_results

#create csv
def test_write_to_csv_creates_file(tmp_path):
    #arrange data
    records = [
        {
            'order_id': 1,
            'amount': 34        
        },
        {
            'order_id': 2,
            'amount': 345
        }
    ]

#arrange output path
    output_path = tmp_path/"test_folder/output_test/sample_records.csv"

#act
    path = write_to_csv(records, output_path)
    
    #assert
    assert path == output_path
    assert output_path.exists()
    
    df = pd.read_csv(output_path)
    
    assert df.shape == (2,2)
    print(df)
    print(df.columns)
    assert set(df.columns) == {'order_id', 'amount'}
    
    assert df.iloc[0,1] == 34

def test_write_profile_metrics_creates_file(tmp_path ):
 #arrange data
    records = [
        {
            'order_id': 1,
            'amount': 34        
        },
        {
            'order_id': 2,
            'amount': 345
        }
    ]

#act
    path = write_profile_metrics(records, 'orders', tmp_path)    

#assert
    assert path.parent == tmp_path
    assert path.name == "orders_profile_metrics.csv"
    assert path.exists()
    
def test_write_validation_results_creates_file(tmp_path):
    
 #arrange data
    records = [
        {
            'order_id': 1,
            'amount': 34        
        },
        {
            'order_id': 2,
            'amount': 345
        }
    ]

#act
    path = write_validation_results(records, 'orders', tmp_path)    

#assert
    assert path.parent == tmp_path
    assert path.name == "orders_validation_results.csv"
    assert path.exists()

