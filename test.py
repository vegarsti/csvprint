from csvprint import *
import sys
from test_cases import *
import pytest

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
    parser = create_parser()
    sys.argv += args
    args = parse_cli_arguments(parser)
    store_content(parser, args)
    output = get_output(args)
    assert output == expected_output