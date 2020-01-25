import pygame

from BaseClasses.Screen import Screen
from Screens.GameScreen.GameScreen import GameScreen
from Screens.StartScreen.BackgroundSprite import BackgroundSprite
from Screens.StartScreen.StartButtonSprite import StartButtonSprite
from Screens.StartScreen.TitleSprite import TitleSprite
from Tools.Tools import play_music, stop_music


class StartScreen(Screen):
    def __init__(self, screen: pygame.display, parent):
        sprites = pygame.sprite.Group(
            BackgroundSprite(self),
            StartButtonSprite(self),
            TitleSprite(self)
        )
        super().__init__(screen, parent, sprites)
        play_music("StartScreen/menu_music.mp3", loop=True)

    def load_game(self):
        """Загрузка игры"""
        stop_music()
        self.parent.change_screen(GameScreen(self.parent.screen, self.parent))
