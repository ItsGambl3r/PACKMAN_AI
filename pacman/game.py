import pygame
import random
import os
from constants import *
from tiles import TileCollection
from pacman import Pacman
from text import Score
from pellets import PowerPellet
from ghost import Blinky, Pinky, Inky, Clyde

class GameController(object):
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_caption("Pacman")
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

    def setBackground(self):
        self.background = pygame.Surface(SCREEN_SIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.score = Score(0, (SCREEN_SIZE[0] // 2, 50))
        self.tileCollection = TileCollection(os.path.join("pacman", "Assets", "Levels", "level1.txt"))
        self.tileCollection.lookup_table[(24, 408)].portal = self.tileCollection.lookup_table[(672, 408)]
        self.tileCollection.lookup_table[(672, 408)].portal = self.tileCollection.lookup_table[(24, 408)]
        self.pacman = Pacman(self.tileCollection.lookup_table[(360, 624)]) # Pacman starts at 31B
        self.blinky = Blinky(self.tileCollection.lookup_table[(408, 384)])
        self.blinky = Blinky(self.tileCollection.lookup_table[(408, 384)])
        self.pinky = Pinky(self.tileCollection.lookup_table[(288, 384)])
        self.inky = Inky(self.tileCollection.lookup_table[(408, 432)])
        self.clyde = Clyde(self.tileCollection.lookup_table[(288, 432)])

    def update(self):
        deltaTime = self.clock.tick(30) / 1000.0
        self.pacman.update(deltaTime)
        self.blinky.update(deltaTime, self.pacman, self.tileCollection.lookup_table)
        self.pinky.update(deltaTime, self.pacman, self.tileCollection.lookup_table)
        self.inky.update(deltaTime, self.pacman, self.tileCollection.lookup_table)
        self.clyde.update(deltaTime, self.pacman, self.tileCollection.lookup_table)
        self.handleItemCollisions(self.pacman)
        self.handleGhostCollisions(self.pacman)
        self.ghostHandler(deltaTime, self.tileCollection.lookup_table)
        self.updateFlashingPowerPellets(deltaTime)
        self.checkEvents()
        self.render()


    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.tileCollection.render(self.screen)
        self.pacman.render(self.screen)
        self.blinky.render(self.screen)
        self.pinky.render(self.screen)
        self.inky.render(self.screen)
        self.clyde.render(self.screen)
        self.score.render(self.screen)
        pygame.display.update()

    def ghostHandler(self, dt, lookup_table):
        for ghost in [self.blinky, self.pinky, self.inky, self.clyde]:
            if ghost.mode == 'chase':
                ghost.timer += dt
                if ghost.timer >= ghost.chase_timer_max:
                    ghost.timer -= ghost.chase_timer_max
                    ghost.mode = 'scatter'

            elif ghost.mode == 'scatter':
                ghost.timer += dt
                if ghost.timer >= ghost.scatter_timer_max:
                    ghost.timer -= ghost.scatter_timer_max
                    ghost.mode = 'chase'

            elif ghost.mode == 'frightened':
                ghost.timer += dt
                if ghost.timer >= ghost.frightened_timer_max:
                    ghost.timer -= ghost.frightened_timer_max
                    ghost.mode = 'chase'
                    ghost.speed = 100

            elif ghost.mode == 'eaten':
                if ghost.tile.tile_item is None:
                    ghost.timer += dt
                    if ghost.timer >= ghost.eaten_timer_max:
                        ghost.timer -= ghost.eaten_timer_max
                        ghost.can_pass_doors = True
                        ghost.mode = 'escape'

            elif ghost.mode == 'escape':
                if ghost.tile.tile_item is not None:
                    ghost.can_pass_doors = False
                    ghost.mode = random.choice(['chase', 'scatter'])
                    ghost.speed = 100


    def handleGhostCollisions(self, pacman):
        for ghost in [self.blinky, self.pinky, self.inky, self.clyde]:
            if ghost.tile == pacman.tile:
                ghost.timer = 0
                if ghost.mode == 'frightened':
                    ghost.mode = 'eaten'
                    ghost.speed = 125
                    ghost.can_pass_doors = True
                    pacman.score += 200
                    self.score.addPoints(200)
                elif ghost.mode == 'chase' or ghost.mode == 'scatter':
                    pacman.lives -= 1
                    pacman.resetPosition()
                    for ghost in [self.blinky, self.pinky, self.inky, self.clyde]:
                        ghost.resetPosition()
                        ghost.mode = 'escape'
                        ghost.can_pass_doors = True
                        ghost.timer = 0
                    if pacman.lives == 0:
                        self.gameOver()

    def handleItemCollisions(self, pacman):
        if pacman.tile.tile_item is not None and not pacman.tile.tile_item.is_eaten:
            points = pacman.tile.tile_item.points
            if points > 0:
                pacman.score += points
            pacman.tile.tile_item.eat()
            if isinstance(pacman.tile.tile_item, PowerPellet):
                for ghost in [self.blinky, self.pinky, self.inky, self.clyde]:
                    ghost.mode = 'frightened'
                    ghost.speed = 50
                    ghost.timer = 0
            self.score.addPoints(points)

    def updateFlashingPowerPellets(self, dt):
        for tile in self.tileCollection.lookup_table.values():
            if tile.tile_item and isinstance(tile.tile_item, PowerPellet):
                tile.tile_item.update(dt)
        

    def gameOver(self):
        self.startGame()
        
if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()