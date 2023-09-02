import pygame
import os
from constants import *
from vector import Vector2D
from sprites import SpriteSheet
from pellets import Pellet, PowerPellet, Fruit

class Tile(object):
    num_tiles = 0 

    def __init__(self, position: tuple, tile_type: str = 'empty', tile_item = None):
        self.id = Tile.generateCharacterID()
        self.position = Vector2D(*position)
        self.neighbors = {UP : None, DOWN : None, LEFT : None, RIGHT : None}
        self.color = Tile.determineColor(self.position.y)
        self.font = pygame.font.Font(os.path.join('pacman', 'Assets', 'Fonts', 'PressStart2P-Regular.ttf'), 6)
        self.tile_type = tile_type # 'empty' or 'wall' or 'tunnel' or 'ghost_spawn' or or 'ghost_door' 
        self.tile_item = tile_item 
        self.sprite = None
        self.portal = None
        Tile.num_tiles += 1

    @staticmethod
    def generateCharacterID():
        num = Tile.num_tiles 
        character_id = format(num, '02X')  # Format num as a two-character hexadecimal string
        return character_id
    
    @staticmethod
    def determineColor(tile_position_y):
        row_index = tile_position_y // TILE_HEIGHT
        if (Tile.num_tiles + row_index) % 2 == 0:
            return (32, 36, 39)  #202427
        else:
            return (36, 40, 44)  #24282C
        
    @staticmethod
    def getOppositeDirection(direction):
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
        
    def getTileCenter(self):
        return (self.position.x + TILE_WIDTH // 2, self.position.y + TILE_HEIGHT // 2)
        
    def connect(self, neighbor, direction):
        self.neighbors[direction] = neighbor
        neighbor.neighbors[Tile.getOppositeDirection(direction)] = self

    def setWallSprite(self, tile_sheet):
        if self.tile_type == 'wall':
            neighbor_tiles = [neighbor for neighbor in self.neighbors.values() if neighbor]
            neighbor_tile_types = [tile.tile_type for tile in neighbor_tiles]
            
            if neighbor_tile_types == ['empty', 'empty', 'empty', 'empty']:
                pass

            # top left corners
            elif neighbor_tile_types == ['empty', 'wall', 'empty', 'wall']:
                self.sprite = tile_sheet.get_image(10, 1)

            # top right corners
            elif neighbor_tile_types == ['empty', 'wall', 'wall', 'empty']:
                self.sprite = tile_sheet.get_image(1, 1)

            # bottom left corners
            elif neighbor_tile_types == ['wall', 'empty', 'empty', 'wall']:
                self.sprite = tile_sheet.get_image(10, 10)

            # bottom right corners
            elif neighbor_tile_types == ['wall', 'empty', 'wall', 'empty']:
                self.sprite = tile_sheet.get_image(1, 10)
            
            # horizontal walls
            elif neighbor_tile_types == ['empty', 'empty', 'wall', 'wall']:
                self.sprite = tile_sheet.get_image(28, 1)

            elif neighbor_tile_types == ['empty', 'empty', 'empty', 'wall']:
                self.sprite = tile_sheet.get_image(28, 1)

            elif neighbor_tile_types == ['empty', 'empty', 'wall', 'empty']:
                self.sprite = tile_sheet.get_image(28, 1)
            
            elif neighbor_tile_types == ['empty', 'empty', 'empty', 'wall']:
                self.sprite = tile_sheet.get_image(28, 1)

            elif neighbor_tile_types == ['empty', 'empty', 'ghost_door', 'wall']:
                self.sprite = tile_sheet.get_image(28, 1)
            elif neighbor_tile_types == ['empty', 'empty', 'wall', 'ghost_door']:
                self.sprite = tile_sheet.get_image(28, 1)

            # vertical walls
            elif neighbor_tile_types == ['wall', 'wall', 'empty', 'empty']:
                self.sprite = tile_sheet.get_image(19, 1)

            # special cases
            elif neighbor_tile_types == ['empty', 'wall', 'wall', 'wall']:
                self.sprite = tile_sheet.get_image(19, 10)
            
            elif neighbor_tile_types == ['wall', 'empty', 'wall', 'wall']:
                self.sprite = tile_sheet.get_image(28, 10)

            elif neighbor_tile_types == ['wall', 'wall', 'empty', 'wall']:
                self.sprite = tile_sheet.get_image(37, 1)

            elif neighbor_tile_types == ['wall', 'wall', 'wall', 'empty']:
                self.sprite = tile_sheet.get_image(37, 10)
            
            elif neighbor_tile_types == ['wall', 'wall', 'wall', 'wall']:
                self.sprite = tile_sheet.get_image(46, 1)
        
    def render(self, screen):
        tile_position = self.position.asTuple()
        pygame.draw.rect(screen, self.color, (tile_position, (TILE_WIDTH, TILE_HEIGHT)))
        if self.sprite:  # Check if the sprite is not None before blitting
            screen.blit(self.sprite, tile_position)
        if isinstance(self.tile_item, Pellet):
            self.tile_item.render(screen)
        elif isinstance(self.tile_item, PowerPellet):
            self.tile_item.render(screen)
        elif isinstance(self.tile_item, Fruit):
            self.tile_item.render(screen)
       
    def __str__(self):
        return str(self.id)
    
    def __repr__(self):
        return self.__str__()

class TileCollection(object):
    def __init__(self, level_file: str):
        self.tile_symbols = {'.' : 'empty', 'X' : 'wall', '=': 'ghost_door'}
        level_data, item_data = self.loadLevel(level_file)
        self.createLookupTable(level_data)
        self.addTileItems(item_data)
        self.connectNeighbors(level_data)

    @staticmethod
    def getKey(x, y):
        return (x * TILE_WIDTH, y * TILE_HEIGHT)
    
    @staticmethod
    def transpose(data):
        return [list(row) for row in zip(*data)]
    
    def loadLevel(self, level_file, level_item_file = os.path.join('pacman', 'Assets', 'Levels', 'collectibles_map.txt')):
        level_data = []
        with open(level_file, 'r') as file:
            for line in file:
                formatted_line = line.strip().split()
                if formatted_line:
                    level_data.append(formatted_line)

        item_data = []
        with open(level_item_file, 'r') as file:
            for line in file:
                formatted_line = line.strip().split()
                if formatted_line:
                    item_data.append(formatted_line)
        return level_data, item_data
    
    def createLookupTable(self, level_data):
        self.lookup_table = {}
        for row_index, row in enumerate(level_data):
            for col_index, symbol in enumerate(row):
                position = TileCollection.getKey(col_index, row_index)
                self.lookup_table[position] = Tile(position, self.tile_symbols[symbol])

    def addTileItems(self, item_data):
        for row_index, row in enumerate(item_data):
            for col_index, item_symbol in enumerate(row):
                position = TileCollection.getKey(col_index, row_index)
                if position in self.lookup_table:
                    current_tile = self.lookup_table[position]
                    self.attachItemToTile(current_tile, item_symbol)
                else:
                    print(f"Warning: No tile found at position {position} for {item_symbol}.")

    def attachItemToTile(self, tile, item_symbol):
        position = tile.position.asTuple()
        if item_symbol == '.':
            tile.tile_item = Pellet(*position)
        elif item_symbol == '+':
            tile.tile_item = PowerPellet(*position)
        elif item_symbol == 'F':
            tile.tile_item = Fruit(*position)


    def connectNeighbors(self, data):
        for i in range(len(data)):
            for j in range(len(data[i])):
                current_tile = self.lookup_table[TileCollection.getKey(j, i)]

                if i > 0:
                    above_tile = self.lookup_table.get(TileCollection.getKey(j, i - 1))
                    current_tile.connect(above_tile, UP)
                            
                if i < len(data) - 1:
                    below_tile = self.lookup_table.get(TileCollection.getKey(j, i + 1))
                    current_tile.connect(below_tile, DOWN)
                
                if j > 0:
                    left_tile = self.lookup_table.get(TileCollection.getKey(j - 1, i))
                    current_tile.connect(left_tile, LEFT)
                
                if j < len(data[i]) - 1:
                    right_tile = self.lookup_table.get(TileCollection.getKey(j + 1, i))
                    current_tile.connect(right_tile, RIGHT)

                current_tile.setWallSprite(SpriteSheet(os.path.join('pacman', 'Assets', 'Sprites', 'test9.png')))

    def render(self, screen):
        for tile in self.lookup_table.values():
            tile.render(screen)
            '''tile_center = tile.getTileCenter()  # Get the tile center from the current tile
            text = tile.font.render(tile.id, True, (255, 255, 255))
            text_rect = text.get_rect(center=tile_center)
            screen.blit(text, text_rect)'''


