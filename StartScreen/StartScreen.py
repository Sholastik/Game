import pygame

from BaseClasses.Screen import Screen
from StartScreen.BackgroundSprite import BackgroundSprite
from StartScreen.StartButtonSprite import StartButtonSprite
from Tools.Constants import size


class StartScreen(Screen):
    def create_surface(self) -> pygame.Surface:
        surface = pygame.Surface(size)
        self.sprites = pygame.sprite.Group(StartButtonSprite(self))

        bg = BackgroundSprite(self)
        bg.draw(surface)

        for sprite in self.sprites:
            sprite.draw(surface)

        return surface

    def load_game(self):
        """Загрузка игры"""
        pass
