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
        """Воздействие усиления на игрока"""

        # Если воздействия прежде не было, сохраняем исходное значение и
        # меняем статус усиления.
        if self._status == self.Status.DEACTIVATED:
            self.__prev_value = player.speed
            self._activate_time = pygame.time.get_ticks()
            self._status = self.Status.ACTIVATED
            player.speed = self.__speed

    def rollback_param(self, player: Player) -> None:
        """Возврат предыдущего значения параметра у игрока"""

        if self.__prev_value is not None:
            player.speed = self.__prev_value
            self.__prev_value = None
            self._activate_time = None
            self._status = self.Status.DEACTIVATED

    def get_time_action_color(self) -> settings.Collors:
        """
        Получение цвета усиления для отрисовки времени действия.

        :return: Цвет.
        """

        return settings.Collors.BLUE

