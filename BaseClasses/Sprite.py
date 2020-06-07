import pygame

from BaseClasses.Screen import Screen
from Tools.Tools import load_image


class Sprite(pygame.sprite.Sprite):
    """Базовый класс кастомного спрайта"""

    def __init__(self, path: str, parent: Screen, group: pygame.sprite.Group = None,
                 left: int = 0, top: int = 0, center: bool = False) -> None:
        """
        Создание кастомного sprite
        :param path: Путь до картинки
        :param parent: Класс-владелец спрайта
        :param group: Группа спрайта
        :param left: Смещение по горизонтальной оси относительно левого края экрана
        :param top: Смещение по вертикальной оси относительно верхнего края экрана
        :param center: Выровнять картинку с учетом её ширины/высоты
        """

        super().__init__(group or [])
        self.parent = parent
        self.image = load_image(path)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

        if center:
            self.rect.left -= self.rect.width // 2
            self.rect.top -= self.rect.height // 2

    def draw(self, screen: pygame.Surface) -> None:
        """Рисование sprite-а на экране"""
        screen.blit(self.image, self.rect)

    def on_click(self) -> None:
        """События нажатия на sprite"""
        pass
