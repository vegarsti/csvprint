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
