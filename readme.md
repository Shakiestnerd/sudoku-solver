# Sudoku Solver

OK, there are probably a million sudoku solver's out there. Much of the original code is not mine. I picked it up somewhere, but am not sure where. Otherwise, I would give credit where credit is due.

My contribution to this little project is the ability to read in an .SDK file.

The details for the file format can be found on [sudocue.net](https://sudocue.net/fileformats.php). It is the Sudoku Puzzle(.sdk) version that allows comments in the puzzle file.

This program ignores any lines in the file that begin with a '**#**'.

```bash
# Usage:
#  python3 sudoku.py [filename]

-> python3 sudoku.py 81.sdk
```
