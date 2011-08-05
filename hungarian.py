#!/usr/bin/python
# This file implements the hungarian maximization algorithm as described here: 
# http://csclab.murraystate.edu/bob.pilgrim/445/munkres.html
import sys
import re
import itertools
import random
import copy

# Brute force solution checker
# Only works on small grids
# used for testing my solution
def bruteForceMaximize(grid, debug=False):
    possible_column_indexes = itertools.permutations(range(len(grid)))
    max_sum = None
    max_positions = []
    for column_indexes in possible_column_indexes:
        current_sum = 0
        current_positions = []
        for row, col in enumerate(column_indexes):
            current_sum += grid[row][col]
            current_positions.append("(%d, %d)" % (row, col))
        if max_sum == None or current_sum > max_sum:
            max_sum = current_sum
            max_positions = current_positions

    if debug:
        for position in max_positions:
            print position
    return max_sum

def minOfRow(row, grid):
    return min(grid[row])

# Step 1
# For each row, find the min in that row, and subtract it from every cell in
# that row 
def subtractRowMinFromEachRow(grid):
    for r in range(len(grid)):
        min = minOfRow(r, grid)
        for c in range(len(grid[r])):
            grid[r][c] -= min

# Step 2
# For each uncovered zero in the grid, add a star to it and then cover that row and column.
# But then uncover all the rows and cols
def starZeros(grid, grid_info, row_info, col_info):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 0 and row_info[r]['covered'] == False and col_info[c]['covered'] == False:
                grid_info[r][c] = 1
                row_info[r]['covered'] = col_info[c]['covered'] = True

    uncoverAll(row_info, col_info)

# Step 3
# Cover all the columns with starred zeros, and return the number of covered columns
def coverColsWithStarredZeros(grid, grid_info, col_info):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid_info[r][c] == 1:
                # cover the column
                col_info[c]['covered'] = True

    covered_cnt = 0
    for c in range(len(col_info)):
        if col_info[c]['covered']:
            covered_cnt += 1

    return covered_cnt

# Return the column of a starred zero in the specified row, or -1
def isStarInRow(row, grid, grid_info):
    for c in range(len(grid[row])):
        if grid_info[row][c] == 1:
            return c

    return -1

# Return the row of a starred zero in the specified column, or -1
def isStarInCol(col, grid, grid_info):
    for r in range(len(grid)):
        if grid_info[r][col] == 1:
            return r

    return -1

# Find an uncovered zero, and return it's row and column (-1 returned if one is not present)
def findZero(grid, grid_info, row_info, col_info):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 0 and row_info[r]['covered'] == False and col_info[c]['covered'] == False:
                return r, c

    return -1, -1

# Step 4
# Keep finding non covered zeros, prime them, and see if there is a starred zero in that row (that you found the non covered zero in).
# If there is no starred zero in that row, return the row and column you just visited, otherwise mark the row as covered, and the column
# you saw the starred zero in as covered
def primeZeros(grid, grid_info, row_info, col_info):
    while True:
        r, c = findZero(grid, grid_info, row_info, col_info)
        if r == -1:
            return False

        grid_info[r][c] = 2
        col_of_star = isStarInRow(r, grid, grid_info)
        if col_of_star == -1:
            return {'row' : r, 'col' : c}

        row_info[r]['covered'] = True
        col_info[col_of_star]['covered'] = False

# Find the smallest number in the grid that is not covered
def findSmallestUncoveredValue(grid, grid_info, row_info, col_info):
    min_ = None
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if row_info[r]['covered'] == 0 and col_info[c]['covered'] == 0 and (min_ == None or grid[r][c] < min_):
                min_ = grid[r][c]

    return min_

# step 6
# For each number in the grid, if it's row is covered, add the min to its value. 
# If the column is not covered, then subtract the min for it
def applySmallestValue(grid, grid_info, row_info, col_info, min_):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if row_info[r]['covered']:
                grid[r][c] += min_
            if not col_info[c]['covered']:
                grid[r][c] -= min_


# Toggle the star in every point in the path
def augmentPath(grid, grid_info, path):
    for pair in path:
        r = pair['row']
        c = pair['col']
        if grid_info[r][c] == 1:
            grid_info[r][c] = 0
        else:
            grid_info[r][c] = 1

# Remove the prime from every primed item in the path
def unprimeAll(grid_info):
    for r in range(len(grid_info)):
        for c in range(len(grid_info[r])):
            if grid_info[r][c] == 2:
                grid_info[r][c] = 0

# Uncover all the rows and cols
def uncoverAll(row_info, col_info):
    for i in range(len(row_info)):
        row_info[i]['covered'] = False
    for i in range(len(col_info)):
        col_info[i]['covered'] = False


# Return the column of a primed zero in the specified row, or -1
def isPrimeInRow(row, grid, grid_info):
    for c in range(len(grid[row])):
        if grid_info[row][c] == 2:
            return c

    return -1

# Step 5
# I really don't want to explain this. I have no idea what its purpose is
def pathStuff(grid, grid_info, row_info, col_info, pair):
    path = []
    path.append(pair)
    done = False
    while not done:
        row = isStarInCol(path[-1]['col'], grid, grid_info)
        if row > -1:
            path.append({"row" : row, "col" : path[-1]['col']})
        else:
            done = True
        if not done:
            col = isPrimeInRow(path[-1]['row'], grid, grid_info)
            path.append({"row" : path[-1]['row'], "col" : col})

    augmentPath(grid, grid_info, path)
    unprimeAll(grid_info)
    uncoverAll(row_info, col_info)

def printGrid(grid, grid_info):
    for r in range(len(grid)):
        s = []
        for c in range(len(grid[r])):
            starred = True if grid_info[r][c] == 1 else False
            primed = True if grid_info[r][c] == 2 else False
            n = grid[r][c]
            if starred and primed:
                s.append("%4d*'" % (n))
            elif starred:
                s.append("%4d*" % (n))
            elif primed:
                s.append("%4d'" % (n))
            else:
                s.append("%4d" % (n))
        print ",".join(s)

# For every element in the grid, set grid[r][c] = max_value_of_grid - grid[r][c]
# This is the trick to turn hungarian minimization into maximization
def normalize(grid):
    max_ = grid[0][0]
    for row in grid:
        max_of_row = max(row)
        if max_of_row > max_:
            max_ = max_of_row

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            grid[r][c] = max_ - grid[r][c]
    return max_

# Transpose a grid
def transpose(grid):
    new_grid = []
    for c in range(len(grid[0])):
        new_grid.append([])
        for r in range(len(grid)):
            new_grid[c].append(grid[r][c])

    return new_grid

# The actual hungarian-munkres algorthim
# Returns a matrix where an item is set to 1 if that row, col is part of the extrema
def assign(working_copy):
    grid = working_copy

    row_info = []
    for r in range(len(grid)):
        row_info.append({"covered" : False})

    col_info = [] #[None]*len(working_copy[0])
    for c in range(len(grid[0])):
        col_info.append({"covered" : False})

    grid_info = []
    for r in range(len(grid)):
        grid_info.append([])
        for c in range(len(working_copy[r])):
            grid_info[r].append(0)
            
    # Step 1
    subtractRowMinFromEachRow(grid)
    # Step 2
    starZeros(grid, grid_info, row_info, col_info)
    cover = True
    while True:
        if cover:
            # step 3
            covered_cnt = coverColsWithStarredZeros(grid, grid_info, col_info)
            if covered_cnt >= min(len(grid), len(grid[0])):
                break
    
        # step 4
        pair = primeZeros(grid, grid_info, row_info, col_info)
        if pair:
            # step 5
            pathStuff(grid, grid_info, row_info, col_info, pair)
            # go to step 3
            cover = True
        else:
            # step 6
            n = findSmallestUncoveredValue(grid, grid_info, row_info, col_info)
            applySmallestValue(grid, grid_info, row_info, col_info, n)
            # goto step 4
            cover = False

    return grid_info

# Transpose the matrix (if it has more rows than cols)
# And, if the method is maximization, perform the subtraction rule (the normalization function)
def prepare(in_grid, method="max"):
    rows = len(in_grid)
    cols = len(in_grid[0])
    # The algo requires that the number of cols >= the number of rows
    if rows > cols:
        in_grid = transpose(in_grid)
    working_copy = copy.deepcopy(in_grid)

    # Make the adjustments for maximization 
    if method == "max":
        normalize(working_copy)

    return in_grid, working_copy

# sum up the starred items in the grid
def sum(grid, grid_info):
    sum = 0
    for r in range(len(grid_info)):
        for c in range(len(grid_info[r])):
            if grid_info[r][c] == 1:
                sum += grid[r][c]

    return sum

# Return a list of the tuples (row, column,) that correspond to the extrema points
def listPoints(grid_info):
    rows = len(grid_info)
    cols = len(grid_info[0])
    # If we transposed the grid earlier, transpose it again to get the proper coordinates
    if rows != cols:
        grid_info = transpose(grid_info)

    points = []
    for r in range(len(grid_info)):
        for c in range(len(grid_info[r])):
            if grid_info[r][c] == 1:
                points.append((r, c))

    return points

def solve(grid, method="min"):
    grid, working_copy = prepare(grid, method)
    grid_info = assign(working_copy)
    sum_ = sum(grid, grid_info)
    return sum_, listPoints(grid_info)


# convience methods
def minimize(in_grid):
    return solve(grid, "min") 

def maximize(grid):
    return solve(grid, "max") 
    
# Pass the name of a file, or two integers representing the number of tests to perform, and the size of the grid
if __name__ == '__main__':
    try:
        tests = int(sys.argv[1])
        size = int(sys.argv[2])
        for i in range(tests):
            grid = []
            for r in range(size):
                grid.append([])
                for c in range(size):
                    grid[r].append(random.randint(0, 20))

            r1 = maximize(grid)[0]
            r2 = bruteForceMaximize(grid)
            print r1, r2
            if r1 != r2:
                print "failed"
                exit(1)

    except ValueError:
        grid = open(sys.argv[1], 'r').read().strip()
        grid = [[float(x) for x in re.split("\s+", line)] for line in grid.split("\n")]
        r1 = maximize(grid)[0]
        r2 = bruteForceMaximize(grid)
        print r1, r2
