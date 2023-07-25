##############################################
# Description:
# * This file contains the abstract class for
#   all drawable objects.
##############################################

from abc import ABC, abstractmethod
import pygame

'''
Class: Drawable
'''
class Drawable(ABC):
    # Constructor
    def __init__(self, x, y, visibliity = True):
        self.__surface = pygame.display.get_surface()
        self.__x = self.__original_x = x
        self.__y = self.__original_y = y
        self.__visibliity = visibliity

    # Getters
    def get_x(self):
        return self.__x
    
    def get_original_x(self):
        return self.__original_x
    
    def get_y(self):
        return self.__y
    
    def get_original_y(self):
        return self.__original_y
    
    def get_visibility(self):
        return self.__visibliity
    
    # Setters
    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_visibility(self, visible):
        self.__visible = visible

    # Methods
    @abstractmethod
    def draw(self): 
        pass

    def get_rect(self):
        return self.__surface.get_rect().move(self.__x, self.__y)
