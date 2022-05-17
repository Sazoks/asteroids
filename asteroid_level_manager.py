import pygame
import math
import random
from typing import (
    List,
    Optional,
)

from asteroid import (
    Asteroid,
    AsteroidType,
)


class AsteroidLevelManager:
    """Класс для управления астероидами"""

    def __init__(self,
                 start_frequency: float,
                 frequency_delta: float,
                 asteroid_types: List[AsteroidType],
                 score_levels: List[int]) -> None:
        """
        Инициализатор класса.

        :param start_frequency: Начальное значение частоты появления астероидов.
        :param end_frequency: Конечное значение частоты появления астероидов.
        :param frequency_delta: Изменения частоты появления с каждым уровнем.
        :param start_probability: Начальное значение коэфф. распределения Пуассона.
        :param end_probability: Конечное значение коэфф распределения Пуассона.
        :param probability_delta: Коэффициент изменения встречаемости астероидов.
        :param asteroid_types: Типы астероидов.
        """

        assert len(asteroid_types) != 0
        assert len(score_levels) != 0

        self.__last_asteroid_spawn = pygame.time.get_ticks()
        self.__start_frequency = start_frequency
        self.__current_frequency = start_frequency
        self.__frequency_delta = frequency_delta

        self.__start_probability = 1
        self.__end_probability = len(asteroid_types)
        self.__current_probability = 1

        self.__asteroid_types = asteroid_types
        self.__score_levels = score_levels
        self.__index_current_level = 0

        # Список встречаемостей астероидов разных типов.
        self.__asteroid_probabilities = self._generate_probabilities(
            len(asteroid_types),
            self.__start_probability,
        )

    def start(self) -> Optional[Asteroid]:
        """Генерация астероидов"""

        now = pygame.time.get_ticks()
        if now - self.__last_asteroid_spawn > self.__current_frequency:
            self.__last_asteroid_spawn = now

            # Выбираем случайным образом с учетом вероятности тип астероида,
            # который хотим создать. Вероятность появления = вес.
            asteroid_type_index = random.choices(
                population=[i for i in range(len(self.__asteroid_types))],
                weights=self.__asteroid_probabilities,
                k=len(self.__asteroid_types),
            )[0]

            # Выбираем нужный тип астероида
            asteroid_type = self.__asteroid_types[asteroid_type_index]
            # Создаем астероид нужного типа.
            new_asteroid = asteroid_type.create_asteroid()

            return new_asteroid

    @staticmethod
    def _generate_probabilities(length: int, k: float = 1.0) -> List[float]:
        """
        Генерация вероятностей появления астероидов каждого типа
        по распределению Пуассона.

        Чем больше мы увеличиваем k, тем больше центр распределения смещается
        в право, а значит тем больше вероятность появления у больших астероидов
        и тем меньше вероятность появления у меньших астероидов.

        :param length: Количество элементов.
        :param k: Коэффициент для смещения среднего значения.
        :return: Список вероятностей появления для каждого типа астероида.
        """

        probabilities: List[float] = []
        for i in range(1, length + 1):
            new_probability = (i ** k * math.e ** (-i)) / math.factorial(k)
            probabilities.append(new_probability)

        return probabilities

    def get_current_level(self) -> int:
        """Получение текущего уровня"""

        return self.__index_current_level

    def level_complete(self, score: int) -> bool:
        """
        Проверка, что уровень пройден.

        :param score: Счет для проверки.
        :return:
            True, если текущий уровень пройден, и False
            в обратном случае.
        """

        if self.__index_current_level >= len(self.__score_levels):
            return False

        return score >= self.__score_levels[self.__index_current_level]

    def level_up(self) -> None:
        """Повышения уровня"""

        # Повышаем счет уровня.
        self.__index_current_level += 1

        # Повышаем скорость появления астероидов.
        if self.__current_frequency > 0:
            self.__current_frequency -= self.__frequency_delta

        # Сдвигаем вероятности появления астероидов к более крупным.
        if self.__current_probability < self.__end_probability:
            self.__current_probability += 1
            self.__asteroid_probabilities = self._generate_probabilities(
                len(self.__asteroid_types),
                self.__current_probability,
            )

    def clear(self) -> None:
        """Сброс уровней"""

        self.__current_frequency = self.__start_frequency
        self.__current_probability = self.__start_probability
        self.__asteroid_probabilities = self._generate_probabilities(
            len(self.__asteroid_types),
            self.__start_probability,
        )
