#!/usr/bin/env python3

import sys
import parser

def main():
    csvparser = parser.create()
    args = parser.parse_cli_arguments(csvparser)
    parser.store_content(csvparser, args)
    reading_from_csvfile = not args['csvfile'] == sys.stdin
    if reading_from_csvfile:
        args['csvfile'].close()
    content = parser.run_pipeline(args)
    print(content)

if __name__ == '__main__':
    main()