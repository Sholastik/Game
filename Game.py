import pygame

import BaseClasses.Screen
from Screens.StartScreen.StartScreen import StartScreen
from Tools.Constants import *
from Tools.Tools import create_sound, load_image


class Game:
    """Основной класс игры"""

    def __init__(self) -> None:
        """Инициализация игры, загрузка необходимых файлов"""
        pygame.init()

        # Подавление предупреждения
        self.click_sound = self.current_screen = None
        self.screen = pygame.display.set_mode(SIZE)

        self.current_screen = StartScreen(self.screen, parent=self)
        self.click_sound = create_sound(CLICK_SOUND_PATH)
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)

        self.load_char_images(ATTACK, ATTACK_COUNT)
        self.load_char_images(RUN, RUN_COUNT)
        self.load_char_images(IDLE, IDLE_COUNT)
        self.load_char_images(DIED, DIED_COUNT)

        self.loop()

    @staticmethod
    def load_char_images(token: str, count: int) -> None:
        """Загрузка анимаций персонажа"""
        for index in range(count):
            CHAR_LEFT[token].append(load_image(f"{CHAR_PATH}/{LEFT}/{token}/{index}.png"))
            CHAR_RIGHT[token].append(load_image(f"{CHAR_PATH}/{RIGHT}/{token}/{index}.png"))

    def change_screen(self, screen: BaseClasses.Screen) -> None:
        """Замена текущего экрана"""
        self.current_screen = screen

    def loop(self) -> None:
        """Обработка событий"""
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Делегация обработки события текущему экрану
                    self.click_sound.play()
                    self.current_screen.notify_click(event.pos)
                else:
                    self.current_screen.notify(event)
            self.current_screen.update()
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
