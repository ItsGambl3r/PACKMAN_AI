# # Import necessary modules and classes
import pygame, os
from pygame.locals import *
from queue import Queue
from constants import *
from vector import Vector2D
from sprites import SpriteSheet
from entity import Entity

class Agent(Entity):
    def __init__(self, tile, neural_network):
        super().__init__(tile) 

        self.score = 0
        self.lives = self.starting_lives = 3
        self.alive = True
        self.is_idle = False
        self.idle_timer = 0
        self.distance_travelled = 0
        self.survival_time = 0
        self.collected_items = []
        self.neural_network = neural_network

        self.ghost = {}

        # Movement and direction attributes
        self.set_speed(75) 
        self.directions_queue = Queue()
        self.queue_timer = 0
        self.max_queue_time = 0.5
        
        # Sprites and game state attributes
        self.load_sprites()  
        self.phase = None
        self.increment = 1

    def load_sprites(self):
        sprite_sheet = SpriteSheet(os.path.join('pacman', 'assets', 'sprites', 'Pac-Man-General-Sprites.png'))
        self.animation_state = 0
        self.sprites = {}
        self.sprites['idle'] = sprite_sheet.get_image(86, 120, 16, 16)
        self.sprites['moving_1'] = sprite_sheet.get_image(103, 120, 16, 16)
        self.sprites['moving_2'] = sprite_sheet.get_image(103, 103, 16, 16)

    def reset(self):
        self.score = 0
        self.lives = self.starting_lives
        self.alive = True
        self.survival_time = 0
        self.distance_travelled = 0
        self.is_idle = False
        self.idle_timer = 0
        self.directions_queu.clear()

    def reset_position(self):
        super().reset()
        self.directions_queue.clear()
        self.is_idle = False
        self.idle_timer = 0

    def insert_into_queue(self, direction: int):
        '''
        Inserts a direction into the queue

        Args:
            direction (int): The direction to insert into the queue
        '''
        if self.directions_queue.empty() and direction != self.current_direction:
            self.directions_queue.enqueue(direction)
            self.queue_timer = 0
        elif self.directions_queue.size() == 1 and direction != self.directions_queue.end():
            self.directions_queue.enqueue(direction)
            self.queue_timer = 0

    def move(self, action, delta_time: float):
        '''Moves the Agent'''
        self.position += self.directions[self.current_direction] * self.speed * delta_time
        self.queue_timer += delta_time
        
        direction = action

        if direction:
            opposite_direction = Agent.opposite_direction(direction)
            if self.current_direction == opposite_direction:
                self.current_direction = direction
                self.directions_queue.clear()
                self.next_tile, self.tile = self.tile, self.next_tile
            else:
                self.insert_into_queue(direction)
            
        if self.has_reached_next_tile():
            self.check_for_portal()
            self.tile = self.next_tile

            if self.directions_queue.empty():
                next_direction = self.current_direction
            elif self.can_move_in_direction(self.directions_queue.peek()):
                next_direction = self.directions_queue.dequeue()
            else:
                next_direction = self.current_direction
            
            self.next_tile = self.determine_next_tile(next_direction)

            if self.next_tile is not self.tile:
                self.current_direction = next_direction
            else:
                self.current_direction = None
                self.set_position()
                self.directions_queue.clear()
            self.set_position()

        if self.current_direction is None:
            self.idle_timer += delta_time
            if self.idle_timer >= 5:
                self.idle_timer = 0
                self.is_idle = not self.is_idle
        else:
            self.is_idle = False
            self.idle_timer = 0

        if self.queue_timer >= self.max_queue_time:
            self.directions_queue.remove_tail()
            self.clear_queue_timer = 0

    def render(self, screen: pygame.Surface, show_lives: bool = True, show_special_items: bool = False):
        '''Renders the pacman on the screen'''
        position = self.position - Vector2D(4, 4)
        
        if self.alive:
            sprite_key = self.get_sprite_key()
            sprite = self.sprites.get(sprite_key)
            
            if sprite:
                if self.current_direction == LEFT:
                    sprite = pygame.transform.flip(sprite, True, False)
                elif self.current_direction == UP:
                    sprite = pygame.transform.rotate(sprite, 90)
                elif self.current_direction == DOWN:
                    sprite = pygame.transform.rotate(sprite, -90)
                
                sprite = pygame.transform.scale(sprite, (24, 24))
                screen.blit(sprite, position.as_tuple())
        if show_lives:
            self.render_lives(screen)
        
        if show_special_items:
            self.render_special_items(screen)

    def render_lives(self, screen: pygame.Surface):
        '''Renders the lives on the screen'''
        for i in range(self.lives):
            position = Vector2D(8 + i * 32, 550)
            sprite = self.sprites.get('moving_1')
            sprite = pygame.transform.scale(sprite, (24, 24))
            screen.blit(sprite, position.as_tuple())

    def render_special_items(self, screen: pygame.Surface):
        '''Renders the special items on the screen'''
        for i, item in enumerate(self.special_items):
            position = Vector2D(410 - i * 32, 550)
            sprite = item.get_sprite()
            sprite = pygame.transform.scale(sprite, (24, 24))
            screen.blit(sprite, position.as_tuple())

    def get_sprite_key(self):
        '''Returns the sprite key'''
        if self.current_direction:
            if self.animation_state == 0:
                return 'moving_1'
            elif self.animation_state == 1:
                return 'moving_2'
        return 'idle'

    def update(self, action, delta_time: float):
        '''Updates the pacman'''
        if self.lives == 0:
            self.alive = False
        self.move(action, delta_time)
        self.survival_time += delta_time
        self.animation_timer += delta_time
        if self.animation_timer >= 0.1:
            self.animation_timer = 0
            if self.animation_state == 2:
                self.increment = -1
            elif self.animation_state == 0:
                self.increment = 1
            self.animation_state += self.increment