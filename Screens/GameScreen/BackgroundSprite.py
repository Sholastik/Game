from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite


class BackgroundSprite(Sprite):
    def __init__(self, parent: Screen) -> None:
        super(BackgroundSprite, self).__init__("GameScreen/bg.png", parent)

    def on_click(self) -> None:
        pass

    def update(self, right):
        if right:
            self.rect.left -= 8
        else:
            self.rect.left += 8
        if self.rect.left <= -self.rect.width // 2 or self.rect.left > 0:
            self.rect.left = 0
