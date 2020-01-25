import pygame

from BaseClasses.Screen import Screen
from StartScreen.BackgroundSprite import BackgroundSprite
from StartScreen.StartButtonSprite import StartButtonSprite
from Tools.Constants import size
from Tools.Tools import play_music, stop_music


class StartScreen(Screen):
    def __init__(self, screen: pygame.display, parent):
        super().__init__(screen, parent)
        play_music("StartScreen/menu_music.mp3", loop=True)

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
        stop_music()
