# `csvprint`

## What?
Command-line utility for pretty printing csv files.

## Why?
I needed to quickly look at some csv files, but the [UNIX utility `column`](https://linux.die.net/man/1/column) didn't solve my problem.

## Example

```
> csvprint example.csv
Widget name Size Price
    Trinket 1000    80
     Doodad   10     8
    Trunket  190  9000
```

Compare to e.g.

```
> column -t -s ',' example.csv
Widget name  Size  Price
Trinket      1000  80
Doodad       10    8
Trunket      190   9000
```
Creating an alias for `column -t -s ','` could work, but I found it a a bit lacking, as it doesn't provide support for various justification or decoration.

## Installation

Clone the repo and add an alias for `python /path/to/csvprint/csvprint.py` to your shell config, e.g.

```
git clone https://github.com/vegarsti/csvprint.git ~/path/to/csvprint
echo "alias csvprint='python3 /path/to/csvprint/csvprint.py'" >> ~/.bash_profile`
```

## Features
`csvprint -h` prints a help message.

* `-s` to specify delimiter (default is comma)
* `-r` to specify number of rows to show (default is 1000)
* `-j` to specify which justification to choose (left or right)
* `-d` decorator to separate fields by (e.g. `' '`, which is default)