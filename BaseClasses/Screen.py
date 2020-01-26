import pygame

from Tools.Constants import SIZE


class Screen:
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
        """Создание экрана"""
        surface = pygame.Surface(SIZE)
        self.sprites.draw(surface)
        return surface

    def notify_click(self, pos: tuple) -> None:
        """Обработка нажатия на sprite
        :param pos: Точка, куда нажали"""
        for sprite in self.sprites:
            if sprite.rect.collidepoint(pos):
                sprite.on_click()

    def update(self):
        """Обновление картинки на экране"""
        surface = self.create_surface()
        self.pending_updates()
        self.screen.blit(surface, (0, 0))

    def notify(self, event: pygame.event):
        """Получение события от Game"""
        pass

    def pending_updates(self):
        """Выполнение необходимых изменений"""
        pass
