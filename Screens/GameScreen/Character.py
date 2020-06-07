import pygame

from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite
from Tools.Constants import *
from Tools.Tools import create_sound


class Character(Sprite):
    """Sprite персонажа"""

    def __init__(self, parent: Screen) -> None:
        super().__init__(f"{CHAR_PATH}/{RIGHT}/{IDLE}/0.png", parent, left=WIDTH // 2, top=HEIGHT // 2, center=True)

        # Начальное состояние анимации персонажа
        self.item = IDLE

        # Направление взгляда персонажа
        self.right = True

        # Номер кадра анимации
        self.frame = -1

        self.death_sound = create_sound(CHARACTER_DEATH_SOUND_PATH)
        self.sword_hit_sound = create_sound(SWORD_HIT_SOUND_PATH)

        # Предварительное вычисление маски для последующей быстрой проверки на пересечение
        self.mask = pygame.mask.from_surface(self.image)

    def update_image(self) -> None:
        """Обновление анимации"""
        if self.right:
            self.frame = (self.frame + 1) % len(CHAR_RIGHT[self.item])
            self.image = CHAR_RIGHT[self.item][self.frame]
        else:
            self.frame = (self.frame + 1) % len(CHAR_LEFT[self.item])
            self.image = CHAR_LEFT[self.item][self.frame]

    def update_pos(self, delta_y: int) -> None:
        """Перемещение по вертикали"""
        self.rect.top += delta_y

    def on_death(self) -> None:
        """События, происходящие при смерти"""
        self.death_sound.play()

    def play_sword_sound(self) -> None:
        """Проигрывание звука взмаха меча"""
        self.sword_hit_sound.play()
