import sys
import test_cases
import pytest
from csvprint import parser
from csvprint import printer

@pytest.mark.parametrize("args, expected_output", test_cases.test_cases)
def test_correct_features(args, expected_output):
    sys.argv = [sys.argv[0]]
    csvparser = parser.create()
    sys.argv += args
    args = parser.parse_cli_arguments(csvparser)
    parser.store_content(csvparser, args)
    output = printer.run_pipeline(args)
    assert output == expected_output