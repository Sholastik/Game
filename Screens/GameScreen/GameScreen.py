import pygame

from BaseClasses.Screen import Screen
from Screens.GameScreen.BackgroundSprite import BackgroundSprite


class GameScreen(Screen):
    def __init__(self, screen: pygame.display, parent):
        sprites = pygame.sprite.Group(
            BackgroundSprite(self),
        )
        super().__init__(screen, parent, sprites)
