from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite


class BackgroundSprite(Sprite):
    def __init__(self, parent: Screen) -> None:
        super(BackgroundSprite, self).__init__("GameScreen/bg.png", parent)

    def on_click(self) -> None:
        pass

    def update(self, delta):
        self.rect.left += delta
        if self.rect.left <= -self.rect.width // 2:
            self.rect.left = 0
        if self.rect.left > 0:
            self.rect.left = -1280
