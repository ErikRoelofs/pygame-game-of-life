import pygame
from pygame.locals import *
import random
import sys
import copy

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

GRID_WIDTH = 120
GRID_HEIGHT = 120

generation = 0
grid = []

def randomValue():
    if random.randint(0,3) == 0:
        return 1
    return 0

for i in range(0, GRID_HEIGHT):
    row = [0] * GRID_WIDTH
    for j in range(0, GRID_WIDTH):
        row[j] = randomValue()
    grid.append(row)

swapGrid = []
for i in range(0, GRID_HEIGHT):
    row = [0] * GRID_WIDTH
    for j in range(0, GRID_WIDTH):
        row[j] = 0
    swapGrid.append(row)



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

def nextGrid():
    global grid, swapGrid, generation
    for colNum, row in enumerate(grid):
        for rowNum, cell in enumerate(row):
            neighbours = countAliveNeighbours(grid, colNum, rowNum)
            alive = findCell(grid, colNum, rowNum)
            swapGrid[colNum][rowNum] = decideNewValue(alive, neighbours)
    grid = copy.deepcopy(swapGrid)
    generation+=1

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
    frames = 0
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
        drawFPS(clock.get_fps())
        drawGeneration()

        pygame.display.update()
        timer = clock.tick(60)

        nextGrid()

def drawGeneration():
    textSurfaceObj = fontObj.render('gen: ' + str(generation), True, (255,0,0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.left = 0
    textRectObj.bottom = SCREEN_HEIGHT
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def drawFPS(fps):
    textSurfaceObj = fontObj.render(str(int(fps)) + ' fps', True, (255,0,0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.right = SCREEN_WIDTH
    textRectObj.bottom = SCREEN_HEIGHT
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


if __name__ == '__main__':
    main()
