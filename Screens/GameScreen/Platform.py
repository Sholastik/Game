from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite
from Tools.Constants import HEIGHT, PLATFORMS_PATH


class Platform(Sprite):
    """Sprite платформы"""
    def __init__(self, path: str, parent: Screen, x, y):
        super().__init__(f"{PLATFORMS_PATH}/{path}", parent)
        self.rect.left = x
        self.rect.top = HEIGHT - y - self.rect.height

    def update(self, delta):
        self.rect.left += delta
