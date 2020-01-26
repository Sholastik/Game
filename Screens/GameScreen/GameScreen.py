import pygame

from BaseClasses.Screen import Screen
from Screens.GameScreen.BackgroundSprite import BackgroundSprite
from Screens.GameScreen.Character import Character
from Screens.GameScreen.World import World
from Tools.Constants import *
from Tools.Tools import play_music


class GameScreen(Screen):
    """Основной игровой экран"""

    def __init__(self, screen: pygame.display, parent) -> None:
        self.bg = BackgroundSprite(self)
        super().__init__(screen, parent, pygame.sprite.Group(self.bg))

        self.char = Character(self)
        self.world = World()

        # Игровые события
        self.state = {HORIZONTAL_MOVEMENT: None, FALLING: False, JUMP: 0, ATTACK: 0, MAIN_MENU: -1}

        # Блокировка событий
        self.locked = False

        play_music(GAME_MUSIC_PATH, loop=True)

    def notify(self, event: pygame.event) -> None:
        """Получение событий от Game"""

        # Проверяем, что события не заблокированы
        if self.locked:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.state[HORIZONTAL_MOVEMENT] = self.char.right = event.key == pygame.K_RIGHT
                self.char.item = RUN
            elif event.key == pygame.K_UP and self.state[JUMP] == 0 and not self.state[FALLING]:
                self.state[JUMP] = JUMP_DURATION
                self.char.item = RUN
            elif event.key == pygame.K_SPACE:
                self.state[ATTACK] = ATTACK_COUNT
                self.char.item = ATTACK
                self.char.play_sword_sound()
                self.state[HORIZONTAL_MOVEMENT] = None
            else:
                return
            self.char.frame = -1
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.state[HORIZONTAL_MOVEMENT] = None

    def back_to_menu(self):
        """Возврат в главное меню"""
        self.parent.back_to_menu()

    def pending_updates(self) -> None:
        """Выполнение необходимых изменений"""

        # Обновляем таймер возврата в главное меню
        if self.state[MAIN_MENU] > 0:
            self.state[MAIN_MENU] -= 1
        # Возврат в главное меню
        if self.state[MAIN_MENU] == 0:
            self.back_to_menu()

        # Проверяем, что события не заблокированы
        if not self.locked:
            self.world.update_enemies()
            if self.state[HORIZONTAL_MOVEMENT] is not None:
                delta = RUN_SPEED
                if self.state[HORIZONTAL_MOVEMENT]:
                    delta = -delta

                # Если можем идти в данном направлении, то сдвигаем мир и фон
                if self.world.can_go_there(self.char, delta):
                    self.bg.update(delta)
                    self.world.update(delta)

            # Проверяем отсутствие опоры под персонажем
            self.state[FALLING] = self.world.should_fall(self.char)

            if self.state[JUMP] > 0:
                # Перемещаем персонажа
                self.state[JUMP] -= 1
                self.char.update_pos(self.state[JUMP] * JUMP_ACCELERATION)

            elif self.state[FALLING]:
                self.char.update_pos(FALLING_SPEED)

            # Если персонаж не двигается
            elif self.state[HORIZONTAL_MOVEMENT] is None and self.state[ATTACK] == 0:
                self.char.item = IDLE

            if self.state[ATTACK] > 0:
                self.world.kill_enemies(self.char)
                self.state[ATTACK] -= 1

            self.check_character()

        # Обновляем анимацию
        self.char.update_image()

    def check_character(self) -> None:
        """Проверка на то, что персонаж в воде или убит врагом"""
        if self.world.in_water(self.char) or self.world.is_killed_by_enemies(self.char):
            # Блокируем события и меняем анимацию, возвращаем игрока в главное меню
            self.locked = True
            self.char.on_death()
            self.char.item = DIED
            self.char.frame = -1
            self.state[MAIN_MENU] = TIME_BEFORE_MENU

    def create_surface(self) -> pygame.Surface:
        """Создание экрана"""
        surface = pygame.Surface(SIZE)

        self.sprites.draw(surface)
        self.world.draw(surface)
        self.char.draw(surface)

        return surface
