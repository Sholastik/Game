from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite


class TitleSprite(Sprite):
    def __init__(self, parent: Screen) -> None:
        super(TitleSprite, self).__init__("StartScreen/title.png", parent, left=640, top=160, center=True)

    def on_click(self) -> None:
        pass
