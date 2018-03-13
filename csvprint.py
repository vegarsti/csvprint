#!/usr/bin/env python3

import sys
import parser
import utils

def main():
    csvparser = parser.create()
    args = parser.parse_cli_arguments(csvparser)
    parser.store_content(csvparser, args)
    output = utils.get_output(args)
    reading_from_csvfile = not args['csvfile'] == sys.stdin
    if reading_from_csvfile:
        args['csvfile'].close()
    print(output)

if __name__ == '__main__':
    main()