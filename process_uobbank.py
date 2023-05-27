import argparse
import os
import pandas as pd

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Clean up Excel data.")
    parser.add_argument("input_file", help="Path to the input Excel file.")
    parser.add_argument("output_file", help="Path to the output CSV file.")
    return parser.parse_args()

def validate_file(file_path):
    """Check if file exists."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

def clean_data(input_file, output_file):
    """
    Clean up the data from the Excel file and save it as a CSV file.
    """
    validate_file(input_file)

    try:
        table_1 = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading file: {input_file}. Error: {e}")
        return

    # Simple cleaning up
    idx = table_1.index[table_1.iloc[:, 1] == 'Transaction Description'].tolist()[0]
    table_1.columns = table_1.iloc[idx, :]
    table_1 = table_1.iloc[idx+1:, :]

    # More complex cleaning and final extraction
    table_1.iloc[:, 0] = pd.to_datetime(table_1.iloc[:, 0])
    table_1.iloc[:, 1] = (table_1.iloc[:, 1]
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
        print(f"Error writing to file: {output_file}. Error: {e}")

def main():
    """Main function."""
    args = parse_args()
    clean_data(args.input_file, args.output_file)

if __name__ == '__main__':
    main()

