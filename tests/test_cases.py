expected_normal_output = """Title                   Release Year  Estimated Budget
Shawshank Redemption    1994          $25 000 000
The Godfather           1972          $6 000 000
The Godfather: Part II  1974          $13 000 000
The Dark Knight         2008          $185 000 000
12 Angry Men            1957          $350 000"""

expected_markdown_output = """Title                  | Release Year | Estimated Budget
:----------------------|:-------------|:----------------
Shawshank Redemption   | 1994         | $25 000 000
The Godfather          | 1972         | $6 000 000
The Godfather: Part II | 1974         | $13 000 000
The Dark Knight        | 2008         | $185 000 000
12 Angry Men           | 1957         | $350 000"""

expected_right_justified_output = """                 Title  Release Year  Estimated Budget
  Shawshank Redemption          1994       $25 000 000
         The Godfather          1972        $6 000 000
The Godfather: Part II          1974       $13 000 000
       The Dark Knight          2008      $185 000 000
          12 Angry Men          1957          $350 000"""

expected_tab_output = """Some parameter  Other parameter  Last parameter
CONST           123456           12.45"""

expected_header_output = """------------------------------------------------------
Title                   Release Year  Estimated Budget
------------------------------------------------------
Shawshank Redemption    1994          $25 000 000
The Godfather           1972          $6 000 000
The Godfather: Part II  1974          $13 000 000
The Dark Knight         2008          $185 000 000
12 Angry Men            1957          $350 000"""

expected_short_output = """Title                 Release Year  Estimated Budget
Shawshank Redemption  1994          $25 000 000
The Godfather         1972          $6 000 000"""

expected_oneline_output = """Title  Release Year  Estimated Budget"""

expected_justified_markdown_output = """Title                  | Release Year | Estimated Budget
:----------------------|-------------:|----------------:
Shawshank Redemption   |         1994 |      $25 000 000
The Godfather          |         1972 |       $6 000 000
The Godfather: Part II |         1974 |      $13 000 000
The Dark Knight        |         2008 |     $185 000 000
12 Angry Men           |         1957 |         $350 000"""

expected_header_with_decorator_output = """----------------------- o -------------- o -----------------
Title                   o  Release Year  o  Estimated Budget
----------------------- o -------------- o -----------------
Shawshank Redemption    o  1994          o  $25 000 000
The Godfather           o  1972          o  $6 000 000
The Godfather: Part II  o  1974          o  $13 000 000
The Dark Knight         o  2008          o  $185 000 000
12 Angry Men            o  1957          o  $350 000"""


NORMAL_FILENAME = 'examples/imdb.csv'

normal = [NORMAL_FILENAME], expected_normal_output
markdown = [NORMAL_FILENAME, '--markdown'], expected_markdown_output
left = [NORMAL_FILENAME, '--j', 'l'], expected_normal_output
right = [NORMAL_FILENAME, '--j', 'r'], expected_right_justified_output
tab = ['examples/small.tsv', '-s', 'tab'], expected_tab_output
comma = [NORMAL_FILENAME, '-s', 'comma'], expected_normal_output
header =[NORMAL_FILENAME, '--header'], expected_header_output
short = [NORMAL_FILENAME, '-n', '3'], expected_short_output
oneline = [NORMAL_FILENAME, '-n', '1'], expected_oneline_output
justified_markdown = [NORMAL_FILENAME, '--markdown', '-j', 'l', 'r', 'r'], expected_justified_markdown_output
header_with_decorator = [NORMAL_FILENAME, '--header', '-d', ' o '], expected_header_with_decorator_output