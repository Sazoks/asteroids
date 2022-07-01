import pygame
import random
from abc import (
    ABC,
    abstractmethod,
)
from enum import (
    Enum,
    auto,
)
from typing import Optional

import settings
from player import Player
from collider.collideable import Collideable


class Powerup(Collideable, pygame.sprite.Sprite, ABC):
    """
    Абстрактный класс усиления для игрока.
    """

    class Status(Enum):
        """Статусы усиления"""

        ACTIVATED = auto()
        DEACTIVATED = auto()
        EXPIRED = auto()

    # Время жизни и время действия усиления.
    _lifetime = 10000
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

        # Начало жизни усиления.
        self._start_time_live = pygame.time.get_ticks()
        # Время активации усиления.
        self._activate_time: Optional[int] = None
        # Статус усиления.
        self._status = self.Status.DEACTIVATED

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


    @abstractmethod
    def influence(self, player: Player) -> None:
        pass

    @abstractmethod
    def rollback_param(self, player: Player) -> None:
        pass

    @abstractmethod
    def get_time_action_color(self) -> settings.Collors:
        pass

    def refresh(self) -> None:
        """Обновление времени действия усиления"""

        self._activate_time = pygame.time.get_ticks()

    def get_activate_time(self) -> Optional[int]:
        return self._activate_time

    @classmethod
    def get_lifetime(cls) -> int:
        return cls._lifetime

    @classmethod
    def get_time_action(cls) -> int:
        return cls._time_action

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, new_status: Status) -> None:
        self._status = new_status


    def update(self) -> None:
        """Метод обновления состояния усиления"""

        now = pygame.time.get_ticks()
        if now - self._start_time_live >= self.get_lifetime():
            self.kill()
        else:
            # FIXME: Убрать.
            ...
