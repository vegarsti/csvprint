import argparse
import sys
import csv
from itertools import islice
from .parse_types import *


def create():
    """Set up and return the parser"""
    script_name = "csvprint"
    parser = argparse.ArgumentParser(
        description="Command line utility for pretty printing csv files.",
        formatter_class=argparse.RawTextHelpFormatter,
        prog=script_name,
    )
    parser.add_argument("filename", type=str, help="file to pretty print", nargs="?")
    parser.add_argument(
        "-s",
        "--separator",
        default=",",
        help="separator/delimiter used in csv file\ndefault is comma: ','\nuse 'tab' for tab separated files\n",
        type=separator,
    )
    parser.add_argument(
        "-n",
        "--rows",
        type=positive_integer,
        default=sys.maxsize,
        help="number of rows to show",
    )
    parser.add_argument(
        "-a",
        "--align",
        nargs="+",
        default=["<"],
        help="which alignment to use\ndefault is left\nchoices: {l, r}\n"
        + "can provide a list, in which case\none choice for each column",
        type=alignment,
    )
    parser.add_argument(
        "-d",
        "--decorator",
        type=str,
        default="",
        help="which string/decorator to use in spacing",
    )
    parser.add_argument(
        "-p", "--padding", type=non_negative_integer, default=1, help="padding"
    )
    parser.add_argument(
        "-c",
        "--columns",
        type=int,
        nargs="*",
        metavar="column",
        help="select columns to print (1-indexed)",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--header", action="store_true", help="header decoration")
    group.add_argument("--markdown", action="store_true", help="output markdown table")
    group.add_argument("--latex", action="store_true", help="output latex table")
    return parser


def print_message_and_exit(parser, message):
    """Print parser usage and the error message provided"""
    script_name = "csvprint"
    parser.print_usage()
    print("{}: error:".format(script_name), end=" ")
    print(message)
    sys.exit()


def file_error_checking(parser, filename):
    """Check the file or pipe provided to the parser is correct"""
    reading_from_pipe = not sys.stdin.isatty() and filename == None
    if reading_from_pipe:
        file = sys.stdin
    elif filename == None:
        print_message_and_exit(parser, "required: filename or pipe")
    else:
        try:
            file = open(filename)
        except FileNotFoundError:
            print_message_and_exit(parser, "no such file: {}".format(filename))
    return file


def parse_cli_arguments(parser):
    """Parse command line arguments and return dictionary with configuration to be used"""
    args = vars(parser.parse_args())
    args["csvfile"] = file_error_checking(parser, args["filename"])
    if args["markdown"]:
        args["decorator"] = "|"
    if args["latex"]:
        args["decorator"] = "&"
    return args


def lstrip_cells_in_row(row):
    return [cell.lstrip() for cell in row]


def list_of_numbers_is_sorted_and_contains_unique_elements(numbers):
    return sorted(list(set(numbers))) == numbers


def store_content(parser, args):
    """Store content in file and extract relevant configurations to the dictionary"""
    csvreader = csv.reader(args["csvfile"], delimiter=args["separator"])
    header = next(csvreader)
    args["num_columns"] = len(header)
    args["content"] = [lstrip_cells_in_row(header)]
    row_number = 0
    for row_number, row in enumerate(islice(csvreader, args["rows"] - 1)):
        args["num_columns"] = max(len(row), args["num_columns"])
        args["content"].append(lstrip_cells_in_row(row))
    args["rows"] = row_number + 1
    align_all_columns_equally = len(args["align"]) == 1
    length_of_alignment_and_columns_differ = len(args["align"]) != args["num_columns"]
    if align_all_columns_equally:
        args["align"] = [args["align"][0]] * args["num_columns"]
    elif length_of_alignment_and_columns_differ:
        print_message_and_exit(
            parser, "argument -a/--align: only one argument or one per column"
        )
    if args["columns"] is None:
        args["columns"] = list(range(1, args["num_columns"] + 1))
    elif not all(0 < c <= args["num_columns"] for c in args["columns"]):
        print_message_and_exit(
            parser, "argument -c/--columns: column number out of range"
        )
    elif not list_of_numbers_is_sorted_and_contains_unique_elements(args["columns"]):
        print_message_and_exit(
            parser,
            "argument -c/--columns: column numbers must be unique and in ascending order",
        )
