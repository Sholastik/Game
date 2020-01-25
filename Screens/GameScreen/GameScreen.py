import pygame

from BaseClasses.Screen import Screen
from Tools.Constants import size


class GameScreen(Screen):
    @staticmethod
    def create_surface() -> pygame.Surface:
        return pygame.Surface(size)
