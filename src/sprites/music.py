from pygame import sprite, image
from ..utils.constants import *
from ..utils.colors import *


class Music(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/sprites/music.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = X_COORD_MUSIC
        self.rect.y = Y_COORD_MUSIC