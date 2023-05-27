import argparse
import os
import pandas as pd

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Clean up Excel data.")
    parser.add_argument("input_file", help="Path to the input Excel file.")
    parser.add_argument("output_file", help="Path to the output CSV file.")
    parser.add_argument("operation", help="Specify operation to be performed: 'bank' or 'card'.")
    return parser.parse_args()

def validate_file(file_path):
    """Validate the existence of a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

def clean_data(input_file, output_file, operation):
    """
    Clean up the data from the Excel file and save it as a CSV file.
    The specific operations performed depend on the operation argument.
    """
    validate_file(input_file)

    try:
        table_1 = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading file: '{input_file}'. Error: {e}")
        return

    if operation == "bank":
        idx = table_1.index[table_1.iloc[:, 1] == 'Transaction Description'].tolist()[0]
        column_to_clean = 1
        rows_to_skip = 1
    elif operation == "card":
        idx = table_1.index[table_1.iloc[:, 0] == 'Transaction Date'].tolist()[0]
        column_to_clean = 2
        rows_to_skip = 2
    else:
        print("Invalid operation. Choose either 'bank' or 'card'.")
        return

    table_1.columns = table_1.iloc[idx, :]
    table_1 = table_1.iloc[idx+rows_to_skip:, :]

    # More complex cleaning and final extraction
    table_1.iloc[:, 0] = pd.to_datetime(table_1.iloc[:, 0])
    table_1.iloc[:, column_to_clean] = (table_1.iloc[:, column_to_clean]
                                        .str.upper()
                                        .replace("\n", " ", regex=True)
                                        .replace("-", "", regex=True)
                                        .replace("\d+", "", regex=True)
                                        .replace("  ", " ", regex=True)
                                        )

    # Save the cleaned data to a CSV file
    try:
        table_1.to_csv(output_file, header=False, index=False)
    except Exception as e:
        print(f"Error writing to file: '{output_file}'. Error: {e}")

def main():
    """Main function."""
    args = parse_args()
    clean_data(args.input_file, args.output_file, args.operation)

if __name__ == '__main__':
    main()

