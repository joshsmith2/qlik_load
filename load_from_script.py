__author__ = 'josh'

import csv
import argparse
import os

def get_arguments():
    """
    Parse command line arguments

    :return: An array of args
    """
    parser = argparse.ArgumentParser(description="Create a Qlikview load "\
                                                 "script from an arbitary "\
                                                 "CSV.")
    parser.add_argument("-d", "--csv-file", metavar="PATH", type=str,
                        dest="csv", help="The CSV file to read")
    parser.add_argument("-o", "--out-file", metavar="PATH", type=str,
                        dest="out_file", help="The load script")
    parser.add_argument("-f", "--header-file", metavar="PATH", type=str,
                        dest="header_file",
                        help="Path to a file containing a standard load script"
                             " header - usually a bunch of SET statements for "
                             "timestamps etc")
    parser.add_argument("-c", "--conversion-table", metavar="PATH", type=str,
                        dest="conversion_table",
                        help="Path to a structured CSV file containing common "
                             "conversions from column names to human readable"
                             " names.")

    return parser.parse_args()


def get_headers(from_file):
    """
    Get CSV headers

    :param from_file: CSV file to return headers from
    :return: List of strings, CSV headers
    """
    with open(from_file, 'r', encoding="utf8") as ff:
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


def load_conversion_table(table_file):
    """
    Load the file which defines common column heading conversions.

    :return: A dictionary containing the following for each row:
        field_from_csv: The field in the original CSV file to convert if found
            e.g twitter.tweet/text
        modifier: Any functions to apply to the field before it is converted
            e.g lower([twitter.tweet/text])
        conversion: The new name for the field
            e.g T_Text
    """
    out_dicts = []
    with open(table_file, 'r', encoding="utf-8") as t_f:
        reader = csv.DictReader(t_f)
        for row in reader:
            #There's almost certainly a better way of doing this
            out_dicts.append(row)
    return out_dicts

def print_table_writer(out_file, headers, conversions, csv_file):
    """
    Print a load script to write headers into out_file
    """
    # Name of the table in QV to store the data into
    table_name = "tweets"

    with open(out_file, 'a') as o:
        o.write("\n")
        o.write("{}:\n".format(table_name))

        # T_ID is a primary key - if it's there, load it as distinct
        if "twitter.tweet/id" in headers:
            o.write("LOAD DISTINCT [twitter.tweet/id] as T_ID,\n")
            headers.remove("twitter.tweet/id")
        else:
            o.write("LOAD\n")


        for header in headers:
            conversion_found = False
            for conversion in conversions:
                if header == conversion['field_from_csv']:
                    if conversion['modifier']:
                        o.write("\t{} as {},\n".format(conversion['modifier'],
                                                     conversion['conversion']))
                        conversion_found = True
                    else:
                        o.write("\t[{}] as {},\n".format(header,
                                                     conversion['conversion']))
                        conversion_found = True
            if not conversion_found:
                o.write("\t[{}],\n".format(header))
            if header == "twitter.tweet/created":
                with open("standard_contents/time_processing.txt", 'r') as scf:
                    for line in scf.readlines():
                        o.write("\t" + line)

        o.write("\t1 as Count\n\n")
        o.write("FROM\n")
        o.write("[{}]\n".format(csv_file))
        o.write("(txt, codepage is 1252, embedded labels, delimiter is ',', "
                "msq);")


def main():
    out_file_default = "load_out.txt"
    header_file_default = os.path.join("standard_contents","header.txt")
    conversion_table_default = os.path.join("standard_contents",
                                           "conversion_table.csv")
    args = get_arguments()
    csv_path = args.csv

    # Set variable defaults
    if not args.out_file:
        out_file = out_file_default
    else:
        out_file = args.out_file

    if not args.header_file:
        header_file = header_file_default
    else:
        out_file = args.header_file

    if not args.conversion_table:
        conversion_table = conversion_table_default
    else:
        conversion_table = args.conversion_table

    print_header(header_file, out_file)
    headers = get_headers(csv_path)
    conversions = load_conversion_table(conversion_table)
    print_table_writer(out_file, headers, conversions, csv_path)


if __name__ == "__main__":
    main()
