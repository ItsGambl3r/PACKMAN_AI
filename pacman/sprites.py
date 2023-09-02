import pygame

class SpriteSheet(object):
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()

    def get_image(self, x, y, width = 8, height = 8):
        image = self.sprite_sheet.subsurface((x, y, width, height))
        image = self.resize(image, 24, 24)
        image.set_colorkey((0, 0, 0))
        return image
    
    def resize(self, image, width = 24, height = 24):
        return pygame.transform.scale(image, (width, height))
