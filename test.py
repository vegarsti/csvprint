from csvprint import *
import sys
from test_cases import *
import pytest
import parser

@pytest.mark.parametrize("args, expected_output", [
    normal,
    markdown,
    left,
    right,
    tab,
    header,
    short,
    oneline,
    justified_markdown,
])
def test_correct_features(args, expected_output):
    sys.argv = [sys.argv[0]]
    csvparser = parser.create()
    sys.argv += args
    args = parser.parse_cli_arguments(csvparser)
    parser.store_content(csvparser, args)
    output = get_output(args)
    print(expected_output)
    assert output == expected_output