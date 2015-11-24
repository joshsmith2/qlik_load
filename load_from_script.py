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
    parser.add_argument("-o", "--out-file", metavar="PATH", type="str",
                        dest="out_file", help="The load script")
    parser.add_argument("-h", "--header-file", metavar="PATH", type="str",
                        dest="header_file",
                        help="Path to a file containing a standard load script"
                             " header - usually a bunch of SET statements for "
                             "timestamps etc")

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


def print_header(header_file, out_file):
    """
    Print the Qlikview header to the out file

    :param header_file: A .txt file containing the desired Qlikview header
    (Usually a bunch of SET statements for DateTime formats etc)
    :param out_file: File to write to
    """
    with open(out_file, 'w') as of:
        with open(header_file, 'r') as hf:
            for line in hf.readlines():
                of.write(line)


def print_table_writer(out_file, headers, csv_file):
    """
    Print a load script to write headers into out_file
    """
    # Name of the table in QV to store the data into
    table_name = "tweets"

    with open(out_file, 'a') as o:
        o.write("\n")
        o.write("{}:\n".format(table_name))
        o.write("LOAD\n")
        for header in headers[:-1]:
            o.write("\t[{}],\n".format(header))
        o.write("\t[{}]\n\n".format(headers[-1]))
        o.write("FROM\n")
        o.write("[{}]\n".format(csv_file))
        o.write("(txt, codepage is 1252, embedded labels, delimiter is ',', "
                "msq);")


def main():
    out_file_default = "load_out.txt"
    header_file_default = "standard_contents/header.txt"

    args = get_arguments()
    csv_path = args.csv

    try:
        out_file = args.out_file
    except:
        out_file = out_file_default

    # If header file exists, print it to the output file
    try:
        header_file = args.header_file
    except:
        header_file = header_file_default

    print_header(header_file, out_file)
    headers = get_headers(csv_path)


if __name__ == "__main__":
    main()
