"""Модуль класса глобальной точки доступа к игровым объектам"""

import pygame

import settings
from quadtree import Quadtree
from utils.singleton import Singleton
from utils.geometry import (
    Area,
    Point,
)
from powerups.active_powerups_manager import ActivePowerupsManager


class GlobalGameObjects(metaclass=Singleton):
    """
    Класс для хранения игровых объектов.

    Реализует паттерн Singleton. Предоставляет в проекте глобальную точку
    получения всех необходимых игровых объектов.

    Хранит в себе группы спрайтов, квадродерево и другие игровые объекты,
    к которым необходим доступ из любой точки программы.
    """

    def __init__(self) -> None:
        """Инициализатор класса"""

        # Создаем квадродерево.
        # Задаем начальный сектор и разброс поиска (в px).
        # Квадродерево необходимо для обнаружения столкновений объектов.
        self.__quadtree = Quadtree(
            area=Area(
                top_left=Point(0, 0),
                bottom_right=Point(settings.WIDTH, settings.HEIGHT),
            ),
            search_accuracy=50,
        )

        # Создаем группы объектов.
        # В них будут помещаться все игровые объекты.
        self.__players_group = pygame.sprite.Group()
        self.__bullets_group = pygame.sprite.Group()
        self.__asteroids_group = pygame.sprite.Group()
        self.__explosions_group = pygame.sprite.Group()
        self.__powerups_group = pygame.sprite.Group()

        # Менджер активных усилений.
        self.__active_powerups_manager = ActivePowerupsManager()

    @property
    def active_powerups_manager(self) -> ActivePowerupsManager:
        return self.__active_powerups_manager

    @property
    def quadtree(self) -> Quadtree:
        return self.__quadtree

    @property
    def players_group(self) -> pygame.sprite.Group:
        return self.__players_group

    @property
    def bullets_group(self) -> pygame.sprite.Group:
        return self.__bullets_group

    @property
    def asteroids_group(self) -> pygame.sprite.Group:
        return self.__asteroids_group

    @property
    def explosions_group(self) -> pygame.sprite.Group:
        return self.__explosions_group

    @property
    def powerups_group(self) -> pygame.sprite.Group:
        return self.__powerups_group
