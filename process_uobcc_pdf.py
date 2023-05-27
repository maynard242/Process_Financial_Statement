import argparse
import os
import pandas as pd
import camelot as cm

# Constants
MONTH = {
    'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
    'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
    'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
}

YEAR = 2023


def convert_negative(value):
    parts = value.split(' ')
    if len(parts) == 2 and parts[1] == 'CR':
        parts[0] = -1 * float(parts[0])
    return parts[0]


def convert_date(text, month):
    parts = text.split(' ')
    if len(parts) == 2:
        parts[0] = parts[0] + '-' + month[parts[1]] + '-' + str(YEAR)
    return parts[0]


def process_pdf_to_csv(input_file, output_file):
    tables = cm.read_pdf(input_file, flavor='stream', pages='all')

    # Concatenate valid tables
    valid_tables = [table.df for table in tables if table.shape[1] == 4]
    if not valid_tables:
        print("No valid tables found in the PDF.")
        return

    data = pd.concat(valid_tables, ignore_index=True)
    data[3] = data[3].replace(',', '', regex=True)
    data[3] = data[3].apply(convert_negative)
    data = data[pd.to_numeric(data[3], errors='coerce').notnull()]

    # Final adjustments
    data = data[1:-2]
    data[0] = data[0].apply(convert_date, month=MONTH)
    data = data[data[0] != '']

    # Write to CSV
    data.to_csv(output_file, index=False, header=False)


def main():
    parser = argparse.ArgumentParser(description="Convert bank and credit card PDFs to CSV.")
    parser.add_argument("input_file", help="Path to the input PDF file.")
    parser.add_argument("output_file", help="Path to the output CSV file.")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"The file {args.input_file} does not exist.")
        return

    process_pdf_to_csv(args.input_file, args.output_file)


if __name__ == '__main__':
    main()

