# Import necessary modules and classes
import pygame, os
from typing import List, Tuple
from constants import *
from vector import Vector2D
from sprites import SpriteSheet
from items import Item, Pellet, PowerPellet, Cherry, Strawberry, Orange, Apple
class Tile(object):
    '''Class representing a tile object'''
    num_tiles = 0

    def __init__(self, position: Tuple[float, float], type: str = EMPTY, item: Item = None):
        """
        Initialize a Tile object.

        Args:
            position (Tuple[float, float]): The position of the tile.
            type (str, optional): The type of the tile. Defaults to EMPTY.
            item (item, optional): An item associated with the tile. Defaults to None.
        """
        self.id = Tile.generate_id()
        self.position = Vector2D(*position)
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}

        # tile type and associated item
        self.type = type
        self.item = item

        self.is_portal = False

        # Visualization attributes
        self.color = Tile.determine_color(self.position.y)
        self.sprite = None

        # Increment the number of tiles
        Tile.num_tiles += 1

    @staticmethod
    def generate_id() -> int:
        '''Generates a unique id for the tile'''
        character_id = format(Tile.num_tiles, '03d')
        return int(f'1{character_id}')
    
    @staticmethod
    def determine_color(tile_position_y: float):
        '''Determines the color of the tile'''
        row_index = int(tile_position_y // TILE_WIDTH)
        if (Tile.num_tiles + row_index) % 2 == 0:
            return TILE_COLOR_1
        return TILE_COLOR_2
    
    @staticmethod
    def get_opposite_direction(direction):
        '''Returns the opposite direction'''
        if direction == UP:
            return DOWN
        if direction == DOWN:
            return UP
        if direction == LEFT:
            return RIGHT
        if direction == RIGHT:
            return LEFT
        raise ValueError(f'Invalid direction {direction}')

    def get_neighbor_types(self) -> List[str]:
        '''Returns the types of the neighbors'''
        neighbor_types = []
        for neighbor in self.neighbors.values():
            if neighbor:
                neighbor_types.append(neighbor.type)
            else:
                neighbor_types.append(None)
        return neighbor_types
    
    def get_tile_center(self):
        '''Returns the center of the tile'''
        return self.position + Vector2D(TILE_WIDTH // 2, TILE_HEIGHT // 2)

    def connect(self, direction: str, tile: 'Tile') -> None:
        '''Connects the tile to another tile'''
        self.neighbors[direction] = tile
        tile.neighbors[Tile.get_opposite_direction(direction)] = self

    def set_portal(self, tile):
        '''Sets the tile as a portal'''
        for arg in [self, tile]:
            arg.is_portal = True
            arg.portal_destination = tile if arg is self else self
    
    def render(self, screen: pygame.Surface, show_items: bool = True) -> None:
            '''Renders the tile on the screen'''
            position = self.position.as_tuple()
            pygame.draw.rect(screen, self.color, (*position, TILE_WIDTH, TILE_WIDTH))
            if self.sprite:
                screen.blit(self.sprite, position)
            if show_items and self.item:
                self.item.render(screen)

    def __str__(self):
        return str(self.id)
    
    def __repr__(self):
        return self.__str__()
    
class TileCollection(object):
    '''
    Class representing a collection of tiles
    '''
    def __init__(self):
        self.unique_item = None
        self.tile_symbols = { 
            '0' : 'empty', '.' : 'path', 'X' : 'wall',
            '=' : 'ghost_door', 'H' : 'ghost_house'
            }
        level_data = TileCollection.load_level_data(os.path.join('level_1.txt'))
        self.create_look_up_table(level_data)
        self.set_tile_sprites(level_data)
        self.connect_tiles()
        self.add_items()
        self.get_tile(0, 17).set_portal(self.get_tile(27, 17))

    def load_level_data(level_file: str) -> List[List[str]]:
        '''Loads the level data from a file'''
        level_data = []
        with open(os.path.join('pacman', 'assets', 'levels', level_file)) as file:
            for line in file:
                line = line.strip().split()
                if line:
                    level_data.append(list(line))
        return level_data
    
    def create_look_up_table(self, level_data: List[List[str]]) -> None:
        '''Creates a lookup table for the level data'''
        self.look_up_table = {}
        for row_index, row in enumerate(level_data):
            for column_index, tile_symbol in enumerate(row):
                tile_type = self.tile_symbols[tile_symbol]
                position = (column_index * TILE_WIDTH, row_index * TILE_WIDTH)
                self.look_up_table[(column_index, row_index)] = Tile(position, tile_type)

    def set_tile_sprites(self, level_data: List[List[str]]) -> None:
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Maze-Parts.png'))
        for row_index, row in enumerate(level_data):
            for column_index, tile in enumerate(row):
                try:
                    sprite = SpriteSheet.get_image(sprite_sheet, column_index * TILE_WIDTH, row_index * TILE_WIDTH, TILE_WIDTH, TILE_HEIGHT)
                    self.look_up_table[(column_index, row_index)].sprite = sprite
                except:
                    pass
            

    def connect_tiles(self) -> None:
        for row_index in range(NUM_ROWS):
            for column_index in range(NUM_COLS):
                tile = self.look_up_table[(column_index, row_index)]
                if row_index > 0:
                    tile.connect(UP, self.look_up_table[(column_index, row_index - 1)])
                if row_index < NUM_ROWS - 1:
                    tile.connect(DOWN, self.look_up_table[(column_index, row_index + 1)])
                if column_index > 0:
                    tile.connect(LEFT, self.look_up_table[(column_index - 1, row_index)])
                if column_index < NUM_COLS - 1:
                    tile.connect(RIGHT, self.look_up_table[(column_index + 1, row_index)])
                # tile.set_tile_sprite()

    def get_tile(self, column_index: int, row_index: int) -> Tile:
        '''Returns the tile at the given column and row index'''
        return self.look_up_table[(column_index, row_index)]
    
    def add_items(self):
        '''Adds items to the tiles'''
        self.items = []
        for row_index in range(NUM_ROWS):
            for column_index in range(NUM_COLS):
                tile = self.look_up_table[(column_index, row_index)]
                if tile.type == PATH:
                    tile.item = Pellet(tile.position.as_tuple())
                    self.items.append(tile.item)
        self.power_pellets = []
        power_pellet_locations = [(1, 6), (26, 6), (1, 26), (26, 26)]
        for location in power_pellet_locations:
            self.look_up_table[location].item = PowerPellet(self.look_up_table[location].position.as_tuple())
            self.items.append(self.look_up_table[location].item)
            self.power_pellets.append(self.look_up_table[location].item)

    def render(self, screen: pygame.Surface) -> None:
        '''Renders the tiles on the screen'''
        for tile in self.look_up_table.values():
            tile.render(screen)
    