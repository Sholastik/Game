from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite
from Tools.Constants import *


class Character(Sprite):
    """Sprite персонажа"""

    def __init__(self, parent: Screen):
        super().__init__(f"{CHAR_PATH}/{RIGHT}/{IDLE}/0.png", parent, left=WIDTH // 2, top=HEIGHT // 2, center=True)
        self.item = IDLE
        self.right = True
        self.frame = -1

    def update_image(self):
        """Обновление анимации"""
        if self.right:
            self.frame = (self.frame + 1) % len(CHAR_RIGHT[self.item])
            self.image = CHAR_RIGHT[self.item][self.frame]
        else:
            self.frame = (self.frame + 1) % len(CHAR_LEFT[self.item])
            self.image = CHAR_LEFT[self.item][self.frame]

    def update_pos(self, delta_y):
        """Перемещение по вертикали"""
        self.rect.top += delta_y
