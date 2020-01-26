from random import randint

import pygame

from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite
from Tools.Constants import ENEMIES_COUNT, ENEMY, ENEMY_PATH, PLATFORM_HEIGHT, HEIGHT, ENEMY_DEATH_SOUND


class Enemy(Sprite):
    """Sprite врага"""

    def __init__(self, x: int, y: int, parent: Screen) -> None:
        self.item = randint(0, ENEMIES_COUNT - 1)
        self.data = ENEMY[self.item]
        super().__init__(f"{ENEMY_PATH}/{self.item}/0.png", parent,
                         left=x, top=HEIGHT - y - PLATFORM_HEIGHT, center=True)
        self.rect.top -= self.rect.height // 3

        self.frame = -1
        self.mask = pygame.mask.from_surface(self.image)

    def update_image(self) -> None:
        """Обновление анимации врага"""
        self.frame = (self.frame + 0.5) % len(self.data)
        self.image = self.data[int(self.frame)]

    def update(self, delta_x: int) -> None:
        """Перемещение по горизонтали"""
        self.rect.left += delta_x

    def on_death(self):
        """События, происходящие при смерти"""
        ENEMY_DEATH_SOUND[self.item].play()
