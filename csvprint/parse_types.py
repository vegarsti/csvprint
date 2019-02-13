import argparse


def alignment(direction):
    """Parse the direction, possibly raising error"""
    if direction == "l":
        return "<"
    elif direction == "r":
        return ">"
    else:
        raise argparse.ArgumentTypeError("must be l for left or r for right")


def separator(string):
    """Parse the separator, possibly raising error"""
    options = {"tab": "\t", "comma": ","}
    s = options.get(string, string)
    if len(s) == 1:
        return s
    else:
        raise argparse.ArgumentTypeError("must be a 1-character string")


def positive_integer(n):
    """Parse positive integer, possibly raising error"""
    message = "must be a positive integer"
    try:
        n = int(n)
    except ValueError:
        raise argparse.ArgumentTypeError(message)
    if n > 0:
        return n
    else:
        raise argparse.ArgumentTypeError(message)


def non_negative_integer(n):
    """Parse non-negative integer, possibly raising error"""
    message = "must be a non-negative integer"
    try:
        n = int(n)
    except ValueError:
        raise argparse.ArgumentTypeError(message)
    if n >= 0:
        return n
    else:
        raise argparse.ArgumentTypeError(message)


def decimal_number_formatting(arg):
    """On format [column_number]:[decimal_numbers]"""
    split = arg.split(":")
    if len(split) != 2:
        raise argparse.ArgumentTypeError(
            "must be on format [column_number]:[decimal_numbers]"
        )
    column, decimals = split
    try:
        column = int(column)
    except:
        raise argparse.ArgumentTypeError("column must be integer")
    if column < 1:
        raise argparse.ArgumentTypeError("column must be positive")
    try:
        decimals = int(decimals)
    except:
        raise argparse.ArgumentTypeError("decimals must be integer")
    if column < 0:
        raise argparse.ArgumentTypeError("decimals must be non-negative")
    return column, decimals
