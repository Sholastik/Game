from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite


class Platform(Sprite):
    def __init__(self, path: str, parent: Screen, x, y):
        super().__init__("GameScreen/Platforms/" + path, parent)
        self.rect.left = x
        self.rect.top = 720 - y - self.rect.height

    def on_click(self) -> None:
        pass

    def update(self, delta):
        self.rect.left += delta
