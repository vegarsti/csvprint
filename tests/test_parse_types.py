import pytest
from csvprint import parse_types
import argparse


def test_alignment_left():
    assert parse_types.alignment("l") == "<"


def test_alignment_right():
    assert parse_types.alignment("r") == ">"


def test_alignment_incorrect_argument():
    with pytest.raises(argparse.ArgumentTypeError):
        parse_types.alignment("")


def test_separator_comma():
    assert parse_types.separator("tab") == "\t"


def test_separator_tab():
    assert parse_types.separator("comma") == ","


def test_separator_one_character():
    assert parse_types.separator(".") == "."


def test_separator_incorrect_argument():
    with pytest.raises(argparse.ArgumentTypeError):
        parse_types.separator("..")


def test_positive_integer():
    assert parse_types.positive_integer(1) == 1
    with pytest.raises(argparse.ArgumentTypeError):
        parse_types.positive_integer(0)
    with pytest.raises(argparse.ArgumentTypeError):
        parse_types.positive_integer(-1)


def test_non_negative_integer():
    assert parse_types.non_negative_integer(1) == 1
    assert parse_types.non_negative_integer(0) == 0
    with pytest.raises(argparse.ArgumentTypeError):
        parse_types.non_negative_integer(-1)
