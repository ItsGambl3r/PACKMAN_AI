import pygame

class SpriteSheet(object):
    '''Class representing a sprite sheet'''
    def __init__(self, file_name: str):
        """
        _summary_

        Args:
            file_name (str): _description_
        """
        self.sprite_sheet = pygame.image.load(file_name).convert()
    
    def get_image(self, x: int, y: int, width: int, height: int) -> pygame.Surface:
        '''Extracts an image from the spritesheet'''
        image = self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
        image.set_colorkey((0, 0, 0))
        return image