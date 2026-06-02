import pandas as pd
import pytest

from dataquality.validation.rule_loader import load_rules

#sucess scenario
def test_load_rules_returns_dictionary_of_orders():
    #arrange data
    rules = load_rules('orders')

    assert isinstance(rules, dict)
    assert rules['dataset']=='orders'
    assert rules['source_file']=='olist_orders_dataset_plus_1000.csv'
    assert "columns" in rules 

#failre scenario
#file doesn't exists
def test_load_rules_error_missing_file():
    #arrange data
    with pytest.raises(FileNotFoundError):
        rules = load_rules('order')

#input datatype doesn't match
#def test_load_rules_error_input_type_mismatch():
#    rules = load_rules(123)

#not converted into dictionary
def test_load_rules_error_output_not_dict():
    rules = load_rules('orders')

    assert isinstance(rules,dict)

#configured_dataset != dataset_name
def test_load_rules_error_configured_dataset_mismatch(tmp_path):
    #arrange data
    dummy = tmp_path/"sample.yml"

    dummy.write_text("""dataset: payments
source_file: olist_order_payments_datset.csv
description: payment details of all the order received

composite_key:
  - order_id""")

    #act and assert
    with pytest.raises(ValueError):
        rules = load_rules('sample', tmp_path)

#empty file
def test_load_rules_error_empty_file(tmp_path):
    #arrange data
    dummy = tmp_path/"sample.yml"

    dummy.write_text(" ")

    #act and assert
    with pytest.raises(ValueError):
        rules = load_rules('sample', tmp_path)
