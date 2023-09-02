import pygame
import os
from constants import *
from vector import Vector2D
from dataStructures import Queue
from entity import Entity
from sprites import SpriteSheet

class Agent(Entity):
    def __init__(self, tile):
        super().__init__(tile)
        self.score = 0
        self.survival_time = 0
        self.is_dead = False
        self.lives = 1
        self.direction_queue = Queue()
        self.clear_queue_timer = 0
        self.clear_queue_timer_max = 0.3
        self.flash_timer = 0
        self.flash_interval = 0.2
        self.can_pass_doors = False #TODO: please rename
        self.loadSprite()

    def loadSprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'Assets', 'Sprites', 'test9.png'))
        self.left_sprite = sprite_sheet.get_image(1, 37)
        self.right_sprite = self.icon_sprite = sprite_sheet.get_image(10, 37)
        self.down_sprite = sprite_sheet.get_image(19, 37)
        self.up_sprite = sprite_sheet.get_image(28, 37)
        self.closed_sprite = sprite_sheet.get_image(37, 37) #TODO: look at
        self.sprites = {'up': self.up_sprite, 'down': self.down_sprite, 'left': self.left_sprite, 'right': self.right_sprite}

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

    def update(self, action, delta_time):
        # Update position based on current direction and speed

        self.position += self.directions[self.current_direction] * self.speed * delta_time
        self.survival_time += delta_time
        self.clear_queue_timer += delta_time
        
        direction = action

        if direction is not None:
            opposite_dir = Agent.oppositeDirection(direction)

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

    def flash(self, delta_time):
        self.flash_timer += delta_time
        if self.flash_timer >= self.flash_interval:
            self.flash_timer -= self.flash_interval
            self.is_visible = not self.is_visible

    def render(self, screen):
        if self.is_visible and self.current_direction is not None:
            screen.blit(self.sprites[self.current_direction], self.position.asTuple())
        else:
            screen.blit(self.closed_sprite, self.position.asTuple())
        
        for i in range(self.lives):
            position = Vector2D(10 + i * 30, 10)
            screen.blit(self.icon_sprite, position.asTuple())

