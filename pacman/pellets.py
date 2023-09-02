import pygame
import os
from constants import *
from vector import Vector2D
from sprites import SpriteSheet 

class Pellet():
    def __init__(self, x, y):
        self.position = Vector2D(x, y)
        self.points = 10
        self.is_eaten = False
        self.loadSprite()

    def loadSprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'Assets', 'Sprites', 'test9.png'))
        self.sprite = sprite_sheet.get_image(1, 19)

    def eat(self):
        self.is_eaten = True
        self.position = Vector2D(-100, -100)
    
    def render(self, screen):
        if not self.is_eaten:
            screen.blit(self.sprite, self.position.asTuple())

class PowerPellet():
    def __init__(self, x, y):
        self.position = Vector2D(x, y)
        self.points = 50
        self.is_eaten = False
        self.flash_timer = 0
        self.flash_interval = 0.2
        self.is_visible = True
        self.loadSprite()

    def loadSprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'Assets', 'Sprites', 'test9.png'))
        self.sprite = sprite_sheet.get_image(19, 19)
        self.flashing_sprite = sprite_sheet.get_image(10, 19)

    def eat(self):
        self.is_eaten = True
        self.position = Vector2D(-100, -100)

    def update(self, dt):
        self.flash_timer += dt
        if self.flash_timer >= self.flash_interval:
            self.flash_timer -= self.flash_interval
            self.is_visible = not self.is_visible

    def flash(self, dt):
        self.flash_timer += dt
        if self.flash_timer >= self.flash_interval:
            self.flash_timer -= self.flash_interval
            self.is_visible = not self.is_visible

    def render(self, screen):
        if not self.is_eaten:
            if self.is_visible:
                screen.blit(self.sprite, self.position.asTuple())
            else:
                screen.blit(self.flashing_sprite, self.position.asTuple())

class Fruit():
    def __init__(self, x, y):
        self.position = Vector2D(x, y)
        self.points = 100
        self.is_eaten = False
        self.loadSprite()

    def loadSprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'Assets', 'Sprites', 'test9.png'))
        self.sprite = sprite_sheet.get_image(28, 19)

    def eat(self):
        self.is_eaten = True
        self.position = Vector2D(-100, -100)

    def render(self, screen):
        if not self.is_eaten:
            screen.blit(self.sprite, self.position.asTuple())
