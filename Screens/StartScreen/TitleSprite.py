from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite
from Tools.Constants import TITLE_PATH


class TitleSprite(Sprite):
    """Заголовок игры"""

    def __init__(self, parent: Screen) -> None:
        super(TitleSprite, self).__init__(TITLE_PATH, parent, left=640, top=160, center=True)
