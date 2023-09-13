import pygame, os
from abc import ABC, abstractmethod
from typing import List, Tuple
from constants import *
from vector import Vector2D
from sprites import SpriteSheet

class Item(ABC):
    '''
    Parent class for all items 
    '''
    num_items = 0

    def __init__(self, position: Tuple[float, float]):
        """
        Initialize an Item object.

        Args:
            position (Tuple[float, float]): The position of the item.
        """
        # position attributes
        self.position = Vector2D(*position)
        self.starting_position = self.position.copy()

        # visualization attributes
        self.is_visible = True
        self.sprite = self.load_sprite()
        self.collision_radius = TILE_WIDTH // 2
        self.collected = False
        Item.num_items += 1

    def get_sprite(self):
        '''Returns the sprite of the item'''
        return self.sprite

    @abstractmethod
    def load_sprite(self):
        pass

    def reset(self):
        '''Resets the item to its initial state'''
        self.position = self.starting_position.copy()
        self.collected = False

    def render(self, screen: pygame.Surface):
        '''Renders the item on the screen'''
        if self.is_visible:
            screen.blit(self.sprite, self.position.as_tuple())

class Pellet(Item):
    '''Class representing a pellet'''
    POINTS = 10
    def __init__(self, position: Tuple[float, float]):
        """
        Initialize a Pellet object.

        Args:
            position (Tuple[float, float]): The position of the pellet.
        """
        super().__init__(position)
        self.name = 'pellet'
        self.sprite = self.load_sprite()

    def load_sprite(self):
        '''Loads the pellet sprite'''
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-Tile-Sprites.png'))
        sprite = sprite_sheet.get_image(234, 36, 16, 16)
        return sprite


class PowerPellet(Item):
    '''Class representing a power pellet'''

    POINTS = 10
    def __init__(self, position: Tuple[float, float]):
        """
        Initialize a Pellet object.

        Args:
            position (Tuple[float, float]): The position of the pellet.
        """
        super().__init__(position)
        self.name = 'power_pellet'
        self.flash_interval = 0.25
        self.flash_timer = 0
        self.flashing = False
        self.load_sprite()

    def load_sprite(self):
        '''Loads the pellet sprite'''
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-Tile-Sprites.png'))
        self.normal_sprite = sprite_sheet.get_image(252, 36, 16, 16)
        self.flashing_sprite = sprite_sheet.get_image(270, 36, 16, 16)
        self.sprite = self.normal_sprite
    
    def flash(self, delta_time: float):
        '''Flashes the power pellet'''
        self.flash_timer += delta_time
        if self.flash_timer >= self.flash_interval:
            self.flash_timer = 0
            self.flashing = not self.flashing
            if self.flashing:
                self.sprite = self.flashing_sprite
            else:
                self.sprite = self.normal_sprite

class Cherry(Item):
    '''Class representing a cherry'''
    POINTS = 100
    def __init__(self, position: Tuple[float, float]):
        super().__init__(position)
        self.name = 'cherry'
        self.load_sprite()

    def load_sprite(self):
        '''Loads the cherry sprite'''
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        self.sprite = sprite_sheet.get_image(1, 69, 16, 16)
    
class Strawberry(Item):
    '''Class representing a strawberry'''
    POINTS = 300
    def __init__(self, position: Tuple[float, float]):
        super().__init__(position)
        self.name = 'strawberry'
        self.load_sprite()

    def load_sprite(self):
        '''Loads the strawberry sprite'''
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        self.sprite = sprite_sheet.get_image(18, 69, 16, 16)
        

class Orange(Item):
    '''Class representing an orange'''
    POINTS = 500
    def __init__(self, position: Tuple[float, float]):
        super().__init__(position)
        self.name = 'orange'
        self.load_sprite()

    def load_sprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        self.sprite = sprite_sheet.get_image(35, 69, 16, 16)

class Apple(Item):
    '''Class representing an apple'''
    POINTS = 700
    def __init__(self, position: Tuple[float, float]):
        super().__init__(position)
        self.name = 'apple'
        self.load_sprite()

    def load_sprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        self.sprite = sprite_sheet.get_image(52, 69, 16, 16)

class Pretzel(Item):
    '''Class representing a pretzel'''
    POINTS = 1000
    def __init__(self, position: Tuple[float, float]):
        super().__init__(position)
        self.name = 'pretzel'
        self.load_sprite()

    def load_sprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        self.sprite = sprite_sheet.get_image(69, 69, 16, 16)

class GalaxianFlagship(Item):
    ''''Class representing a galaxian flagship'''
    POINTS = 2000
    def __init__(self, position: Tuple[float, float]):
        super().__init__(position)
        self.name = 'galaxian_flagship'
        self.load_sprite()

    def load_sprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        self.sprite = sprite_sheet.get_image(86, 69, 16, 16)

class Bell(Item):
    ''''Class representing a bell'''
    POINTS = 2000
    def __init__(self, position: Tuple[float, float]):
        super().__init__(position)
        self.name = 'bell'
        self.load_sprite()

    def load_sprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        self.sprite = sprite_sheet.get_image(103, 69, 16, 16)

class Key(Item):
    ''''Class representing a key'''
    POINTS = 5000
    def __init__(self, position: Tuple[float, float]):
        super().__init__(position)
        self.name = 'key'
        self.load_sprite()

    def load_sprite(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        self.sprite = sprite_sheet.get_image(120, 69, 16, 16)






