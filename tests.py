#!/usr/bin/python
import sys
import re
import itertools
import random
import hungarian

pass_cnt = 0
fail_cnt = 0
def stringToGrid(string):
    return [[float(x) for x in re.split("\s+", line.strip())] for line in grid.strip().split("\n")]

def testGrid(grid, expected_sum, method):
    global pass_cnt, fail_cnt
    result = hungarian.solve(grid, method)
    if result[0] != expected_sum:
        print "FAILURE on", method + ": Expected %f got %f" % (expected_sum, result[0])
        fail_cnt += 1
    else:
        print "Pass"
        pass_cnt += 1

# Simple case
grid = """
5 9 3 6
8 7 8 2
6 10 12 7 
3 10 8 6"""
grid = stringToGrid(grid)
testGrid(grid, 18.0, "min")
testGrid(grid, 36.0, "max")

# Requires more work
grid = """
11 7 10 17 10
13 21 7 11 13
13 13 15 13 14
18 10 13 16 14
12 8 16 19 10"""
grid = stringToGrid(grid)
testGrid(grid, 51.0, "min")
testGrid(grid, 86.0, "max")

# Hard (most other algos fail with this matrix)
grid = """
2 8 1 3
9 9 8 10
10 6 20 19
11 6 20 14"""
grid = stringToGrid(grid)
testGrid(grid, 27.0, "min")
testGrid(grid, 56.0, "max")

# cols > rows
# has mutliple solutions
grid = """
1 2 3
4 5 6"""
grid = stringToGrid(grid)
testGrid(grid, 6, "min")
testGrid(grid, 8, "max")

# rows > cols
# big matrix
grid = """
9   13.5    9   9   9   13.5    9   13.5    13.5    13.5    9   13.5    13.5    9   13.5
6   6   13.5    6   9   6   6   6   6   9   6   6   9   9   6
22.5    22.5    14  22.5    14  22.5    22.5    22.5    22.5    21  22.5    22.5    21  14  22.5
6   6   7   6   7   6   6   6   6   7   9   6   7   7   6
4.5 6.75    6   4.5 6   6.75    4.5 4.5 6.75    9   4.5 6.75    9   6   6.75
6   9   5   6   5   9   6   6   9   7.5 6   9   7.5 5   9
13.5    13.5    4   13.5    4   13.5    13.5    13.5    13.5    6   13.5    13.5    4   4   13.5
4.5 4.5 4   4.5 4   4.5 4.5 4.5 4.5 4   4.5 4.5 6   4   4.5
10.5    10.5    10  10.5    10  10.5    10.5    10.5    10.5    10  10.5    10.5    10  10  10.5
11.25   11.25   3   11.25   3   11.25   11.25   11.25   11.25   3   11.25   11.25   3   3   11.25
7.5 11.25   10  7.5 10  11.25   7.5 11.25   11.25   15  7.5 11.25   15  10  11.25
7.5 7.5 12  7.5 8   7.5 7.5 7.5 7.5 8   7.5 7.5 8   8   7.5
13.5    13.5    6   13.5    6   13.5    13.5    13.5    13.5    9   13.5    13.5    9   6   13.5
9   9   8   9   8   9   9   9   9   12  9   9   12  8   9
7.5 7.5 12  7.5 8   7.5 7.5 7.5 7.5 8   7.5 7.5 8   8   7.5
18  18  10  18  10  18  18  18  18  15  18  18  15  10  18"""
grid = stringToGrid(grid)
testGrid(grid, 100.0, "min")
testGrid(grid, 184.0, "max")

if fail_cnt == 0:
    print "COMPLETE PASS"
else:
    print "%d failures" % (fail_cnt)
    exit(1)
