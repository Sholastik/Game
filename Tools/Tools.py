import os

import pygame

from Tools.Constants import ASSETS_PATH, VOLUME


def get_path(path: str) -> str:
    """Получение пути до файла
    param path: Путь до картинки в папке Assets
    """
    return os.path.join(ASSETS_PATH, path)


def load_image(path: str) -> pygame.image:
    """
    Загрузка картинки
    :param path: Путь до картинки в папке Assets
    """
    fullname = get_path(path)
    image = pygame.image.load(fullname).convert_alpha()

    return image


def play_music(name: str, loop: bool = False) -> None:
    """
    Проигрывание музыки
    :param name: Путь до музыки в папке Assets
    :param loop: Бесконечное проигрывание
    """
    fullname = get_path(name)
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.set_volume(VOLUME)
    pygame.mixer.music.play(-1 if loop else 0)


def stop_music() -> None:
    """Остановка всей проигрываемой музыки"""
    pygame.mixer.music.stop()


def create_sound(path: str) -> pygame.mixer.Sound:
    """
    Создание звука
    :param path: путь до звука
    """
    fullname = get_path(path)
    return pygame.mixer.Sound(fullname)
