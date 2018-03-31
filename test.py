import sys
import test_cases
import pytest
import parser
import printer

@pytest.mark.parametrize("args, expected_output", [
    test_cases.normal,
    test_cases.markdown,
    test_cases.left,
    test_cases.right,
    test_cases.tab,
    test_cases.comma,
    test_cases.header,
    test_cases.short,
    test_cases.oneline,
    test_cases.justified_markdown,
])
def test_correct_features(args, expected_output):
    sys.argv = [sys.argv[0]]
    csvparser = parser.create()
    sys.argv += args
    args = parser.parse_cli_arguments(csvparser)
    parser.store_content(csvparser, args)
    output = printer.run_pipeline(args)
    assert output == expected_output