import pygame

from player import Player
from powerups import Powerup
from global_game_objects import GlobalGameObjects
from .abstract_collide_resolve import AbstractCollideResolve


class PowerupPlayerCollideResolve(AbstractCollideResolve):
    """Класс решения столкновения усиления и игрока"""

    def __init__(self, powerup: Powerup, player: Player) -> None:
        """
        Инициализатор класса.

        :param powerup: Объект усиления.
        :param player: Объект игрока.
        """

        self.__powerup = powerup
        self.__player = player

    @staticmethod
    def get_object_types() -> tuple:
        """
        Геттер для получения имен классов объектов, столкновения
        которых может решать этот резолвер.

        :return:
            Кортеж имен классов объектов, которые могут сталкиваться.
        """

        return Powerup, Player

    def resolve(self) -> None:
        """Обработка столкновения объектов"""

        if pygame.sprite.collide_mask(self.__player, self.__powerup):
            self.__powerup.kill()
            GlobalGameObjects().quadtree.remove(self.__powerup)

            GlobalGameObjects().active_powerups_manager.add_powerup(
                player=self.__player,
                new_powerup=self.__powerup,
            )
