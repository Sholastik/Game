from random import randint, choice

import pygame

from BaseClasses.Sprite import Sprite
from Screens.GameScreen.Enemy import Enemy
from Screens.GameScreen.Platform import Platform
from Screens.GameScreen.Tree import Tree
from Tools.Constants import *


class World:
    """Класс, управляющий игровым миром"""

    def __init__(self) -> None:
        self.world = None
        self.coord = 0
        self.next = [[[None, None] for _ in range(LEVEL_WIDTH)] for _ in range(5)]

        self.platforms = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.generate_world()
        self.change_layer()

    def generate_world(self) -> None:
        """Генерация игровых обьектов"""
        self.generate_mountains(self.next)
        self.generate_floor(self.next[0])
        self.generate_assistant_floor(self.next)
        self.generate_additional_floors(self.next)
        self.add_trees(self.next)
        self.coord = 0

    @staticmethod
    def generate_floor(world: list) -> None:
        """Генерация самого нижнего уровня"""

        # Заполнение водой
        for i in range(randint(MIN_WATER_COUNT, MAX_WATER_COUNT)):
            pos = randint(PROTECTED_LEFT, LEVEL_WIDTH - PROTECTED_RIGHT)

            length = randint(MIN_WATER_LENGTH,
                             max(MIN_WATER_LENGTH,
                                 min(LEVEL_WIDTH - pos - PROTECTED_RIGHT, MAX_WATER_LENGTH)
                                 )
                             )

            # Проверка что выбранные клетки не заняты
            if all(map(lambda x: x[0] is None, world[pos - 1:pos + length + 1])):
                for index in range(pos, pos + length):
                    world[index][0] = WATER_PATH

        # Заполнение оставшихся клеток платформами
        for i in range(1, LEVEL_WIDTH - 1):
            if world[i][0] is None:
                # Проверяем, нужно ли выбрать платформу с гладкими углами
                prev_cell = world[i - 1] == WATER_PATH
                next_cell = world[i + 1] == WATER_PATH

                if prev_cell ^ next_cell:
                    if prev_cell:
                        world[i][0] = FLOOR_RIGHT_PATH
                    else:
                        world[i][0] = FLOOR_LEFT_PATH
                else:
                    world[i][0] = FLOOR_MIDDLE_PATH

        # Первая и последняя платформа должна быть без углов
        world[0][0] = FLOOR_MIDDLE_PATH
        world[LEVEL_WIDTH - 1][0] = FLOOR_MIDDLE_PATH

    @staticmethod
    def generate_mountains(world: list) -> None:
        """Генерация гор"""

        cnt = randint(MIN_MOUNTAINS_COUNT, MAX_MOUNTAINS_COUNT)
        while cnt != 0:
            pos = randint(PROTECTED_LEFT + MIN_MOUNTAINS_COUNT,
                          LEVEL_WIDTH - PROTECTED_RIGHT - MIN_MOUNTAINS_LENGTH)

            length = randint(MIN_MOUNTAINS_COUNT,
                             min(LEVEL_WIDTH - PROTECTED_RIGHT - pos + 1, MAX_MOUNTAINS_COUNT)
                             )

            # Проверка, что клетки не заняты
            if all(map(lambda x: x[0] is None, world[MOUNTAINS_HEIGHT - 1][pos - 1: pos + length + 1])):
                for index in range(pos, pos + length):
                    for layer in range(MOUNTAINS_HEIGHT):
                        world[layer][index][0] = MOUNTAIN_PATH
                    world[MOUNTAINS_HEIGHT][index][0] = FLOOR_MIDDLE_PATH

                # Добавление платформ с углами
                world[MOUNTAINS_HEIGHT][pos - 1][0] = MOUNTAIN_LEFT_PATH
                world[MOUNTAINS_HEIGHT][pos + length][0] = MOUNTAIN_RIGHT_PATH
                cnt -= 1

    @staticmethod
    def generate_assistant_floor(world: list) -> None:
        """Генерация платформ, помогающих взобраться на гору"""

        add = True
        for i in range(0, LEVEL_WIDTH - PROTECTED_RIGHT):
            # Если добавили одну вспомогательную платформу, то больше не нужно
            if add:
                if world[MOUNTAINS_HEIGHT][i][0] is not None:
                    world[MOUNTAINS_HEIGHT - 1][i - 2][0] = ASSISTANCE_PATH
                    add = False
            elif world[MOUNTAINS_HEIGHT][i][0] is None:
                add = True

    @staticmethod
    def generate_additional_floors(world: list) -> None:
        """Генерация дополнительных платформ"""

        for i in range(randint(MIN_ADDITIONAL_FLOORS_COUNT, MAX_ADDITIONAL_FLOORS_COUNT)):
            layer = choice(AVAILABLE_FOR_ADDITIONAL_FLOOR)
            pos = randint(PROTECTED_LEFT + 1, LEVEL_WIDTH - PROTECTED_RIGHT - MAX_ADDITIONAL_FLOORS_LENGTH)
            length = randint(MIN_ADDITIONAL_FLOORS_LENGTH, MAX_ADDITIONAL_FLOORS_LENGTH)

            # Выбор из сдвоенной/обычной платформы-полублока
            double = choice((True, False))

            # Проверка, что клетки не заняты
            if all(map(lambda x: x[0] is None, world[layer][pos - 1: pos + length + 1])) \
                    and all(map(lambda x: x[0] is None, world[layer - 1][pos - 1: pos + length + 1])):

                for index in range(pos, pos + length):
                    if double:
                        world[layer][index][0] = DOUBLE_MIDDLE_PATH
                    else:
                        world[layer][index][0] = MIDDLE_PATH

                # Добавление платформ с углами
                if double:
                    world[layer][pos][0] = DOUBLE_LEFT_PATH
                    world[layer][pos + length][0] = DOUBLE_RIGHT_PATH
                else:
                    world[layer][pos][0] = LEFT_PATH
                    world[layer][pos + length][0] = RIGHT_PATH

    def generate_enemies(self, world: list) -> None:
        """Генерация врагов"""
        for j in range(PROTECTED_LEFT, LEVEL_WIDTH - PROTECTED_RIGHT):
            for i in range(LEVEL_HEIGHT - 1):
                if world[i][j][0] not in (None, WATER_PATH, MOUNTAIN_PATH):
                    val = randint(1, 100)
                    if val <= ENEMY_CHANCE:
                        enemy = Enemy(PLATFORM_WIDTH * j, PLATFORM_HEIGHT * i, None)
                        self.enemies.add(enemy)

    @staticmethod
    def add_trees(world: list) -> None:
        """Добавление декораций"""

        for i in range(LEVEL_HEIGHT):
            for j in range(LEVEL_WIDTH):
                if world[i][j][0] not in (None, WATER_PATH, MOUNTAIN_PATH):
                    val = randint(1, 100)
                    if val <= TREE_POSSIBILITY:
                        world[i][j][1] = TREE_FORMAT.format(randint(MIN_TREE, MAX_TREE))

    def change_layer(self) -> None:
        """Замена прошлого сегмента уровня на следующий сегмент"""
        self.world = self.next
        self.next = [[[None, None] for _ in range(LEVEL_WIDTH)] for _ in range(LEVEL_HEIGHT)]
        self.generate_world()
        self.create_sprites(self.world)
        self.generate_enemies(self.next)

    def create_sprites(self, world: list) -> None:
        """Создание sprite-ов"""
        self.platforms = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()

        for j in range(LEVEL_WIDTH):
            for i in range(LEVEL_HEIGHT):
                x = j * PLATFORM_WIDTH
                y = i * PLATFORM_HEIGHT
                if world[i][j][1] is not None:
                    self.trees.add(Tree(world[i][j][1], None, x, y))
                if world[i][j][0] is not None:
                    if world[i][j][0] == WATER_PATH:
                        self.water.add(Platform(world[i][j][0], None, x, y))
                    else:
                        self.platforms.add(Platform(world[i][j][0], None, x, y))

    def update(self, delta: int) -> None:
        """Передвижение sprite-ов"""

        self.platforms.update(delta)
        self.water.update(delta)
        self.trees.update(delta)
        self.enemies.update(delta)

        # Обновляем сдивг относительно начала
        self.coord += delta

        # Проверяем, нужно ли заменить сегмент мира на новый
        if self.coord <= -(LEVEL_WIDTH - PROTECTED_RIGHT) * PLATFORM_WIDTH:
            self.change_layer()

    def update_enemies(self, y: int) -> None:
        """Обновление координат врагов"""
        for sprite in self.enemies:
            if sprite.rect.left < 0:
                continue
            if sprite.rect.left > WIDTH:
                break
            if abs(WIDTH // 2 - sprite.rect.right) >= INFELICITY:
                delta_x = -ENEMY_SPEED
                if sprite.rect.right < WIDTH // 2:
                    delta_x = -delta_x
                sprite.rect.left += delta_x
            if abs(y - sprite.rect.right) >= INFELICITY:
                delta_y = -ENEMY_SPEED // 2
                if sprite.rect.top < y:
                    delta_y = -delta_y
                sprite.rect.top += delta_y
            sprite.update_image()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Рисование sprite-ов
        Рисуются только те, которые сейчас видны на экране
        """
        self.draw_group(self.platforms, screen)
        self.draw_group(self.water, screen)
        self.draw_group(self.trees, screen)
        self.draw_group(self.enemies, screen)

    @staticmethod
    def draw_group(group: pygame.sprite.Group, screen: pygame.Surface) -> None:
        """Отрисовка группы видимых sprite-ов"""
        for sprite in group:
            if sprite.rect.left < -PLATFORM_WIDTH:
                continue
            if sprite.rect.left <= WIDTH:
                sprite.draw(screen)
            else:
                break

    def in_water(self, char: Sprite) -> bool:
        """Проверка на то, что игрок попал в воду"""
        for sprite in self.water:
            if sprite.rect.left < -PLATFORM_WIDTH:
                continue
            if sprite.rect.left > WIDTH:
                break
            if pygame.sprite.collide_mask(char, sprite):
                return True
        return False

    def should_fall(self, char: Sprite) -> bool:
        """Проверка на отсутствие платформы под игроком"""
        for sprite in self.platforms:
            if sprite.rect.left < 0:
                continue
            if sprite.rect.left > WIDTH:
                break
            # Проверяем, что игрок в пределах платформы по оси OX
            if sprite.rect.left <= char.rect.left + char.rect.width // 2 <= sprite.rect.right:
                # Проверяем, что игрок в пределах платформы по оси OY
                if abs(sprite.rect.top - char.rect.height // 2 - char.rect.top) <= INFELICITY:
                    return False
        return True

    def can_go_there(self, char: Sprite, delta: int, enemy: bool = False) -> bool:
        """Проверка на возможность прохода в заданном направлении"""
        for sprite in self.platforms:
            if sprite.rect.left < 0:
                continue
            if sprite.rect.left > WIDTH:
                break

            char_horizontal_middle = char.rect.left + char.rect.width // 2
            char_vertical_middle = char.rect.top - char.rect.height // 2

            if self.coord >= 0 and delta > 0 and not enemy:
                return False

            # Проверяем, что персонаж на уровне платформы
            if not -sprite.rect.height <= char_vertical_middle - sprite.rect.top <= 0 and not enemy:
                continue

            # Если игрок идет назад
            if delta > 0:
                # Если сзади мира нет

                # Проверка на то, что перед нами нет блока
                if delta >= char_horizontal_middle - sprite.rect.right >= 0:
                    return False

            # Если игрок идет вперед
            elif delta < 0:
                # Проверка на то, что перед нами нет блока
                if char_horizontal_middle - delta >= sprite.rect.left >= char.rect.left:
                    return False
        return True

    def kill_enemies(self, char: Sprite) -> None:
        """Убиваем врагов, попавших в прямоугольник пересечения"""
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(enemy, char):
                enemy.kill()
                enemy.on_death()

    def is_killed_by_enemies(self, char: Sprite) -> bool:
        """Игрок умирает, если маска врага пересекла маску игрока"""
        for enemy in self.enemies:
            if pygame.sprite.collide_mask(enemy, char):
                return True
        return False
