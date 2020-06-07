import pygame

from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite
from Tools.Constants import HEIGHT, PLATFORMS_PATH


class Platform(Sprite):
    """Sprite платформы"""

    def __init__(self, path: str, parent: Screen, x: int, y: int) -> None:
        super().__init__(f"{PLATFORMS_PATH}/{path}", parent, left=x)
        self.rect.top = HEIGHT - y - self.rect.height
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta: int) -> None:
        """Перемещение по горизонтали"""
        self.rect.left += delta
