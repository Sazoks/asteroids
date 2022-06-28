import pygame
import random
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Optional,
)

import settings
from player import Player


class Powerup(pygame.sprite.Sprite, ABC):
    """
    Абстрактный класс усиления для игрока.
    """

    _lifetime = 5000
    _time_action = 5000

    def __init__(
            self,
            pos_x: Optional[int] = None,
            pos_y: Optional[int] = None,
    ) -> None:
        """
        Инициализатор класса.

        :param pos_x: Координаты центра по оси X.
        :param pos_y: Координаты центра по оси Y.
        """

        pygame.sprite.Sprite.__init__(self)

        self._start_time_live = pygame.time.get_ticks()

        # Ширина и высота спрайта усиления, объекты спрайтов.
        self._size = 30

        # Позиция центра спрайта по оси Х.
        self._pos_x = random.randint(
            self._size // 2,
            settings.WIDTH - self._size // 2,
        ) if pos_x is None else pos_x

        # Позиция центра спрайта по оси Y.
        self._pos_y = random.randint(
            self._size // 2,
            settings.HEIGHT - self._size // 2,
        ) if pos_y is None else pos_y

        # Время активации усиления.
        self._activate_time: Optional[int] = None

    @abstractmethod
    def influence(self, player: Player) -> None:
        pass

    @abstractmethod
    def rollback_param(self, player: Player) -> None:
        pass

    def activate(self) -> None:
        """Активация усиления"""

        self._activate_time = pygame.time.get_ticks()

    def activated(self) -> bool:
        """Статус усиления"""

        return self._activate_time is not None

    def get_activate_time(self) -> Optional[int]:
        return self._activate_time

    @classmethod
    def get_lifetime(cls) -> int:
        return cls._lifetime

    @classmethod
    def get_time_action(cls) -> int:
        return cls._time_action

    def update(self) -> None:
        """Метод обновления состояния усиления"""

        now = pygame.time.get_ticks()
        if now - self._start_time_live >= self.get_lifetime():
            self.kill()
        else:
            ...
