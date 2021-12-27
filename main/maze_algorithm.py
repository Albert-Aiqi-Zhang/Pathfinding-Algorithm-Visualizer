import pygame
import sys
import random

LOW_POSSIBILITY = 0.1
MAZE_POSSIBILITY = 0.25 # P(create_maze) = 0.25
MIDDLE_POSSIBILITY = 0.65
SKEWED_POSSIBILITY = 0.75 # P(create_maze) = 0.75
HIGH_POSSIBILITY = 0.8

INTERVAL = 2

def create_random_maze(draw, grid):
    numRows, numCols = len(grid), len(grid[0])
    clear_barrier(grid)

    for row in grid:
        for spot in row:
            doesCreateMaze = random.random() < MAZE_POSSIBILITY
            if doesCreateMaze and not spot.is_start() and not spot.is_end():
                spot.make_barrier()
        draw()

def create_vertical_skewed_maze(draw, grid):
    numRows, numCols = len(grid), len(grid[0])
    clear_barrier(grid)
    # doesMakeLast = False # track the last element
    # doesCreateMaze = False
    for rowIdx, row in enumerate(grid):
        for colIdx, spot in enumerate(row):
            if spot.is_start() or spot.is_end():
                continue
            if rowIdx in (0, numRows - 1) or colIdx in (0, numCols - 1): # create maze in the outer bound
                spot.make_barrier()
                continue
            elif rowIdx == numRows // 2 or colIdx in [numCols // 10 * i for i in range(10)]:
                doesCreateMaze = random.random() < SKEWED_POSSIBILITY
            else:
                doesCreateMaze = random.random() < LOW_POSSIBILITY 
            if doesCreateMaze:
                spot.make_barrier()
        draw()

def create_horizontal_skewed_maze(draw, grid):
    numRows, numCols = len(grid), len(grid[0])
    clear_barrier(grid)
    # doesMakeLast = False # track the last element
    # doesCreateMaze = False
    for rowIdx, row in enumerate(grid):
        for colIdx, spot in enumerate(row):
            if spot.is_start() or spot.is_end():
                continue
            if rowIdx in (0, numRows - 1) or colIdx in (0, numCols - 1): # create maze in the outer bound
                spot.make_barrier()
                continue
            elif rowIdx in [numRows // 10 * i for i in range(9)]:
                doesCreateMaze = random.random() < MIDDLE_POSSIBILITY
            else:
                doesCreateMaze = random.random() < LOW_POSSIBILITY 
            if doesCreateMaze:
                spot.make_barrier()
            draw()
            # doesMakeLast = doesCreateMaze

def create_recursive_skewed_maze(draw, grid, orientation):
    ### orientation = "horizontal" or "vertical"
    numRows, numCols = len(grid), len(grid[0])
    clear_barrier(grid)
    create_recursive_skewed_maze_helper(draw, grid, 0, numRows - 1, 0, numCols - 1, orientation, False)

def create_recursive_skewed_maze_helper(draw, grid, rowStart, rowEnd, colStart, colEnd, orientation, isSurrounded):
    if rowEnd < rowStart or colEnd < colStart:
        return
    if not isSurrounded:
        for rowIdx, row in enumerate(grid):
            for colIdx, spot in enumerate(row):
                if spot.is_start() or spot.is_end():
                    continue
                if rowIdx in (0, len(grid) - 1) or colIdx in (0, len(grid[0]) - 1): # create maze in the outer bound
                    spot.make_barrier() 
            draw()
        isSurrounded = True

    if orientation == "horizontal":
        possible_rows = [i for i in range(rowStart, rowEnd + 2, INTERVAL)]
        possible_cols = [i for i in range(colStart - 1, colEnd + 3, INTERVAL)]
        random_row = possible_rows[int(random.random() * len(possible_rows))]
        random_col = possible_cols[int(random.random() * len(possible_cols))]
        rowIdx = random_row

        for colIdx in range(colStart - 1, colEnd + 2):
            if inBound(grid, rowIdx, colIdx):
                spot = grid[rowIdx][colIdx]
                if spot.is_start() or spot.is_end() or spot.is_barrier():
                    continue
                if colIdx != random_col and rowIdx != len(grid) - 2 and random.random() < HIGH_POSSIBILITY:
                    spot.make_barrier()
            draw()

        if random_row - INTERVAL - rowStart > colEnd - colStart:
            create_recursive_skewed_maze_helper(draw, grid, rowStart, random_row - INTERVAL, colStart, colEnd, orientation, isSurrounded)
        else:
            create_recursive_skewed_maze_helper(draw, grid, rowStart, random_row - INTERVAL, colStart, colEnd, "vertical", isSurrounded)
        if rowEnd - (random_row + INTERVAL) > colEnd - colStart:
            create_recursive_skewed_maze_helper(draw, grid, random_row + INTERVAL, rowEnd, colStart, colEnd, orientation, isSurrounded)
        else:
            create_recursive_skewed_maze_helper(draw, grid, random_row + INTERVAL, rowEnd, colStart, colEnd, "vertical", isSurrounded)

    else: # "vertical"
        possible_rows = [i for i in range(rowStart - 1, rowEnd + 3, INTERVAL)]
        possible_cols = [i for i in range(colStart, colEnd + 2, INTERVAL)]
        random_row = possible_rows[int(random.random() * len(possible_rows))]
        random_col = possible_cols[int(random.random() * len(possible_cols))]
        colIdx = random_col

        for rowIdx in range(rowStart - 1, rowEnd + 2):
            if inBound(grid, rowIdx, colIdx):
                spot = grid[rowIdx][colIdx]
                if spot.is_start() or spot.is_end() or spot.is_barrier():
                    continue
                if rowIdx != random_row and random.random() < HIGH_POSSIBILITY:
                    spot.make_barrier()
            draw()

        if rowEnd - rowStart > random_col - INTERVAL - colStart:
            create_recursive_skewed_maze_helper(draw, grid, rowStart, rowEnd, colStart, random_col - INTERVAL, "horizontal", isSurrounded)
        else:
            create_recursive_skewed_maze_helper(draw, grid, rowStart, rowEnd, colStart, random_col - INTERVAL, orientation, isSurrounded)
        if rowEnd - rowStart > colEnd - (random_col + INTERVAL):
            create_recursive_skewed_maze_helper(draw, grid, rowStart, rowEnd, random_col + INTERVAL, colEnd, "horizontal", isSurrounded)
        else:
            create_recursive_skewed_maze_helper(draw, grid, rowStart, rowEnd, random_col + INTERVAL, colEnd, orientation, isSurrounded)

def clear_barrier(grid):
    for row in grid:
        for spot in row:
            spot.reset_value()
            if not spot.is_start() and not spot.is_end():
                spot.reset()

def inBound(grid, i, j):
    numRows = len(grid)
    numCols = len(grid[0])
    return 0 <= i < numRows and 0 <= j < numCols
