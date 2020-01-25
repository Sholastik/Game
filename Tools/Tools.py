import os

import pygame


def load_image(name: str, color_key=None) -> pygame.image:
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


def play_music(name: str, loop: bool = False) -> None:
    """
    Проигрывание музыки
    :param name: Путь до музыки в папке Assets
    :param loop: Бесконечное проигрывание
    """
    fullname = os.path.join('Assets', name)
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.set_volume(0.03)
    pygame.mixer.music.play(-1 if loop else 0)


def stop_music() -> None:
    pygame.mixer.music.stop()


def create_sound(name: str) -> pygame.mixer.Sound:
    """
    Создание звука
    :param name: путь до звука
    """
    fullname = os.path.join('Assets', name)
    return pygame.mixer.Sound(fullname)
