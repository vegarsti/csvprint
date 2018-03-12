from csvprint import *
import sys
from test_cases import *
import pytest
import parser

@pytest.mark.parametrize("args, expected_output", [
    (['imdb.csv'], expected_normal_output),
    (['imdb.csv', '--markdown'], expected_markdown_output),
    (['imdb.csv', '--j', 'l'], expected_normal_output),
    (['imdb.csv', '--j', 'r'], expected_right_justified_output),
    (['example.tsv', '-s', '\\t'], expected_tab_output),
    (['imdb.csv', '--header'], expected_header_output)
])
def test_correct_features(args, expected_output):
    sys.argv = [sys.argv[0]]
    csvparser = parser.create()
    sys.argv += args
    args = parser.parse_cli_arguments(csvparser)
    parser.store_content(csvparser, args)
    output = get_output(args)
    assert output == expected_output