import pygame
from typing import Optional

import settings
from player import Player
from .abstract_powerup import Powerup


class SpeedPowerup(Powerup):
    """Усиление дополнительной скорости"""

    __speed = 7
    __skin = settings.speed_powerup_skin

    def __init__(self, *args, **kwargs) -> None:
        """Инициализатор класса"""

        super(SpeedPowerup, self).__init__(*args, **kwargs)

        self.image = pygame.transform.scale(
            self.__skin,
            (self._size, self._size),
        )
        self.image.set_colorkey(settings.Collors.BLACK.value)
        self.rect = self.image.get_rect(center=(self._pos_x, self._pos_y))

        self.__prev_value: Optional[int] = None

    def influence(self, player: Player) -> None:
        """
        Эффект на игрока.

        :param player: Объект игрока.
        """

        self.__prev_value = player.speed
        player.speed = self.__speed

    def rollback_param(self, player: Player) -> None:
        """
        Возврат предыдущего значения парметра у игрока.

        :param player: Объект игрока.
        """

        if self.__prev_value is not None:
            player.speed = self.__prev_value
            self.__prev_value = None
