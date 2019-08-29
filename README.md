# `csvprint`

[![Build Status](https://travis-ci.org/vegarsti/csvprint.svg?branch=master)](https://travis-ci.org/travis-ci/travis-web)
[![codecov](https://codecov.io/gh/vegarsti/csvprint/branch/master/graph/badge.svg)](https://codecov.io/gh/vegarsti/csvprint)

A command-line utility for pretty printing csv files and converting to other formats.

## Installation

If Python 3 with the package manager pip is installed, doing `pip3 install csvprint` in your terminal should do the trick.

## Development installation

With [pipenv](https://github.com/pypa/pipenv) installed.

1. Clone this repo
2. Do `pipenv install`
3. `pipenv shell`
4. `pip install -e .`

## Usage

`csvprint [filename]` prints a formatted table if `filename` is a comma separated file.

```
» cat imdb.csv
Title,Release Year,Estimated Budget
Shawshank Redemption,1994,$25 000 000
The Godfather,1972,$6 000 000
The Godfather: Part II,1974,$13 000 000
The Dark Knight,2008,$185 000 000
12 Angry Men,1957,$350 000

» csvprint imdb.csv
Title                  Release Year Estimated Budget
Shawshank Redemption   1994         $25 000 000
The Godfather          1972         $6 000 000
The Godfather: Part II 1974         $13 000 000
The Dark Knight        2008         $185 000 000
12 Angry Men           1957         $350 000
```
You can also pipe into `csvprint`:

```
» cat imdb.csv | csvprint
Title                  Release Year Estimated Budget
Shawshank Redemption   1994         $25 000 000
The Godfather          1972         $6 000 000
The Godfather: Part II 1974         $13 000 000
The Dark Knight        2008         $185 000 000
12 Angry Men           1957         $350 000
```

## Options

Command        | Result
:--------------|:-------------------------------------------------------------
`-a`           | specify alignment (left or right) - see examples below
`-c`           | specify which columns to print 
`-h`           | print help message
`--markdown`   | print as markdown
`--latex`      | print as latex table
`--numeric [c1:d1] [c2:d2] ...`   | specify decimal numbers for chosen numeric columns (`c` for column, `d` for digits)
`--header`     | add header decoration around the first line
`-s 'char'`    | file is delimited by `char` (instead of comma), `tab` for tab
`-p [n]`       | add a padding of `n` spaces for each column, on both sides
`-d [string]`  | specify the string to separate columns

## Alignment example

There are three options for specifying alignment. One can use `l` or `r` for aligning all cells to the left or right, respectively. One can also specify a distinct alignment option for each column. Then the number of options will need to match the number of columns.

```
» csvprint imdb.csv -a l r r
Title                  Release Year Estimated Budget
Shawshank Redemption           1994      $25 000 000
The Godfather                  1972       $6 000 000
The Godfather: Part II         1974      $13 000 000
The Dark Knight                2008     $185 000 000
12 Angry Men                   1957         $350 000
```

## Markdown example

Markdown output also supports left and right alignment.

```
» csvprint examples/imdb.csv --markdown -a l r r
Title                  | Release Year | Estimated Budget
:----------------------|-------------:|----------------:
Shawshank Redemption   |         1994 |      $25 000 000
The Godfather          |         1972 |       $6 000 000
The Godfather: Part II |         1974 |      $13 000 000
The Dark Knight        |         2008 |     $185 000 000
12 Angry Men           |         1957 |         $350 000
```

When rendered as HTML, this looks like

Title                  | Release Year | Estimated Budget
:----------------------|-------------:|----------------:
Shawshank Redemption   |         1994 |      $25 000 000
The Godfather          |         1972 |       $6 000 000
The Godfather: Part II |         1974 |      $13 000 000
The Dark Knight        |         2008 |     $185 000 000
12 Angry Men           |         1957 |         $350 000

## Numeric example

```
» csvprint examples/numeric.csv
measure1  measure2
1.2323    9000
1.299     9000001

» csvprint examples/numeric.csv --numeric 1:1 2:1
measure1  measure2
1.2       9000.0
1.3       9000001.0
```

## Testing

Run `pytest` while in the root directory of this repository.
