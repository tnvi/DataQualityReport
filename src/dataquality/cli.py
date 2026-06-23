from typing import Sequence, Any
import argparse
from pathlib import Path
import pandas as pd
from collections import Counter 
from dataquality.validation.rule_loader import load_rules
from dataquality.ingestion.csv_reader import read_csv
from dataquality.profiling.pandas_profiler import profile_dataframe
from dataquality.validation.schema_validator import validate_schema
from dataquality.validation.accepted_values_validator import validate_acceptable_values
from dataquality.validation.duplicate_validator import validate_duplicates
from dataquality.validation.range_validator import validate_range
from dataquality.validation.relationships_validator import validate_table_relationships
from dataquality.validation.required_validator import validate_required
from dataquality.storage.result_writer import write_profile_metrics, write_validation_results

import yaml
import sys

DEFAULT_RAW_DATA_DIRECTORY = Path("data/raw/olist")
DEFAULT_RULES_DIRECTORY = Path("configs/datasets")
DEFAULT_PROFILE_OUTPUT_DIR = Path("data/processed/profile_metrics")
DEFAULT_VALIDATION_OUTPUT_DIR = Path("data/processed/validation_results")

def build_parser() ->argparse.ArgumentParser :
    parser = argparse.ArgumentParser(prog= "dataquality", description= "profiles datset using YAML based dataquality rules")
    subparser = parser.add_subparsers(dest = "command", required= True)
    validate_parser = subparser.add_parser(name= 'validate', help = 'profile and validate dataset', description = "load dataset, "
    "generate profile metrics, execute configured validation rules, write the results")
    
    validate_parser.add_argument("--dataset", required= True, help= "Dataset name matching a yaml file under configs/datasets. Eg: orders" )
    validate_parser.add_argument("--input_path", required= False, type = Path, default = None, help= "Optional input file path, if omitted path is resolved from source_file value in dataset yaml config " )
    validate_parser.add_argument("--raw_data_dir", required= False, type = Path, default= DEFAULT_RAW_DATA_DIRECTORY, help= "Directory containing the raw data files" )
    validate_parser.add_argument("--rules_data_dir", required= False, type = Path, default= DEFAULT_RULES_DIRECTORY, help= "Directory containing the rules files" )
    validate_parser.add_argument("--profile_output_dir", required= False, type = Path, default= DEFAULT_PROFILE_OUTPUT_DIR, help= "Directory containing the profile verification output files" )
    validate_parser.add_argument("--validation_output_dir", required= False, type = Path, default= DEFAULT_VALIDATION_OUTPUT_DIR, help= "Directory containing the validation output files" )

    return parser

def validate_dataset(
        dataset:str, 
        input_path: Path | None=None, 
        raw_data_dir: Path = DEFAULT_RAW_DATA_DIRECTORY,
        rules_dir: Path = DEFAULT_RULES_DIRECTORY,
        profile_output_dir:Path = DEFAULT_PROFILE_OUTPUT_DIR,
        validation_output_dir: Path = DEFAULT_VALIDATION_OUTPUT_DIR
    ) -> dict[str, Any]:
    rules = load_rules(dataset, rules_dir)

    resolved_input_path = resolve_input_path(input_path, rules, raw_data_dir)

    df = read_csv(file_path= resolved_input_path)

    profile_records = profile_dataframe(df, dataset, rules.get('primary_key'), rules.get('composite_key'))
    
    referential_dataframes = load_referential_dataframe(rules, raw_data_dir, rules_dir)
    
    validation_results = run_validators(df, rules, referential_dataframes)
    
    profile_metric_path = write_profile_metrics(profile_records, dataset, profile_output_dir)

    validation_results_path = write_validation_results(validation_results, dataset, validation_output_dir)

    validations_summary = summarize_validation_results(validation_results)

    return {
        'dataset': dataset,
        'input_path': resolved_input_path,
        'row_count': len(df),
        'profile_metric_count': len(profile_records),
        'validation_summary': validations_summary,
        'profile_output_path': profile_metric_path,
        'validation_output_path': validation_results_path
    }

def run_validators(df: pd.DataFrame, rules: dict[str, Any], referential_df) -> list[dict[str, Any]]:
    validation_results: list[dict[str,Any]] =[]

    validation_results.extend(validate_schema(df, rules))
    validation_results.extend(validate_acceptable_values(df, rules))
    validation_results.extend(validate_duplicates(df, rules))
    validation_results.extend(validate_range(df, rules))
    validation_results.extend(validate_table_relationships(df, rules, referential_df))
    validation_results.extend(validate_required(df, rules))

    return validation_results 

def load_referential_dataframe(rules:dict[str, Any], raw_data_dir: Path, rules_dir) -> dict[str, pd.DataFrame]:
    relations = rules.get('relationships', [])

    referenced_datasets = {relation['references']['dataset'] for relation in relations}

    #loop through every dataset and get its data
    referenced_dfs: dict[str, pd.DataFrame] = {}

    for ds in referenced_datasets:
        yml_file = load_rules(ds, rules_dir)
        resolved_input_path = resolve_input_path(None, yml_file, raw_data_dir)
        referenced_df= read_csv(resolved_input_path)
        referenced_dfs[ds] = referenced_df
    
    return referenced_dfs

def summarize_validation_results(validation_results: list[dict[str, Any]]) -> dict[str, int]:
    Count = Counter(result.get('status', 'UNKNOWN') for result in validation_results)

    return {
        'total': len(validation_results),
        'passed': Count.get('PASSED', 0),
        'failed': Count.get('FAILED', 0),
        'skipped': Count.get('SKIPPED', 0),
        'warning': Count.get('WARNING', 0),
        'unknown': Count.get('UNKNOWN', 0)
    }

def resolve_input_path(input_path:Path|None, rules: dict[str,Any], raw_data_dir:Path) -> Path:
    if input_path is not None:
        return input_path
    
    source_file = rules.get('source_file')

    if not source_file:
        raise ValueError("Rule config does not define source file and no --input_path was provided")
    
    return raw_data_dir/source_file

def print_validation_summary(summary: dict[str,Any]) -> None:
    print()
    print("Dataquality validation completed")
    print("="*40)
    print(f"Dataset:{summary['dataset']}")
    print(f"Input path:{summary['input_path']}")
    print(f"Rows processed:{summary['row_count']}")
    print(f"Profile metrics generated:{summary['profile_metric_count']}")
    
    validation_summary = summary['validation_summary']
    print(f"Validation checks:{validation_summary['total']}")
    print(f"Passed: {validation_summary['passed']}")
    print(f"Failed: {validation_summary['failed']}")
    print(f"Skipped: {validation_summary['skipped']}")
    print(f"Warning: {validation_summary['warning']}")

    if validation_summary['unknown']>0:
        print(f"Unknown statuses: {validation_summary['unknown']}")
    
    print()
    print("Profile_metrics:")
    print(summary['profile_output_path'])

    print()
    print("validation results:")
    print(summary['validation_output_path'])

#returns exit code 0 when there is no validation failures, returns 2 if 1 or more vaalidation failed, 
# if the execution faails return 1
def main(argv: Sequence[str] | None = None) -> int:
    print(argv)
    parser = build_parser()
    # parse argv
    args = parser.parse_args(argv)
    print(args)

    
    # validate rules/ calculate profile metrics
    try:
        if args.command == "validate":
            validated_paths = validate_dataset(
                dataset = args.dataset, 
                input_path= args.input_path, 
                raw_data_dir= args.raw_data_dir, 
                rules_dir= args.rules_data_dir,
                profile_output_dir= args.profile_output_dir,
                validation_output_dir= args.validation_output_dir
            )

             # print validation summary
            print_validation_summary(validated_paths)

            # check rules and count them and return 2 in case of failures else 0 in case of success
            # return 1 in case encountering an exception

            failed_count = validated_paths['validation_summary']['failed']

            if failed_count>0:
                return 2
            return 0
        
        parser.error(f"Unsupported command: {args.command}")
        return 1



    except(
        FileNotFoundError, ValueError, KeyError, yaml.YAMLError, pd.errors.ParserError
    ) as error:
        print(f"Dataquality execution failed: {error}", file= sys.stderr)
        return 1
  

if __name__ == "__main__":
    raise SystemExit(main())