import pygame
from typing import Optional

import settings
from player import Player
from .abstract_powerup import Powerup


class AttackSpeedPowerup(Powerup):
    """
    Класс усиления скорострельности игрока.
    """

    __attack_speed = 100
    __damage = 50
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

        self.__prev_attack_speed: Optional[int] = None
        self.__prev_damage: Optional[int] = None

    def influence(self, player: Player) -> None:
        """Воздействие усиления на игрока"""

        # Если воздействия прежде не было, сохраняем исходное значение и
        # меняем статус усиления.
        if self._status == self.Status.DEACTIVATED:
            self.__prev_attack_speed = player.shoot_delay
            self.__prev_damage = player.damage
            self._activate_time = pygame.time.get_ticks()
            self._status = self.Status.ACTIVATED
            player.shoot_delay = self.__attack_speed
            player.damage = self.__damage

    def rollback_param(self, player: Player) -> None:
        """Возврат предыдущего значения параметра у игрока"""

        if self.__prev_attack_speed is not None \
                and self.__prev_damage is not None:
            player.shoot_delay = self.__prev_attack_speed
            player.damage = self.__prev_damage
            self.__prev_damage = None
            self.__prev_attack_speed = None
            self._activate_time = None
            self._status = self.Status.DEACTIVATED

    def get_time_action_color(self) -> settings.Collors:
        """
        Получение цвета усиления для отрисовки времени действия.

        :return: Цвет.
        """

        return settings.Collors.YELLOW
