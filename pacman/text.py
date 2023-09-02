import pygame
import os
from constants import *
from vector import Vector2D

class Text(object):
    def __init__(self, text: str, position: tuple, font_size: int = 12, color: tuple = WHITE):
        self.text = text
        self.position = Vector2D(*position)
        self.font = pygame.font.Font(os.path.join('pacman', 'Assets', 'Fonts', 'PressStart2P-Regular.ttf'), font_size)
        self.color = color
        self.isVisible = True

    def render(self, screen):
        if self.isVisible:
            surface = self.font.render(self.text, True, self.color)
            rect = surface.get_rect(center=self.position.asTuple())
            screen.blit(surface, rect)

class Score(Text):
    def __init__(self, initial_score: int, position: tuple, font_size: int = 12, color: tuple = WHITE):
        super().__init__(str(initial_score), position, font_size, color)
        self.score = initial_score

    def addPoints(self, points: int):
        self.score += points
        self.text = str(self.score)

    def resetScore(self):
        self.score = 0
        self.text = str(self.score)