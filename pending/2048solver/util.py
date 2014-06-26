#!/usr/bin/python
import numpy as np


def makeGrid(tuples, n=4):
    """
    Given a list of tuples defining a grid,
    put them in a 2d dictionary
    """
    grid = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0)
        grid.append(row)

    for t in tuples:
        tl = map(int, t)
        grid[tl[2]-1][tl[1]-1] = int(t[0])
        
    return grid



def canMoveRight(grid):
    # can move right if
    #   - there is space anywhere
    #   - there exists a tile which has another tile with
    #     the same number in that direction

    # if there exists a tile with a space to the right
    # failing this, there exists a tile with a similar neighbor to it's right

    n = len(grid)
    
    for r in range(n):
        for c in range(n-1):
            curr = grid[r][c]
            right = grid[r][c+1]
            
            if curr == 0: continue
            if right == 0 or curr == right:
                return True
    return False
    
    
def canMoveDir(dr, grid):
    """
    Question is: is there a valid move to the right?
    If I press "right" will it change anything on the board?
    """
    grid = np.array(grid)
    
    if dr == "right":
        # no need to rotate.
        print grid
        pass
    elif dr == "up":
        # rotate 3 times
        grid = np.rot90(grid, 3)
    elif dr == "left":
        # rotate 2 times
        grid = np.rot90(grid, 2)
    elif dr == "down":
        #rotate once
        grid = np.rot90(grid)

    grid = grid.tolist()
        
    return canMoveRight(grid)    



if __name__ == "__main__":
    tuples = [("4", "1", "4"), ("2", "2", "4"), ("4", "3", "4"), ("2", "4", "4")]
    grid = makeGrid(tuples)
    print grid

    print canMoveDir("up", grid)
    print canMoveDir("down", grid)
    print canMoveDir("left", grid)
    print canMoveDir("right", grid)
