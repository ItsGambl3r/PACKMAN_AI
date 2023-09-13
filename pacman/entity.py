# Import necessary modules and classes
from abc import ABC, abstractmethod
from typing import List, Tuple
from constants import *
from vector import Vector2D

class Entity(ABC):
    def __init__(self, tile):
        self.elapsed_time, self.timer = 0, 0
        self.phase = LEAVE_GHOST_HOUSE
        self.animation_timer = 0
        self.is_visible = True
        self.sprite_toggle = False

        # Movement Attributes
        self.speed = 0
        self.directions = {
            UP : Vector2D(0, -1),
            DOWN : Vector2D(0, 1),
            LEFT : Vector2D(-1, 0),
            RIGHT : Vector2D(1, 0),
            None : Vector2D(0, 0)
        }
        self.current_direction = None

        # Tile Related Attributes
        self.tile = tile
        self.next_tile = tile
        self.starting_tile = tile

        # Initialize the entity's position
        self.set_position()

    @staticmethod  
    def opposite_direction(direction: int) -> int:
        '''
        Returns the opposite direction

        Args:
            direction (int): The direction to get the opposite of
        '''
        if direction == UP:
            return DOWN
        if direction == DOWN:
            return UP
        if direction == LEFT:
            return RIGHT
        if direction == RIGHT:
            return LEFT
        return None
    
    def reset(self):
        '''Resets the entity to its initial state'''
        self.elapsed_time = 0
        self.current_direction = None
        self.tile = self.next_tile = self.starting_tile
        self.set_position()

    def set_position(self):
        '''Sets the entity's position'''
        self.position = self.tile.position.copy()
    
    def set_speed(self, speed: float):
        '''
        Sets the entity's speed

        Args:
            speed (float): The speed to set
        '''
        self.speed = speed

    def has_reached_next_tile(self) -> bool:
        '''Returns whether the entity has reached the next tile'''
        positon_to_target = self.next_tile.position - self.position
        tile_to_target = self.next_tile.position - self.tile.position
        dot_product = positon_to_target.dot(tile_to_target)
        return dot_product <= 0
    
    def check_for_portal(self):
        '''Checks if the entity is on a portal'''
        if self.next_tile.is_portal:
            self.next_tile = self.next_tile.portal_destination
            self.tile = self.next_tile
            self.set_position()
    
    def can_move_in_direction(self, direction):
        '''
        Returns whether the entity can move in the given direction
        based on the entity's current phase
        Args:
            direction (int): The direction to check
        '''
        if direction is None:
            return False
        else:
            movement_rules = { 
                None : [WALL, GHOST_DOOR, GHOST_HOUSE],
                SCATTER : [WALL, GHOST_DOOR, GHOST_HOUSE],
                CHASE : [WALL, GHOST_DOOR, GHOST_HOUSE],
                FRIGHTENED : [WALL, GHOST_DOOR, GHOST_HOUSE],
                EATEN : [WALL],
                LEAVE_GHOST_HOUSE : [WALL]
            }

            current_phase = self.phase
            tile_type = self.tile.neighbors[direction].type
            if tile_type in movement_rules[current_phase]:
                return False
            return True
        
    def determine_next_tile(self, direction):
        ''' Determines the next tile for the entity to move to '''
        if self.can_move_in_direction(direction):
            return self.tile.neighbors[direction]
        return self.tile
    
    @abstractmethod
    def update(self, delta_time):
        pass

    @abstractmethod
    def render(self, screen):
        pass