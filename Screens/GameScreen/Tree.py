from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite
from Tools.Constants import HEIGHT, PLATFORM_HEIGHT, PLATFORMS_PATH


class Tree(Sprite):
    """Sprite дерева"""

    def __init__(self, path: str, parent: Screen, x: int, y: int) -> None:
        super().__init__(f"{PLATFORMS_PATH}/{path}", parent, left=x)
        self.rect.top = HEIGHT - y - self.rect.height - PLATFORM_HEIGHT

    def update(self, delta: int) -> None:
        self.rect.left += delta
