from abc import ABC, abstractmethod

import pygame

from BaseClasses.Screen import Screen
from Tools.Tools import load_image


class Sprite(pygame.sprite.Sprite, ABC):
    """Базовый класс кастомного спрайта"""

    def __init__(self, path: str, parent: Screen, group: pygame.sprite.Group = None, left: int = 0, top: int = 0,
                 center: bool = False, transparent: bool = False) -> None:
        """
        Создание кастомного sprite
        :param path: Путь до картинки
        :param parent: Класс-владелец спрайта
        :param group: Группа спрайта
        :param left: Смещение по горизонтальной оси относительно левого края экрана
        :param top: Смещение по вертикальной оси относительно верхнего края экрана
        :param center: Выровнять картинку с учетом её ширины/высоты
        :param transparent: Прозрачность фона
        """

        super().__init__(group or [])
        self.parent = parent
        self.image = load_image(path, -1 if transparent else None)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

        if center:
            self.rect.left -= self.rect.width // 2
            self.rect.top -= self.rect.height // 2

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    @abstractmethod
    def on_click(self) -> None:
        pass
