import pygame
from pygame.locals import *
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

GRID_WIDTH = 120
GRID_HEIGHT = 120

grid = []

def randomValue():
    if random.randint(0,3) == 0:
        return 1
    return 0

for i in range(0, GRID_HEIGHT):
    row = []
    for j in range(0, GRID_WIDTH):
        row.append(randomValue())
    grid.append(tuple(row))

grid = tuple(grid)


COLOR_ALIVE = (255,255,255)
COLOR_DEAD = (100,100,100)

CELL_WIDTH = 5
CELL_HEIGHT = 5

def drawGrid(surface, grid):
    for colnum, col in enumerate(grid):
        for rownum, cell in enumerate(col):
            drawCell(surface, cell, rownum, colnum)

def drawCell(surface, cell, row, col):
    pygame.draw.rect(surface, COLOR_ALIVE if cell else COLOR_DEAD, (row * CELL_WIDTH, col * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

def findCell(grid, col, row):
    if not (0 <= col < GRID_HEIGHT):
        return 0
    if not (0 <= row < GRID_WIDTH):
        return 0
    return grid[col][row]

def countAliveNeighbours(grid, col, row):
    return  findCell(grid, col-1,row-1) + findCell(grid, col-1,row) + findCell(grid, col-1,row+1) +\
            findCell(grid, col,row-1) + findCell(grid, col,row+1) +\
            findCell(grid, col + 1, row - 1) + findCell(grid, col + 1, row) + findCell(grid, col + 1, row + 1)

def nextGrid(grid):
    newGrid = []
    for colNum, row in enumerate(grid):
        newRow = []
        for rowNum, cell in enumerate(grid):
            neighbours = countAliveNeighbours(grid, colNum, rowNum)
            alive = findCell(grid, colNum, rowNum)
            newRow.append(decideNewValue(alive, neighbours))
        newGrid.append(tuple(newRow))
    return tuple(newGrid)

def decideNewValue(alive, neighbours):
    if neighbours == 3:
        return 1
    if neighbours == 2 and alive:
        return 1
    return 0

def main():
    global DISPLAYSURF, fontObj, grid
    clock = pygame.time.Clock()

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('GoL.')

    # setup vars
    mousex = 0
    mousey = 0

    # make font
    fontObj = pygame.font.Font('freesansbold.ttf', 16)

    # main loop
    while True:

        mouseClicked = False
        for someEvent in pygame.event.get():
            if someEvent.type == QUIT:
                pygame.quit()
                sys.exit()
            if someEvent.type == MOUSEMOTION:
                mousex, mousey = someEvent.pos
            if someEvent.type == MOUSEBUTTONUP:
                mousex, mousey = someEvent.pos
                mouseClicked = True


        drawGrid(DISPLAYSURF, grid)
        pygame.display.update()
        timer = clock.tick(60)
        if timer > 100:
            timer -= 100
            grid = nextGrid(grid)


if __name__ == '__main__':
    main()
