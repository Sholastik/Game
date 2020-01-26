from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite
from Tools.Constants import GAME_BACKGROUND_PATH


class BackgroundSprite(Sprite):
    """Sprite фоновой картинки"""
    def __init__(self, parent: Screen) -> None:
        super(BackgroundSprite, self).__init__(GAME_BACKGROUND_PATH, parent)

    def update(self, delta):
        """Зацикливание фонового изображения"""
        self.rect.left += delta
        if self.rect.left <= -self.rect.width // 2:
            self.rect.left = 0
        if self.rect.left > 0:
            self.rect.left = -self.rect.width
