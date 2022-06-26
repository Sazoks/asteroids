import pygame

import settings
from quadtree import Quadtree
from utils.singleton import Singleton
from utils.geometry import (
    Area,
    Point,
)


class GameObjects(metaclass=Singleton):
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
        self.__asteroids_sprites = pygame.sprite.Group()
        self.__explosions_sprites = pygame.sprite.Group()

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
    def asteroids_sprites(self) -> pygame.sprite.Group:
        return self.__asteroids_sprites

    @property
    def explosions_sprites(self) -> pygame.sprite.Group:
        return self.__explosions_sprites
