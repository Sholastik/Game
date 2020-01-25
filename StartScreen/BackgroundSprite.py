from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite


class BackgroundSprite(Sprite):
    def __init__(self, parent: Screen) -> None:
        super(BackgroundSprite, self).__init__("StartScreen/bg.png", parent)

    def on_click(self) -> None:
        pass
