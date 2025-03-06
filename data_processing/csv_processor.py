#!/usr/bin/env python3
"""
CSV Processor Utility

This script provides various operations for processing CSV files including sorting,
filtering, and generating statistics. It uses pandas for efficient data handling
and provides detailed error reporting and column validation.

Author: Zulqurnain Haider
Email: zulqurnainjj@gmail.com
"""

import pandas as pd
import argparse
from pathlib import Path

def validate_columns(df, columns):
    """
    Validate that all columns exist in the dataframe.
    
    Args:
        df (pandas.DataFrame): The dataframe to check
        columns (str): Comma-separated list of column names
    
    Returns:
        tuple: (bool, str) indicating success and error message if any
    
    Example:
        >>> df = pd.DataFrame({'name': [], 'age': []})
        >>> validate_columns(df, 'name,age')
        (True, None)
        >>> validate_columns(df, 'name,invalid')
        (False, "Columns not found: invalid")
    """
    if not columns:
        return False, "No columns specified"
    
    column_list = columns.split(',')
    missing_columns = [col for col in column_list if col not in df.columns]
    
    if missing_columns:
        return False, f"Columns not found: {', '.join(missing_columns)}"
    return True, None

def process_csv(input_file, output_file, operation, columns=None, value=None):
    """
    Process CSV file based on the specified operation.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to save the processed CSV
        operation (str): Operation to perform ('sort', 'filter', or 'stats')
        columns (str, optional): Comma-separated list of columns to process
        value (str, optional): Value to filter by
    
    Returns:
        bool: True if operation was successful, False otherwise
    
    Example:
        >>> process_csv('input.csv', 'output.csv', 'sort', columns='name,age')
        Processed CSV saved to: output.csv
        True
    """
    try:
        # Validate input file
        input_path = Path(input_file)
        if not input_path.is_file():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Create output directory if needed
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read CSV file
        try:
            df = pd.read_csv(input_file)
        except pd.errors.EmptyDataError:
            print("Error: The CSV file is empty")
            return False
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return False
        
        # Perform the requested operation
        if operation == "sort":
            valid, error = validate_columns(df, columns)
            if not valid:
                print(f"Error: {error}")
                return False
            df = df.sort_values(by=columns.split(','))
        
        elif operation == "filter":
            valid, error = validate_columns(df, columns)
            if not valid:
                print(f"Error: {error}")
                return False
            if value is None:
                print("Error: Please specify a value for filtering")
                return False
            try:
                df = df[df[columns] == value]
                if df.empty:
                    print(f"Warning: No rows match the filter criteria")
            except Exception as e:
                print(f"Error applying filter: {str(e)}")
                return False
        
        elif operation == "stats":
            print("\nDataset Statistics:")
            print("-" * 20)
            print(f"Total Rows: {len(df)}")
            print(f"Total Columns: {len(df.columns)}")
            print("\nColumns:")
            for col in df.columns:
                null_count = df[col].isnull().sum()
                print(f"- {col}: {df[col].dtype} (Null values: {null_count})")
            print("\nNumerical Columns Summary:")
            print(df.describe())
            if output_file:
                with open(output_file, 'w') as f:
                    f.write("Dataset Statistics\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"Total Rows: {len(df)}\n")
                    f.write(f"Total Columns: {len(df.columns)}\n\n")
                    f.write("Columns:\n")
                    for col in df.columns:
                        null_count = df[col].isnull().sum()
                        f.write(f"- {col}: {df[col].dtype} (Null values: {null_count})\n")
                    f.write("\nNumerical Columns Summary:\n")
                    f.write(df.describe().to_string())
                print(f"\nStatistics saved to: {output_file}")
            return True
        
        # Save processed data
        df.to_csv(output_file, index=False)
        print(f"Processed CSV saved to: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    """
    Main function to handle command-line arguments and execute CSV processing.
    
    The script accepts the following arguments:
    1. Input CSV file path
    2. Output file path
    3. Operation to perform (sort, filter, or stats)
    4. Optional arguments:
       - --columns: Columns to process
       - --value: Value to filter by
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Process CSV files with various operations",
        epilog="For issues or suggestions, contact: zulqurnainjj@gmail.com"
    )
    parser.add_argument("input_file", help="Input CSV file path")
    parser.add_argument("output_file", help="Output file path")
    parser.add_argument(
        "--operation",
        choices=["sort", "filter", "stats"],
        required=True,
        help="Operation to perform"
    )
    parser.add_argument("--columns", help="Columns to process (comma-separated)")
    parser.add_argument("--value", help="Value to filter by")
    
    args = parser.parse_args()
    success = process_csv(args.input_file, args.output_file, args.operation, args.columns, args.value)
    if not success:
        exit(1)

if __name__ == "__main__":
    main() 