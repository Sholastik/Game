from abc import ABC, abstractmethod

import pygame


class Screen(ABC):
    """Базовый класс экрана игры"""

    def __init__(self, screen: pygame.display, parent) -> None:
        """
        :param screen: Экран, на который выводится картинка
        :param parent: Класс-владелец экрана
        """
        self.screen = screen
        self.parent = parent
        self.sprites = list()

        surface = self.create_surface()
        screen.blit(surface, (0, 0))

    @staticmethod
    @abstractmethod
    def create_surface() -> pygame.Surface:
        pass

    def notify_click(self, pos: tuple) -> None:
        for sprite in self.sprites:
            if sprite.rect.collidepoint(pos):
                sprite.on_click()
