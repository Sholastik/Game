from abc import ABC

import pygame

from Tools.Constants import size


class Screen(ABC):
    """Базовый класс экрана игры"""

    def __init__(self, screen: pygame.display, parent, sprites: pygame.sprite.Group) -> None:
        """
        :param screen: Экран, на который выводится картинка
        :param parent: Класс-владелец экрана
        """
        self.screen = screen
        self.parent = parent
        self.sprites = sprites

    def create_surface(self) -> pygame.Surface:
        surface = pygame.Surface(size)

        self.sprites.update()
        self.sprites.draw(surface)

        return surface

    def notify_click(self, pos: tuple) -> None:
        for sprite in self.sprites:
            if sprite.rect.collidepoint(pos):
                sprite.on_click()

    def update(self):
        surface = self.create_surface()
        self.screen.blit(surface, (0, 0))
