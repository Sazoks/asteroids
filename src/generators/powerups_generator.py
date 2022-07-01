import pygame
import random
from typing import Optional

from levels.abstract_managing_levels import ManagingLevels
from powerups import (
    Powerup,
    AttackSpeedPowerup,
    SpeedPowerup,
    HealthPowerup,
)


class PowerupsGenerator(ManagingLevels):
    """
    Класс генератора усилений.
    """

    __powerups_classes = [
        AttackSpeedPowerup,
        SpeedPowerup,
        HealthPowerup,
    ]

    def __init__(
            self,
            start_frequency: float,
            end_frequency: float,
            max_level: int,
    ) -> None:
        """
        Инициализатор класса.

        :param start_frequency: Начальная частота появления усилений.
        :param max_level: Максимальный уровень генератора.
        """

        self.__last_asteroid_spawn = pygame.time.get_ticks()

        self.__start_level = 0
        self.__max_level = max_level
        self.__current_level = 0

        self.__start_frequency = start_frequency
        self.__end_frequency = end_frequency
        self.__current_frequency = start_frequency
        self.__frequency_delta = start_frequency // max_level

    def generate(self) -> Optional[Powerup]:
        """Генерация усиления"""

        now = pygame.time.get_ticks()
        if now - self.__last_asteroid_spawn >= self.__current_frequency:
            self.__last_asteroid_spawn = now
            random_powerup = random.choice(self.__powerups_classes)()

            return random_powerup

    def get_current_level(self) -> int:
        return self.__current_level

    def level_up(self) -> None:
        """Повышение уровня"""

        if self.__current_level < self.__max_level:
            self.__current_level += 1
            if self.__current_frequency - self.__frequency_delta \
                    >= self.__end_frequency:
                self.__current_frequency -= self.__frequency_delta
            else:
                self.__current_frequency = self.__end_frequency

    def level_down(self) -> None:
        """Понижение уровня"""

        if self.__current_level > self.__start_level:
            self.__current_level -= 1
            if self.__current_frequency + self.__frequency_delta \
                    <= self.__start_frequency:
                self.__current_frequency += self.__frequency_delta
            else:
                self.__current_frequency = self.__start_frequency

    def reset_levels(self) -> None:
        """Сброс уровней"""

        self.__current_level = self.__start_level
        self.__current_frequency = self.__start_frequency
