import pygame
from pygame.locals import *
from hashMap import HashMap
from vector import Vector2
from constants import *

class PackMan(object):
    def __init__(self):
        self.__name = PACKMAN
        self.__position = Vector2(200, 400)
        hash_map = HashMap(5)
        hash_map.put(UP, Vector2(0, -1)) #TODO: Find a better way to do this
        hash_map.put(DOWN, Vector2(0, 1))
        hash_map.put(LEFT, Vector2(-1, 0))
        hash_map.put(RIGHT, Vector2(1, 0))
        hash_map.put(STOP, Vector2(0, 0))
        self.__directions = hash_map
        self.__direction = STOP
        self.__speed = 100
        self.__radius = 10
        self.__color = Colors.YELLOW

    def update(self, delta_time):
        self.__position += self.__directions.get(self.__direction) * self.__speed * delta_time
        direction = self.get_valid_key()
        self.__direction = direction

    def get_valid_key(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP] or key_pressed[K_w]:
            return UP
        if key_pressed[K_DOWN] or key_pressed[K_s]:
            return DOWN
        if key_pressed[K_LEFT] or key_pressed[K_a]:
            return LEFT
        if key_pressed[K_RIGHT] or key_pressed[K_d]:
            return RIGHT
        return STOP
    
    def render(self, screen):
        position = self.__position.asInt()
        pygame.draw.circle(screen, self.__color, position, self.__radius)


       
