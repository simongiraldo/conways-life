from pygame import sprite, image


class VoidScreen(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load("./assets/sprites/initial_animation.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self._speed_alpha = 2
    
    def get_speed_alpha(self):
        return self._speed_alpha