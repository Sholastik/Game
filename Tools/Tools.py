import os

import pygame


def load_image(name, color_key=None) -> pygame.image:
    """
    Загрузка картинки
    :param name: Путь до картинки в папке Assets
    :param color_key: Фоновый цвет / -1 для прозрачности
    """
    fullname = os.path.join('Assets', name)
    image = pygame.image.load(fullname).convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    return image
