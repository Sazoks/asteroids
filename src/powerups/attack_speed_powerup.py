import pygame
from typing import Optional

import settings
from player import Player
from .abstract_powerup import Powerup


class AttackSpeedPowerup(Powerup):
    """
    Класс усиления скорострельности игрока.
    """

    __new_attack_speed = 100
    __skin = settings.attack_speed_powerup_skin

    def __init__(self, *args, **kwargs) -> None:
        """Инициализатор класса"""

        super(AttackSpeedPowerup, self).__init__(*args, **kwargs)

        self.image = pygame.transform.scale(
            self.__skin,
            (self._size, self._size),
        )
        self.image.set_colorkey(settings.Collors.BLACK.value)
        self.rect = self.image.get_rect(center=(self._pos_x, self._pos_y))

        self.__prev_value: Optional[int] = None

    def influence(self, player: Player) -> None:
        """Воздействие усиления на игрока"""

        # FIXME: Что, если на игрока как-то два раза повлияет усиление?
        #  В таком случае исходное значение затрется.
        self.__prev_value = player.shoot_delay
        player.shoot_delay = self.__new_attack_speed

    def rollback_param(self, player: Player) -> None:
        """Возврат предыдущего значения параметра у игрока"""

        if self.__prev_value is not None:
            player.shoot_delay = self.__prev_value
            self.__prev_value = None
