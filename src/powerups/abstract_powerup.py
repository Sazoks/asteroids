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

    def __init__(
            self,
            lifetime: int,
            time_action: int,
            pos_x: Optional[int] = None,
            pos_y: Optional[int] = None,
    ) -> None:
        """
        Инициализатор класса.

        :param lifetime: Время жизни усиления.
        :param time_action: Время действия усиления.
        :param pos_x: Координаты центра по оси X.
        :param pos_y: Координаты центра по оси Y.
        """

        pygame.sprite.Sprite.__init__(self)

        self._lifetime = lifetime
        self._time_action = time_action
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

    @abstractmethod
    def influence(self, player: Player) -> None:
        pass

    def update(self) -> None:
        """Метод обновления состояния усиления"""

        now = pygame.time.get_ticks()
        if now - self._start_time_live >= self._lifetime:
            self.kill()
        else:
            ...
