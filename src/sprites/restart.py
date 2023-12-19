from pygame import sprite, image
from ..utils.constants import *
from ..utils.colors import *


class Restart(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/sprites/restart.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = X_COORD_RESTART
        self.rect.y = Y_COORD_RESTART