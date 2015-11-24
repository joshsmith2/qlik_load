__author__ = 'josh'

import csv
import argparse


def get_arguments():
    """
    Parse command line arguments

    :return: An array of args
    """
    parser = argparse.ArgumentParser(description="Create a Qlikview load "\
                                                 "script from an arbitary "\
                                                 "CSV.")
    parser.add_argument("-c", "--csv-file", metavar="PATH", type="str",
                        dest='csv', help="The CSV file to read")
    return parser.parse_args()

def get_headers(from_file):
    """
    Get CSV headers

    :param from_file: CSV file to return headers from
    :return: List of strings, CSV headers
    """
    with open(from_file, 'r') as ff:
        reader = csv.DictReader(ff)
        return reader.fieldnames

def main():
    args = get_arguments()
    csv_path = args.csv
    headers = get_headers(csv_path)

if __name__ == "__main__":
    main()
