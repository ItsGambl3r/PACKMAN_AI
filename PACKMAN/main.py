import pygame
from constants import * # import all constants from constants.py


# 0: Wall (blue), 1: Empty (black), 2, Pellet (white)
gameBoard = [ # 20 x 11 grid
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 0, 0, 2, 2, 2, 0, 2, 0, 0, 2, 2, 2, 0, 2, 2, 0, 0, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0],
    [0, 2, 0, 0, 2, 2, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
pygame.init()
width = 64 * 21
height = 64 * 12
screen = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(Colors.BLACK)
    x = 0
    y = 0
    increment = width / 10
    for row in gameBoard: # lets us range(len(gameBoard) - 1) and row = gameBoard[i]
        for col in row:
            if col == 0:
                pygame.draw.rect(screen, Colors.BLUE, [x, y, 64, 64])
            elif col == 1:
                pygame.draw.rect(screen, Colors.BLACK, [x, y, 64, 64])
            elif col == 2:
                pygame.draw.circle(screen, Colors.WHITE, [x + 32, y + 32], 4)
            x += 64
        y += 64
        x = 0
    pygame.display.flip()
    clock.tick(60)
pygame.quit()


