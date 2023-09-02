import pygame
import os
from pygame.locals import *
from constants import *
from vector import Vector2D
from dataStructures import Queue
from entity import Entity
from sprites import SpriteSheet

class Pacman(Entity):
    def __init__(self, tile):
        super().__init__(tile)
        self.color = YELLOW
        self.can_pass_doors = False
        self.score = 0
        self.lives = 1
        self.close_timer = 0
        self.close_interval = 0.2
        self.direction_queue = Queue()
        self.clear_queue_timer = 0
        self.clear_queue_timer_max = 0.3
        self.loadSprite()
        
    def loadSprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'Assets', 'Sprites', 'test9.png'))
        self.left_sprite = sprite_sheet.get_image(1, 37)
        self.right_sprite = self.life_sprite = sprite_sheet.get_image(10, 37)
        self.down_sprite = sprite_sheet.get_image(19, 37)
        self.up_sprite = sprite_sheet.get_image(28, 37)
        self.sprite = self.closed_sprite = sprite_sheet.get_image(37, 37)

    @staticmethod
    def fetchInput():
        keys = pygame.key.get_pressed()
        if keys[K_UP] or keys[K_w]:
            return UP
        elif keys[K_DOWN] or keys[K_s]:
            return DOWN
        elif keys[K_LEFT] or keys[K_a]:
            return LEFT
        elif keys[K_RIGHT] or keys[K_d]:
            return RIGHT
        else:
            return None
        
    def resetPosition(self):
        self.current_direction = None
        self.tile = self.target_tile = self.start_tile
        self.setPosition()
        self.direction_queue.clear()
        
    def insertIntoQueue(self, direction):
        if self.direction_queue.empty() and self.current_direction != direction:
            self.direction_queue.enqueue(direction)
            self.clear_queue_timer = 0
        if (1 <= self.direction_queue.size() < 2) and self.direction_queue.end() != direction: 
                self.direction_queue.enqueue(direction)
                self.clear_queue_timer = 0       
                
    def update(self, dt):
        self.position += self.directions[self.current_direction] * self.speed * dt
        self.clear_queue_timer += dt
        direction = Pacman.fetchInput()

        if direction is not None:
            opposite_dir = Pacman.oppositeDirection(direction)
            
            if self.current_direction == opposite_dir:
                self.current_direction = direction
                self.direction_queue.clear()
                self.target_tile, self.tile = self.tile, self.target_tile
            else:
                self.insertIntoQueue(direction)

        if self.hasReachedTargetTile():
            self.handlePortal()
            
            self.tile = self.target_tile
            if self.direction_queue.empty():
                next_direction = self.current_direction
            elif self.canMoveInDirection(self.direction_queue.peek()):
                next_direction = self.direction_queue.dequeue()
            else:
                next_direction = self.current_direction

            self.target_tile = self.determineTargetTile(next_direction)
            if self.target_tile is not self.tile:
                self.current_direction = next_direction
            else:
                self.current_direction = None
                self.setPosition()
                self.direction_queue.clear()

            if self.clear_queue_timer >= self.clear_queue_timer_max:
                self.direction_queue.removeTail()
                self.clear_queue_timer = 0

    def flash(self, dt):
        self.close_timer += dt
        if self.close_timer >= self.close_interval:
            self.close_timer -= self.close_interval
            self.is_visible = not self.is_visible

    def render(self, screen):
        if self.is_visible:
            if self.current_direction == LEFT:
                self.sprite = self.left_sprite
            elif self.current_direction == RIGHT:
                self.sprite = self.right_sprite
            elif self.current_direction == DOWN:
                self.sprite = self.down_sprite
            elif self.current_direction == UP:
                self.sprite = self.up_sprite
            screen.blit(self.sprite, self.position.asTuple())
        else:
            screen.blit(self.closed_sprite, self.position.asTuple())

        for lives in range(self.lives):
            position = Vector2D(10 + lives * 30, 10)
            screen.blit(self.life_sprite, position.asTuple())
                

            

    
