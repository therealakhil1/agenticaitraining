import pandas as pd
import numpy as np
from typing import Union, List


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values in a DataFrame:
    - For numeric columns or string columns that can be converted to integers: use median
    - For string columns: use mode

    Args:
        df: Input DataFrame with missing values

    Returns:
        DataFrame with missing values filled
    """
    # Create a copy of the dataframe to avoid modifying the original
    filled_df = df.copy()

    for column in filled_df.columns:
        # Skip if no missing values in this column
        if not filled_df[column].isna().any():
            continue

        # Check if column can be treated as numeric
        is_numeric = False

        # First, check if column is already numeric
        if pd.api.types.is_numeric_dtype(filled_df[column]):
            is_numeric = True
        else:
            # Check if string values can be converted to integers
            try:
                # Try to convert non-null values to integers
                non_null_values = filled_df[column].dropna()
                if len(non_null_values) > 0:
                    pd.to_numeric(non_null_values)
                    is_numeric = True
            except (ValueError, TypeError):
                is_numeric = False

        # Fill missing values based on column type
        if is_numeric:
            # Convert to numeric first if needed
            if not pd.api.types.is_numeric_dtype(filled_df[column]):
                filled_df[column] = pd.to_numeric(filled_df[column], errors='coerce')

            # Fill with median
            median_value = filled_df[column].median()
            filled_df[column] = filled_df[column].fillna(median_value)
            print(f"Column '{column}' filled with median: {median_value}")
        else:
            # String column - fill with mode
            mode_value = filled_df[column].mode().iloc[0] if not filled_df[column].mode().empty else "Unknown"
            filled_df[column] = filled_df[column].fillna(mode_value)
            print(f"Column '{column}' filled with mode: {mode_value}")

    return filled_df


def main():
    import argparse

    # Create argument parser
    parser = argparse.ArgumentParser(description='Fill missing values in a CSV file.')
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('output_file', help='Path to save the output CSV file')
    parser.add_argument('--encoding', default='utf-8', help='Encoding of the CSV file (default: utf-8)')
    parser.add_argument('--show-sample', action='store_true', help='Show sample of data before and after filling')

    # Parse arguments
    args = parser.parse_args()

    try:
        # Read the CSV file
        print(f"Reading CSV file: {args.input_file}")
        df = pd.read_csv(args.input_file, encoding=args.encoding)

        # Show sample of original data if requested
        if args.show_sample:
            print("\nOriginal DataFrame (first 5 rows):")
            print(df.head())

            # Count missing values
            missing_counts = df.isna().sum()
            print("\nMissing values per column:")
            print(missing_counts[missing_counts > 0])

        # Fill missing values
        print("\nFilling missing values...")
        filled_df = fill_missing_values(df)

        # Show sample of filled data if requested
        if args.show_sample:
            print("\nFilled DataFrame (first 5 rows):")
            print(filled_df.head())

        # Save the filled data to the output file
        filled_df.to_csv(args.output_file, index=False, encoding=args.encoding)
        print(f"\nFilled data saved to: {args.output_file}")

    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{args.input_file}' is empty.")
    except pd.errors.ParserError:
        print(f"Error: Could not parse '{args.input_file}'. Check if it's a valid CSV file.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()