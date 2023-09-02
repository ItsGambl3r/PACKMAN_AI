import pygame
import os
import random
from constants import *
from vector import Vector2D
from entity import Entity
from dataStructures import Queue
from sprites import SpriteSheet

class Ghost(Entity):
    def __init__(self, tile):
        super().__init__(tile)
        self.speed = 100
        self.target = None
        self.timer = 0
        self.scatter_timer_max = 7
        self.chase_timer_max = 15
        self.eaten_timer_max = 6
        self.frightened_timer_max = 10
        self.mode = 'escape' # 'scatter', 'frightened', 'eaten', 'chase', 'escape'
        self.loadSprites()

    def loadSprites(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'Assets', 'Sprites', 'test9.png'))
        self.frightened_sprite = sprite_sheet.get_image(37, 28)
        self.eaten_sprite = sprite_sheet.get_image(46, 28)

    def determineNextDirection(self):
        possible_directions = []
    
        # Iterate through available directions
        for direction in self.directions:
            # Check if the direction is not the opposite of the current direction
            if direction != self.oppositeDirection(self.current_direction):
                # Check if the ghost can move in this direction without hitting a wall
                if self.canMoveInDirection(direction):
                    possible_directions.append(direction)
        
        if len(possible_directions) == 1:
            return possible_directions[0]  # Only one possible direction
        
        # Calculate distances to target for each possible direction
        distances = {}
        for direction in possible_directions:
            neighbor = self.tile.neighbors[direction]
            distance = neighbor.position.distance(self.target.position)
            distances[direction] = distance
        
        # Choose the direction with the shortest distance to the target
        next_direction = min(distances, key=distances.get)
        return next_direction
    
    def update(self, dt):
        self.position += self.directions[self.current_direction] * self.speed * dt
        
        if self.hasReachedTargetTile():
            self.handlePortal()
            self.tile = self.target_tile
            next_direction = self.determineNextDirection()
            self.target_tile = self.determineTargetTile(next_direction)
            self.current_direction = next_direction
    
    def render(self, screen):
        if self.mode == 'chase' or self.mode == 'scatter' or self.mode == 'escape':
            screen.blit(self.sprite, self.position.asTuple())
        elif self.mode == 'frightened':
            screen.blit(self.frightened_sprite, self.position.asTuple())
        elif self.mode == 'eaten':
            screen.blit(self.eaten_sprite, self.position.asTuple())

class Blinky(Ghost):
    def __init__(self, tile):
        super().__init__(tile)
        self.target = None
        self.addSprite()

    def addSprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'Assets', 'Sprites', 'test9.png'))
        self.sprite = sprite_sheet.get_image(1, 28)

    def findTarget(self, pacman, lookup_table):
        if self.mode == 'scatter':
            self.target = lookup_table[(696, 0)] # Top right corner
        elif self.mode == 'chase':
            self.target = pacman.tile #TODO: change for each ghost
        elif self.mode == 'frightened':
            self.target = random.choice(list(lookup_table.values()))
        elif self.mode == 'eaten':
            self.target = lookup_table[(408, 384)] # Ghost house
        elif self.mode == 'escape':
            self.target = lookup_table[(384, 312)]

    def update(self, dt, pacman, lookup_table):
        self.findTarget(pacman, lookup_table)
        super().update(dt)
           
class Pinky(Ghost):
    def __init__(self, tile):
        super().__init__(tile)
        self.color = PINK
        self.addSprite()

    def addSprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'Assets', 'Sprites', 'test9.png'))
        self.sprite = sprite_sheet.get_image(10, 28)

    def findTarget(self, pacman, lookup_table):
        if self.mode == 'scatter':
            self.target = lookup_table[(0, 0)] # Top left corner
        elif self.mode == 'chase':
            self.target = pacman.tile #TODO: change for each ghost
        elif self.mode == 'frightened':
            self.target = random.choice(list(lookup_table.values()))
        elif self.mode == 'eaten':
            self.target = lookup_table[(288, 384)] # Ghost house
        elif self.mode == 'escape':
            self.target = lookup_table[(336, 312)]
    
    def update(self, dt, pacman, lookup_table):
        self.findTarget(pacman, lookup_table)
        super().update(dt)

class Inky(Ghost):
    def __init__(self, tile):
        super().__init__(tile)
        self.addSprite()

    def addSprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'Assets', 'Sprites', 'test9.png'))
        self.sprite = sprite_sheet.get_image(19, 28)

    def findTarget(self, pacman, lookup_table):
        if self.mode == 'scatter':
            self.target = lookup_table[(696, 840)] # Bottom right corner
        elif self.mode == 'chase':
            self.target = pacman.tile #TODO: change for each ghost
        elif self.mode == 'frightened':
            self.target = random.choice(list(lookup_table.values()))
        elif self.mode == 'eaten':
            self.target = lookup_table[(408, 432)] # Ghost house
        elif self.mode == 'escape':
            self.target = lookup_table[(384, 312)]
    
    def update(self, dt, pacman, lookup_table):
        self.findTarget(pacman, lookup_table)
        super().update(dt)

class Clyde(Ghost):
    def __init__(self, tile):
        super().__init__(tile)
        self.color = ORANGE
        self.addSprite()

    def addSprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'Assets', 'Sprites', 'test9.png'))
        self.sprite = sprite_sheet.get_image(28, 28)

    def findTarget(self, pacman, lookup_table):
        if self.mode == 'scatter':
            self.target = lookup_table[(0, 840)] # Bottom left corner
        elif self.mode == 'chase':
            self.target = pacman.tile #TODO: change for each ghost
        elif self.mode == 'frightened':
            self.target = random.choice(list(lookup_table.values()))
        elif self.mode == 'eaten':
            self.target = lookup_table[(288, 432)]
        elif self.mode == 'escape':
            self.target = lookup_table[(336, 312)]
        elif self.mode == 'escape':
            self.target = lookup_table[(336, 312)]
    
    def update(self, dt, pacman, lookup_table):
        self.findTarget(pacman, lookup_table)
        super().update(dt)