import pygame

from BaseClasses.Screen import Screen
from Screens.GameScreen.GameScreen import GameScreen
from Screens.StartScreen.BackgroundSprite import BackgroundSprite
from Screens.StartScreen.StartButtonSprite import StartButtonSprite
from Screens.StartScreen.TitleSprite import TitleSprite
from Tools.Constants import size
from Tools.Tools import play_music, stop_music


class StartScreen(Screen):
    def __init__(self, screen: pygame.display, parent):
        super().__init__(screen, parent)
        play_music("StartScreen/menu_music.mp3", loop=True)

    def create_surface(self) -> pygame.Surface:
        surface = pygame.Surface(size)
        self.sprites = pygame.sprite.Group(
            BackgroundSprite(self),
            StartButtonSprite(self),
            TitleSprite(self)
        )

        for sprite in self.sprites:
            sprite.draw(surface)

        return surface

    def load_game(self):
        """Загрузка игры"""
        stop_music()
        self.parent.change_screen(GameScreen(self.parent.screen, self.parent))
