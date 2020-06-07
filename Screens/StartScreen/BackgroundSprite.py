from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite
from Tools.Constants import START_BACKGROUND_PATH


class BackgroundSprite(Sprite):
    """Sprite фоновой картинки в главном меню"""
    def __init__(self, parent: Screen) -> None:
        super(BackgroundSprite, self).__init__(START_BACKGROUND_PATH, parent)
