import pygame
from abc import ABC, abstractmethod
from constants import *
from vector import Vector2D

class Entity(ABC):
    def __init__(self, tile):
        self.color = None
        self.can_pass_doors = True
        self.radius = 10
        self.is_visible = True
        self.speed = 100
        self.directions = {UP : Vector2D(0, -1), DOWN : Vector2D(0, 1), 
                           LEFT : Vector2D(-1, 0), RIGHT : Vector2D(1, 0), None : Vector2D(0, 0)}
        self.current_direction = None
        self.tile = tile
        self.target_tile = tile
        self.start_tile = tile
        self.setPosition()
    
    @staticmethod
    def oppositeDirection(direction):
        if direction == 'up':
            return 'down'
        elif direction == 'down':
            return 'up'
        elif direction == 'left':
            return 'right'
        elif direction == 'right':
            return 'left'
        else:
            return None
    
    def resetPosition(self):
        self.current_direction = None
        self.tile = self.target_tile = self.start_tile
        self.setPosition()

    def setPosition(self):
        self.position = self.tile.position.copy()

    def handlePortal(self):
        if self.target_tile.portal is not None:
                self.target_tile = self.target_tile.portal
                self.tile = self.target_tile
                self.setPosition()

    def hasReachedTargetTile(self):
        position_to_target = self.target_tile.position - self.position
        node_to_target = self.target_tile.position - self.tile.position
        dot_product = position_to_target.dot(node_to_target)
        if dot_product <= 0:
            return True
        return False
    
    def canMoveInDirection(self, direction):
        if direction is not None:
            if self.can_pass_doors == False:
                return self.tile.neighbors[direction].tile_type != 'wall' and \
                     self.tile.neighbors[direction].tile_type != 'ghost_door' 
            else:
                return self.tile.neighbors[direction].tile_type != 'wall' 

    def determineTargetTile(self, direction):
        if self.canMoveInDirection(direction):
            return self.tile.neighbors[direction]
        else:
            return self.tile

    @abstractmethod
    def update(self, dt):
        pass

    def render(self, screen):
        if self.is_visible:
            position = self.position + Vector2D(TILE_WIDTH // 2, TILE_HEIGHT // 2)
            pygame.draw.circle(screen, self.color, position.asTuple(), self.radius)
