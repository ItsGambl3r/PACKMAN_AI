import pygame, os, random
from constants import *
from vector import Vector2D
from entity import Entity
from sprites import SpriteSheet


SCALE_FACTOR = 2

class Ghost(Entity):
    '''
    Class representing a ghost
    '''
    def __init__(self, tile):
        super().__init__(tile)
        self.target = None
        self.set_speed(75)
        self.elapsed_time = 0
        self.phase = LEAVE_GHOST_HOUSE
        self.load_sprites()
        self.collision_radius = 8

    def set_phase(self, phase: int):
        '''
        Sets the phase of the ghost

        Args:
            phase (int): The phase to set the ghost to
        '''
        self.phase = phase

    def load_sprites(self):
        '''Loads the sprites for the ghost'''
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        self.sprites = {}
        self.sprites['frightened_1'] = sprite_sheet.get_image(1, 86, 16, 16)
        self.sprites['frightened_2'] = sprite_sheet.get_image(18, 86, 16, 16)
        self.sprites['eaten_1'] = sprite_sheet.get_image(35, 86, 16, 16)
        self.sprites['eaten_2'] = sprite_sheet.get_image(52, 86, 16, 16)    

    def determine_next_direction(self):
        '''Determines the next direction to move in'''
        possible_directions = []
        for direction in self.directions:
                if direction != Entity.opposite_direction(self.current_direction):
                    if self.can_move_in_direction(direction):
                        possible_directions.append(direction)
                    
        if len(possible_directions) == 1:
            return possible_directions[0]
    
        distances = {}
        for direction in possible_directions:
            neighbor = self.tile.neighbors[direction]
            distances[direction] = self.target.position.distance(neighbor.position)
        next_direction = min(distances, key=distances.get)
        return next_direction
    
    def move(self, delta_time: float):
        self.position += self.directions[self.current_direction] * self.speed * delta_time
        if self.has_reached_next_tile():
            self.check_for_portal()
            self.tile = self.next_tile
            self.current_direction = self.determine_next_direction()
            self.next_tile = self.determine_next_tile(self.current_direction)
            
    def update(self, delta_time: float):
        '''Updates the ghost'''
        self.move(delta_time)
        self.animation_timer += delta_time
        if self.animation_timer >= .20:
            self.animation_timer = 0
            self.sprite_toggle = not self.sprite_toggle

    def render(self, screen):
        '''Renders the ghost'''
        sprite_key = None

        if self.phase in [LEAVE_GHOST_HOUSE, CHASE, SCATTER]:
            direction_sprites = {
                UP: ['up_1', 'up_2'],
                DOWN: ['down_1', 'down_2'],
                LEFT: ['left_1', 'left_2'],
                RIGHT: ['right_1', 'right_2'],
            }
            sprite_key = direction_sprites.get(self.current_direction)

        elif self.phase == FRIGHTENED:
            sprite_key = ['frightened_1', 'frightened_2']
        elif self.phase == EATEN:
            sprite_key = ['eaten_1', 'eaten_2']

        if sprite_key:
            # position = self.position - Vector2D(8, 8)
            position = self.position - Vector2D(4, 4)
            if self.sprite_toggle:
                sprite = self.sprites[sprite_key[0]]
                sprite = pygame.transform.scale(sprite, (24, 24))
                screen.blit(sprite, position.as_tuple())
            else:
                sprite = self.sprites[sprite_key[1]]
                sprite = pygame.transform.scale(sprite, (24, 24))
                screen.blit(sprite, position.as_tuple())

class Blinky(Ghost):
    '''Class representing Blinky'''
    def __init__(self, tile):
        super().__init__(tile)
        self.add_sprites()

    def add_sprites(self):
        '''Adds the sprites for Blinky'''
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        directions = ['right', 'down', 'left', 'up']
        x, y = 1, 1
        for direction in directions:
            for i in range(1, 3):
                self.sprites[f'{direction}_{i}'] = sprite_sheet.get_image(x, y, 16, 16)
                x += 17

    def find_target(self, pacman, look_up_table):
        '''Finds the target tile for Blinky'''
        if self.phase == SCATTER: 
            self.target = look_up_table[(27, 0)]
        elif self.phase == CHASE:
            self.target = pacman.tile 
        elif self.phase == FRIGHTENED:
            self.target = random.choice(list(look_up_table.values()))
        elif self.phase == EATEN:
            self.target = look_up_table[(16, 16)]
        elif self.phase == LEAVE_GHOST_HOUSE:
            self.target = look_up_table[(15, 10)]

    def update(self, delta_time: float, pacman, look_up_table: dict):
        self.find_target(pacman, look_up_table)
        return super().update(delta_time)
    
class Pinky(Ghost):
    '''Class representing Pinky'''
    def __init__(self, tile):
        super().__init__(tile)
        self.add_sprites()

    def add_sprites(self):
        '''Adds the sprites for Pinky'''
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        directions = ['right', 'down', 'left', 'up']
        x, y = 1, 18
        for direction in directions:
            for i in range(1, 3):
                self.sprites[f'{direction}_{i}'] = sprite_sheet.get_image(x, y, 16, 16)
                x += 17

    def find_target(self, pacman, look_up_table):
        '''Finds the target tile for Pinky'''
        if self.phase == SCATTER: 
            self.target = look_up_table[(0, 0)]
        elif self.phase == CHASE:
            self.target = pacman.tile
        elif self.phase == FRIGHTENED:
            self.target = random.choice(list(look_up_table.values()))
        elif self.phase == EATEN:
            self.target = look_up_table[(11, 16)]
        elif self.phase == LEAVE_GHOST_HOUSE:
            self.target = look_up_table[(13, 10)]

    def update(self, delta_time: float, pacman, look_up_table: dict):
        self.find_target(pacman, look_up_table)
        return super().update(delta_time)
    
class Inky(Ghost):
    '''Class representing Inky'''
    def __init__(self, tile):
        super().__init__(tile)
        self.add_sprites()

    def add_sprites(self):
        '''Adds the sprites for Inky'''
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        directions = ['right', 'down', 'left', 'up']
        x, y = 1, 35
        for direction in directions:
            for i in range(1, 3):
                self.sprites[f'{direction}_{i}'] = sprite_sheet.get_image(x, y, 16, 16)
                x += 17

    def find_target(self, pacman, look_up_table):
        '''Finds the target tile for Inky'''
        if self.phase == SCATTER: 
            self.target = look_up_table[(27, 35)]
        elif self.phase == CHASE:
            self.target = pacman.tile
        elif self.phase == FRIGHTENED:
            self.target = random.choice(list(look_up_table.values()))
        elif self.phase == EATEN:
            self.target = look_up_table[(11, 18)]
        elif self.phase == LEAVE_GHOST_HOUSE:
            self.target = look_up_table[(17, 10)]

    def update(self, delta_time: float, pacman, look_up_table: dict):
        self.find_target(pacman, look_up_table)
        return super().update(delta_time)
    
class Clyde(Ghost):
    '''Class representing Clyde'''
    def __init__(self, tile):
        super().__init__(tile)
        self.add_sprites()

    def add_sprites(self):
        '''Adds the sprites for Clyde'''
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        directions = ['right', 'down', 'left', 'up']
        x, y = 1, 52
        for direction in directions:
            for i in range(1, 3):
                self.sprites[f'{direction}_{i}'] = sprite_sheet.get_image(x, y, 16, 16)
                x += 17

    def find_target(self, pacman, look_up_table):
        '''Finds the target tile for Clyde'''
        if self.phase == SCATTER: 
            self.target = look_up_table[(0, 35)]
        elif self.phase == CHASE:
            self.target = pacman.tile
        elif self.phase == FRIGHTENED:
            self.target = random.choice(list(look_up_table.values()))
        elif self.phase == EATEN:
            self.target = look_up_table[(16, 18)]
        elif self.phase == LEAVE_GHOST_HOUSE:
            self.target = look_up_table[(10, 10)]

    def update(self, delta_time: float, pacman, look_up_table: dict):
        self.find_target(pacman, look_up_table)
        return super().update(delta_time)