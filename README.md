# `pycolumn`
A Python implementation of something akin to the [UNIX utility `column`](https://linux.die.net/man/1/column). Nothing fancy, just a way to quickly get a decent pretty printed version of csv files.

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

Compare to

```
column -t -s ',' example.csv
Widget name  Size  Price
Trinket      1000  80
Doodad       10    8
Trunket      190   9000
```
Creating an alias for `column -t -s ','` could work, but I don't like how it left-justifies cells.

## Installation

Clone the repo and add an alias for `python /path/to/pycolumn.py` to your shell config, e.g.

```
git clone https://github.com/vegarsti/pycolumn.git ~/path/to/
echo "alias pycolumn='python3 /path/to/pycolumn.py'" >> ~/.bash_profile`
```

## Features
`pycolumn -h` prints a help message.

* `-s` to specify delimiter (default is comma)
* `-r` to specify number of rows to show (default is 1000)
* `-j` to specify which justification to choose (left or right)
* `-d` decorator to separate fields by (e.g. ' ')