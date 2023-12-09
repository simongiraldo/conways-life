from pygame import sprite, image
from ..utils.constants import *
from ..utils.colors import *


class Click_banner(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/sprites/click_start.png").convert_alpha()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = X_COORD_CLICK_BANNER
        self.rect.y = Y_COORD_CLICK_BANNER
        self._speed_alpha = 4

    def get_speed_alpha(self):
        return self._speed_alpha

    def change_speed_alpha_sign(self):
        self._speed_alpha *= -1