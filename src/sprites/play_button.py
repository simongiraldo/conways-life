from pygame import sprite, image
from ..utils.colors import *


class PlayButton(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/sprites/play_button.png").convert_alpha()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50