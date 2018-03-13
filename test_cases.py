expected_normal_output ="""Title                  Release Year Estimated Budget
Shawshank Redemption   1994         $25 000 000     
The Godfather          1972         $6 000 000      
The Godfather: Part II 1974         $13 000 000     
The Dark Knight        2008         $185 000 000    
12 Angry Men           1957         $350 000        """

expected_markdown_output = """Title                  | Release Year | Estimated Budget
-----------------------|--------------|-----------------
Shawshank Redemption   | 1994         | $25 000 000     
The Godfather          | 1972         | $6 000 000      
The Godfather: Part II | 1974         | $13 000 000     
The Dark Knight        | 2008         | $185 000 000    
12 Angry Men           | 1957         | $350 000        """

expected_right_justified_output = """                 Title Release Year Estimated Budget
  Shawshank Redemption         1994      $25 000 000
         The Godfather         1972       $6 000 000
The Godfather: Part II         1974      $13 000 000
       The Dark Knight         2008     $185 000 000
          12 Angry Men         1957         $350 000"""

expected_tab_output = """Some parameter Other parameter Last parameter
CONST          123456          12.45         """

expected_header_output ="""----------------------------------------------------
Title                  Release Year Estimated Budget
----------------------------------------------------
Shawshank Redemption   1994         $25 000 000     
The Godfather          1972         $6 000 000      
The Godfather: Part II 1974         $13 000 000     
The Dark Knight        2008         $185 000 000    
12 Angry Men           1957         $350 000        """

expected_short_output ="""Title                Release Year Estimated Budget
Shawshank Redemption 1994         $25 000 000     
The Godfather        1972         $6 000 000      """

expected_oneline_output ="""Title Release Year Estimated Budget"""

expected_justified_markdown_output = """Title                  | Release Year | Estimated Budget
-----------------------|-------------:|----------------:
Shawshank Redemption   |         1994 |      $25 000 000
The Godfather          |         1972 |       $6 000 000
The Godfather: Part II |         1974 |      $13 000 000
The Dark Knight        |         2008 |     $185 000 000
12 Angry Men           |         1957 |         $350 000"""


normal = ['imdb.csv'], expected_normal_output
markdown = ['imdb.csv', '--markdown'], expected_markdown_output
left = ['imdb.csv', '--j', 'l'], expected_normal_output
right = ['imdb.csv', '--j', 'r'], expected_right_justified_output
tab = ['example.tsv', '-s', 'tab'], expected_tab_output
header =['imdb.csv', '--header'], expected_header_output
short = ['imdb.csv', '-n', '3'], expected_short_output
oneline = ['imdb.csv', '-n', '1'], expected_oneline_output
justified_markdown = ['imdb.csv', '--markdown', '-j', 'l', 'r', 'r'],expected_justified_markdown_output