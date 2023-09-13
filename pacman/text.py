import pygame, os
from constants import *
from vector import Vector2D

class Text(object):
    def __init__(self, text: str, position: tuple, font_size: int = 12, color: tuple = (255, 255, 255)):
        self.text = text
        self.position = Vector2D(*position)
        self.font = pygame.font.Font(os.path.join('pacman', 'assets', 'fonts', 'PressStart2P-Regular.ttf'), font_size)
        self.color = color
        self.is_visible = True

    def render(self, screen: pygame.Surface):
        '''Renders the text on the screen'''
        if self.is_visible:
            surface = self.font.render(self.text, True, self.color)
            rect = surface.get_rect(center=self.position.as_tuple())
            screen.blit(surface, rect)

class Score(Text):
    def __init__(self, position: tuple):
        super().__init__('SCORE', position, 20, (255, 255, 255))
        self.score = 0

    def add_points(self, points: int):
        '''Adds points to the score'''
        self.score += points
        self.text = f'SCORE: {self.score}'

    def update(self, score: int):
        '''Updates the score'''
        self.text = f'SCORE: {score}'

    def reset(self):
        '''Resets the score'''
        self.score = 0
        self.text = f'SCORE: {self.score}'
