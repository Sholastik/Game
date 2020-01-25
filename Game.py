import pygame

import BaseClasses.Screen
from StartScreen.StartScreen import StartScreen
from Tools.Constants import size
from Tools.Tools import create_sound


class Game:
    """Основной класс игры"""

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(size)
        pygame.init()
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        self.current_screen = StartScreen(self.screen, parent=self)
        self.click_sound = create_sound("click_sound.wav")

        self.loop()

    def change_screen(self, screen: BaseClasses.Screen) -> None:
        """Замена текущего экрана"""
        self.current_screen = screen

    def loop(self) -> None:
        """Обработка событий"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Делегация обработки события текущему экрану
                    self.click_sound.play()
                    self.current_screen.notify_click(event.pos)
            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
