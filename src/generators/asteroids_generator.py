import pygame
import math
import random
from typing import (
    List,
    Optional,
)

from asteroids.asteroid import (
    Asteroid,
    AsteroidType,
)
from levels.abstract_managing_levels import ManagingLevels


class AsteroidsGenerator(ManagingLevels):
    """
    Класс для управления астероидами.

    Наследует абстрактный класс (интерфейс) ManagingLevels для изменения
    уровня генерации астероидов.
    """

    def __init__(
            self,
            start_frequency: float,
            end_frequency: float,
            asteroid_types: List[AsteroidType],
            max_level: int,
    ) -> None:
        """
        Инициализатор класса.

        :param start_frequency: Начальная частота появления астероидов.
        :param end_frequency: Конечная частота появления астероидов.
        :param asteroid_types:
            Типы астероидов. Количество элементов этого списка определяет
            количество уровней для генератора.
        :param max_level: Максимальный уровень генератора.
        """

        assert len(asteroid_types) != 0

        self.__last_asteroid_spawn = pygame.time.get_ticks()
        self.__start_frequency = start_frequency
        self.__end_frequency = end_frequency
        self.__current_frequency = start_frequency
        # Дельта частоты появления астероидов между уровнями будет одинаковая.
        self.__frequency_delta = start_frequency // max_level

        self.__start_level = 0
        self.__max_level = max_level
        self.__current_level = 0

        self.__asteroid_types = asteroid_types

    def generate(self) -> Optional[Asteroid]:
        """Генерация астероидов"""

        now = pygame.time.get_ticks()
        if now - self.__last_asteroid_spawn >= self.__current_frequency:
            self.__last_asteroid_spawn = now

            # Создаем астероид случайного типа.
            asteroid_type = random.choice(self.__asteroid_types)
            new_asteroid = asteroid_type.create_asteroid()

            return new_asteroid

    def get_current_level(self) -> int:
        return self.__current_level

    def level_up(self) -> None:
        """Повышения уровня"""

        if self.__current_level < self.__max_level:
            self.__current_level += 1
            # Понижаем задержку появления нового астероида. Т.е. повышаем
            # частоту появления астероидов. Это увеличит сложность игры,
            # что логично с повышением уровня.
            if self.__current_frequency - self.__frequency_delta \
                    >= self.__end_frequency:
                self.__current_frequency -= self.__frequency_delta
            else:
                self.__current_frequency = self.__end_frequency

    def level_down(self) -> None:
        """Понижение уровня"""

        # Если есть, куда понижать уровни.
        if self.__current_level > self.__start_level:
            self.__current_level -= 1
            # Меняем частоту появления астероидов.
            if self.__current_frequency + self.__frequency_delta \
                    <= self.__start_frequency:
                self.__current_frequency += self.__frequency_delta
            else:
                self.__current_frequency = self.__start_frequency

    def reset_levels(self) -> None:
        """Сброс уровней"""

        self.__current_frequency = self.__start_frequency
        self.__current_level = self.__start_level
