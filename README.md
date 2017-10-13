# `pycolumn`
A Python implementation of the [UNIX utility `column`](https://linux.die.net/man/1/column). Nothing fancy, just a way to quickly get a decent pretty printed version of csv files.

## Why?
I needed to quickly look at some csv files, but I didn't like the usability of the UNIX utility and how it printed the columns.

## Example

```
> pycolumn example.csv
  Widget name Size Price
      Trinket 1000    80
       Doodad   10     8
      Trunket  190  9000
```

## Installation

Add an alias for `python /path/to/pycolumn.py` to your shell config, e.g. `echo "alias pycolumn='python3 /path/to/pycolumn.py'" >> ~/.bash_profile`.

## Features
`pycolumn -h` prints a help message.

* `-s` flag to handle delimiters that are not commas
