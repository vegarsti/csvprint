import argparse

def justification(direction):
    if direction == 'l':
        return '<'
    elif direction == 'r':
        return '>'
    else:
        raise argparse.ArgumentTypeError('must be l for left or r for right')

def separator(string):
    options = {
        'tab': '\t',
        'comma': ','
    }
    s = options.get(string, string)
    if len(s) == 1:
        return s
    else:
        raise argparse.ArgumentTypeError(
            'must be a 1-character string'
        )

def positive_integer(n):
    message = 'must be a positive integer'
    try:
        n = int(n)
    except ValueError:
        raise argparse.ArgumentTypeError(message)
    if n > 0:
        return n
    else:
        raise argparse.ArgumentTypeError(message)

def non_negative_integer(n):
    message = 'must be a non-negative integer'
    try:
        n = int(n)
    except ValueError:
        raise argparse.ArgumentTypeError(message)
    if n >= 0:
        return n
    else:
        raise argparse.ArgumentTypeError(message)