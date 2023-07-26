import pygame
from pygame.locals import *
from packman import PackMan
from constants import *

class GameController(object):
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
        self.__background = None
        self.__clock = pygame.time.Clock()

    def setBackground(self, background):
        self.__background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.__background.fill(Colors.BLACK)

    def startGame(self):
        self.setBackground(Colors.BLACK)
        self.__packman = PackMan()

    def update(self):
        delta_time = self.__clock.tick(30) / 1000.0 
        self.__packman.update(delta_time)
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

    def render(self):
        self.__screen.blit(self.__background, (0, 0))
        self.__packman.render(self.__screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()


