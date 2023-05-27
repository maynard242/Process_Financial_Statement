import argparse
import csv
import re
import os
from datetime import datetime

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input CSV file")
    parser.add_argument("output_file", help="path to output CSV file")
    return parser.parse_args()

def validate_file(file_path):
    """Check if file exists"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file (file_path) does not exist.")

def process_file(input_file, output_file):
    """
    Open a CSV file, read each line, validate the date and if the conditions are met,
    convert the date and write the row to the output file.
    """
    date_regex = r'\d{1,2}\s\w{3}\s\d{4}'  # regex for date in "01 Jan 2022" format
    validate_file(input_file)
    with open(input_file, 'r') as f, open(output_file, 'a+', newline='') as newf:
        reader = csv.reader(f)
        writer = csv.writer(newf)
        for row in reader:
            if len(row) > 9 and re.match(date_regex, row[0]):
                try:
                    row[0] = datetime.strptime(row[0], '%d %b %Y').strftime('%d-%m-%Y')
                    writer.writerow(row)
                except ValueError as ve:
                    print(f"Error while processing date {row[0]}: {str(ve)}")

def main():
    """Main function"""
    args = parse_args()
    process_file(args.input_file, args.output_file)

if __name__ == '__main__':
    main()

