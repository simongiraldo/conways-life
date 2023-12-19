from pygame import sprite, image
from ..utils.constants import *
from ..utils.colors import *


class Play(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/sprites/play.png").convert_alpha()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = X_COORD_PLAY
        self.rect.y = Y_COORD_PLAY