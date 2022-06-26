import pygame
import settings
from player import Player
from .abstract_powerup import Powerup


class AttackSpeedPowerup(Powerup):
    """
    Класс усиления скорострельности игрока.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Инициализатор класса"""

        super(AttackSpeedPowerup, self).__init__(*args, **kwargs)

        self.__skin = settings.attack_speed_powerup_skin
        self.image = pygame.transform.scale(
            self.__skin,
            (self._size, self._size),
        )
        self.image.set_colorkey(settings.Collors.BLACK.value)
        self.rect = self.image.get_rect(center=(self._pos_x, self._pos_y))

        self.__new_attack_speed = 100

    def influence(self, player: Player) -> None:
        """Воздействие усиления на игрока"""

        player.shoot_delay = self.__new_attack_speed
