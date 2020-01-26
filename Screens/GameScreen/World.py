from random import randint, choice

import pygame

from Screens.GameScreen.Platform import Platform
from Screens.GameScreen.Tree import Tree

FLOOR_MIDDLE = "floor_middle.png"
FLOOR_LEFT = "floor_left.png"
FLOOR_RIGHT = "floor_right.png"
WATER = "water.png"
MOUNTAIN = "mountain.png"
MOUNTAIN_LEFT = "mountain_left.png"
MOUNTAIN_RIGHT = "mountain_right.png"
ASSISTANCE = "edged.png"
DOUBLE_MIDDLE = "double_middle.png"
MIDDLE = "middle.png"
LEFT = "left.png"
DOUBLE_LEFT = "double_left.png"
RIGHT = "right.png"
DOUBLE_RIGHT = "double_right.png"


class World:
    def __init__(self) -> None:
        self.width = 200 + 20
        self.world = None
        self.next = [[[None, None] for _ in range(self.width)] for _ in range(5)]
        self.generate_mountains(self.next)
        self.generate_floor(self.next[0])
        self.generate_assistant_floor(self.next)
        self.generate_additional_floors(self.next)
        self.add_trees(self.next)
        self.platforms = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.change_layer()
        self.coord = 0

    def generate_floor(self, world) -> None:
        for i in range(randint(self.width // 10, self.width // 4)):
            pos = randint(10, self.width - 15)
            length = randint(1, max(2, min(self.width - pos - 15, 2)))
            if all(map(lambda x: x[0] is None, world[pos - 1:pos + length + 1])):
                for index in range(pos, pos + length):
                    world[index][0] = WATER

        for i in range(1, self.width - 1):
            if world[i][0] is None:
                prev = world[i - 1] == WATER
                next = world[i + 1] == WATER
                if prev ^ next:
                    if prev:
                        world[i][0] = FLOOR_RIGHT
                    else:
                        world[i][0] = FLOOR_LEFT
                else:
                    world[i][0] = FLOOR_MIDDLE
        world[0][0] = FLOOR_MIDDLE
        world[self.width - 1][0] = FLOOR_MIDDLE

    def generate_mountains(self, world) -> None:
        cnt = randint(4, 7)
        while cnt != 0:
            pos = randint(12, self.width - 18)
            length = randint(3, min(self.width - 13 - pos, 8))
            if all(map(lambda x: x[0] is None, world[2][pos - 1: pos + length + 1])):
                for index in range(pos, pos + length):
                    world[0][index][0] = world[1][index][0] = world[2][index][0] = MOUNTAIN
                    world[3][index][0] = FLOOR_MIDDLE
                world[3][pos - 1][0] = MOUNTAIN_LEFT
                world[3][pos + length][0] = MOUNTAIN_RIGHT
            else:
                cnt += 1
            cnt -= 1

    def generate_assistant_floor(self, world) -> None:
        add = True
        for i in range(0, self.width - 10):
            if add:
                if world[3][i][0] is not None:
                    world[2][i - 2][0] = ASSISTANCE
                    add = False
            elif world[3][i][0] is None:
                add = True

    def generate_additional_floors(self, world) -> None:
        for i in range(randint(40, 100)):
            layer = choice((1, 2, 4))
            pos = randint(11, self.width - 17 - 5)
            length = randint(2, 7)
            double = choice((True, False))
            if all(map(lambda x: x[0] is None, world[layer][pos - 1: pos + length + 1])) \
                    and all(map(lambda x: x[0] is None, world[layer - 1][pos - 1: pos + length + 1])):
                for index in range(pos, pos + length):
                    if double:
                        world[layer][index][0] = DOUBLE_MIDDLE
                    else:
                        world[layer][index][0] = MIDDLE
                if double:
                    world[layer][pos][0] = DOUBLE_LEFT
                    world[layer][pos + length][0] = DOUBLE_RIGHT
                else:
                    world[layer][pos][0] = LEFT
                    world[layer][pos + length][0] = RIGHT

    def add_trees(self, world):
        for i in range(5):
            for j in range(self.width):
                if world[i][j][0] not in (None, WATER, MOUNTAIN):
                    val = randint(1, 100)
                    if val >= 35:
                        world[i][j][1] = f"tree_{randint(2, 7 if i == 4 else 8)}.png"

    def change_layer(self):
        self.world = self.next
        self.next = [[[None, None] for _ in range(self.width)] for _ in range(6)]
        self.generate_mountains(self.next)
        self.generate_floor(self.next[0])
        self.generate_assistant_floor(self.next)
        self.generate_additional_floors(self.next)
        self.add_trees(self.next)
        self.create_sprites(self.world)
        self.coord = 0

    def create_sprites(self, world):
        self.platforms = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        for j in range(self.width):
            for i in range(5):
                if world[i][j][1] is not None:
                    self.platforms.add(Tree(world[i][j][1], None, j * 128, i * 128))
                if world[i][j][0] is not None:
                    if world[i][j][0] == WATER:
                        self.water.add(Platform(world[i][j][0], None, j * 128, i * 128))
                    else:
                        self.platforms.add(Platform(world[i][j][0], None, j * 128, i * 128))

    def update(self, delta):
        for sprite in self.platforms:
            sprite.update(delta)
        for sprite in self.water:
            sprite.update(delta)
        self.coord += delta
        if self.coord <= -(self.width - 10) * 128:
            self.change_layer()

    def draw(self, screen):
        for i in self.platforms:
            if i.rect.left <= 1280:
                i.draw(screen)
            else:
                break
        for i in self.water:
            if i.rect.left <= 1280:
                i.draw(screen)
            else:
                break

    def in_water(self, mask):
        for sprite in self.water:
            if sprite.rect.left > 1280:
                return False
            if pygame.sprite.collide_mask(mask, sprite):
                return True
        return False

    def should_fall(self, char):
        for sprite in self.platforms:
            if sprite.rect.left > 1280:
                break
            if sprite.rect.left < 0:
                continue
            if not (sprite.rect.left <= char.rect.left + 60 <= sprite.rect.left + sprite.rect.width):
                continue
            if type(sprite) is not Tree:
                if abs(sprite.rect.top - 64 - char.rect.top) <= 20:
                    return False
        return True

    def can_go_there(self, char, delta):
        for sprite in self.platforms:
            if sprite.rect.left > 1280:
                break
            if sprite.rect.left < 0 or type(sprite) is Tree:
                continue
            if delta > 0:
                if - sprite.rect.left - sprite.rect.width + char.rect.left + 60 <= delta \
                        and sprite.rect.top >= char.rect.top - 64 >= sprite.rect.top - sprite.rect.height \
                        and sprite.rect.left + sprite.rect.width <= char.rect.left + 60:
                    return False
            elif delta < 0:
                if char.rect.left + 60 - delta - sprite.rect.left >= 0 \
                        and sprite.rect.top >= char.rect.top - 64 >= sprite.rect.top - sprite.rect.height \
                        and sprite.rect.left >= char.rect.left:
                    return False
        return True
