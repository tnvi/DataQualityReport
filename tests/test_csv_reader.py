import pandas as pd
import pytest 

from dataquality.ingestion.csv_reader import read_csv

#sucess scenario
def test_read_csv_returns_dataframe(tmp_path):
    #arranging data
    csv_file = tmp_path/"sample.csv"

    csv_file.write_text("ID,name\n 1,namesake\n 2,anything")

#acting
    df = read_csv(csv_file)

#asserting
    assert isinstance(df,pd.DataFrame)
    assert df.shape==(2,2)
    assert list(df.columns)==['ID', 'name']

#failure scenarios
def test_read_csv_error_for_non_csv_file(tmp_path):
    #arranging the data
    text_file = tmp_path/"sample.txt"

    text_file.write_text("ID,name\n 1,namesake\n 2,anything")
    
    #acting   and asserting
    with pytest.raises(ValueError):
        df = read_csv(text_file)
 

def test_read_csv_error_missing_file(tmp_path):
    # arranging data 
    csv_file = tmp_path/"no_data.csv"

    #acting and asserting    
    
    with pytest.raises(FileNotFoundError):
        df = read_csv(csv_file)

        