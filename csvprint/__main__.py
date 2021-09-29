#!/usr/bin/env python3

import sys
from csvprint import parser
from csvprint import printer


def main():
    csvparser = parser.create()
    args = parser.parse_cli_arguments(csvparser)
    parser.store_content(csvparser, args)
    reading_from_csvfile = not args["csvfile"] == sys.stdin
    if reading_from_csvfile:
        args["csvfile"].close()
    output = printer.run_pipeline(args)
    print(output)


if __name__ == "__main__":
    main()
