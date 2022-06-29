import pygame
from typing import Optional

import settings
from player import Player
from .abstract_powerup import Powerup


class HealthPowerup(Powerup):
    """Усиление здоровья игрока"""

    __add_health = 50
    __skin = settings.health_powerup_skin
    _time_action = 0

    def __init__(self, *args, **kwargs) -> None:
        """Инициализатор класса"""

        super(HealthPowerup, self).__init__(*args, **kwargs)

        self.image = pygame.transform.scale(
            self.__skin,
            (self._size, self._size),
        )
        self.image.set_colorkey(settings.Collors.BLACK.value)
        self.rect = self.image.get_rect(center=(self._pos_x, self._pos_y))

        self.__prev_value: Optional[int] = None

    def influence(self, player: Player) -> None:
        """
        Эффект, оказываемый на игрока.

        :param player: Объект игрока.
        """

        self._activate_time = pygame.time.get_ticks()
        lost_health = player.source_health - player.health
        if self.__add_health <= lost_health:
            player.health += self.__add_health
        else:
            player.health = player.source_health

    def rollback_param(self, player: Player) -> None:
        pass

    def get_time_action_color(self) -> settings.Collors:
        pass
