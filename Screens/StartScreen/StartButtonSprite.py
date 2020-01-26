from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite
from Tools.Constants import START_BUTTON_PATH


class StartButtonSprite(Sprite):
    """Кнопка начать игру"""

    def __init__(self, parent: Screen) -> None:
        super(StartButtonSprite, self).__init__(START_BUTTON_PATH, parent, left=640, top=480, center=True)

    def on_click(self) -> None:
        self.parent.load_game()
