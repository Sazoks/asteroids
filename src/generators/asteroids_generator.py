# import pygame
# import math
# import random
# from typing import (
#     List,
#     Optional,
# )
#
# from asteroids.asteroid import (
#     Asteroid,
#     AsteroidType,
# )
# from levels.abstract_managing_levels import ManagingLevels
#
#
# class AsteroidsGenerator(ManagingLevels):
#     """
#     Класс для управления астероидами.
#
#     Наследует абстрактный класс (интерфейс) ManagingLevels для изменения
#     уровня генерации астероидов.
#     """
#
#     def __init__(
#             self,
#             start_frequency: float,
#             asteroid_types: List[AsteroidType],
#             levels_to_increase: int,
#     ) -> None:
#         """
#         Инициализатор класса.
#
#         :param start_frequency: Начальная частота появления астероидов.
#         :param asteroid_types:
#             Типы астероидов. Количество элементов этого списка определяет
#             количество уровней для генератора.
#         :param max_level: Максимальный уровень генератора.
#         :param levels_to_increase: Уровней для повышения уровня генератора.
#         """
#
#         assert len(asteroid_types) != 0
#
#         self.__last_asteroid_spawn = pygame.time.get_ticks()
#         self.__start_frequency = start_frequency
#         self.__current_frequency = start_frequency
#         # Дельта частоты появления астероидов между уровнями будет одинаковая.
#         self.__frequency_delta = \
#             (start_frequency - start_frequency // len(asteroid_types)) \
#             // len(asteroid_types)
#
#         self.__start_level = 0
#         self.__max_level = len(asteroid_types) - 1
#         self.__current_level = 0
#
#         # Уровней для повышения уровня генератора.
#         self.__levels_to_increase = levels_to_increase
#         # Счетчик уровней для повышения. Обнуляется по достижению
#         # self.__levels_to_increase.
#         self.__counter_to_increase = self.__start_level
#
#         self.__asteroid_types = asteroid_types
#
#         # Список встречаемостей астероидов разных типов.
#         self.__asteroid_probabilities = self._generate_probabilities(
#             len(self.__asteroid_types),
#             self.__start_level + 1,
#         )
#
#     def generate(self) -> Optional[Asteroid]:
#         """Генерация астероидов"""
#
#         now = pygame.time.get_ticks()
#         if now - self.__last_asteroid_spawn >= self.__current_frequency:
#             self.__last_asteroid_spawn = now
#
#             # Выбираем случайным образом с учетом вероятности тип астероида,
#             # который хотим создать. Вероятность появления = вес.
#             asteroid_type_index = random.choices(
#                 population=[i for i in range(len(self.__asteroid_types))],
#                 weights=self.__asteroid_probabilities,
#                 k=len(self.__asteroid_types),
#             )[0]
#
#             # Выбираем нужный тип астероида
#             asteroid_type = self.__asteroid_types[asteroid_type_index]
#             # Создаем астероид нужного типа.
#             new_asteroid = asteroid_type.create_asteroid()
#
#             return new_asteroid
#
#     @staticmethod
#     def _generate_probabilities(length: int, k: float = 1.0) -> List[float]:
#         """
#         Генерация вероятностей появления астероидов каждого типа
#         по распределению Пуассона.
#
#         Чем больше мы увеличиваем k, тем больше центр распределения смещается
#         в право, а значит тем больше вероятность появления у больших астероидов
#         и тем меньше вероятность появления у меньших астероидов.
#
#         :param length: Количество элементов.
#         :param k: Коэффициент для смещения среднего значения.
#         :return: Список вероятностей появления для каждого типа астероида.
#         """
#
#         probabilities: List[float] = [
#             (i ** k * math.e ** (-i)) / math.factorial(k)
#             for i in range(1, length + 1)
#         ]
#
#         return probabilities
#
#     def get_current_level(self) -> int:
#         return self.__current_level
#
#     def level_up(self) -> None:
#         """Повышения уровня"""
#
#         # TODO: Здесь должно быть еще условие для счетчика уровней.
#         if self.__current_level < self.__max_level:
#             # Понижаем задержку появления нового астероида. Т.е. повышаем
#             # частоту появления астероидов. Это увеличит сложность игры,
#             # что логично с повышением уровня.
#             if self.__current_frequency - self.__frequency_delta \
#                     >= self.__frequency_delta:
#                 self.__current_frequency -= self.__frequency_delta
#
#             # Сдвигаем вероятности появления астероидов к более крупным.
#             self.__current_level += 1
#             # Если счетчик равен количеству уровней для повышения уровня
#             # счетчика, пересчитываем вероятности появления астероидов.
#             self.__counter_to_increase += 1
#             if self.__counter_to_increase == self.__levels_to_increase:
#                 self.__asteroid_probabilities = self._generate_probabilities(
#                     len(self.__asteroid_types),
#                     self.__current_level + 1,
#                 )
#
#     def level_down(self) -> None:
#         """Понижение уровня"""
#
#         # Если есть, куда понижать уровни.
#         if self.__current_level > self.__start_level:
#             # Понижаем уровень и обновляем список вероятностей появлений
#             # астероидов определенного типа.
#             self.__current_level -= 1
#             self.__counter_to_increase -= 1
#             self.__asteroid_probabilities = self._generate_probabilities(
#                 len(self.__asteroid_types),
#                 self.__current_level + 1,
#             )
#             # Понижаем частоту появления астероидов, повышая задержку
#             # между появлениями астероидов.
#             self.__current_frequency += self.__frequency_delta
#
#     def reset_levels(self) -> None:
#         """Сброс уровней"""
#
#         self.__current_frequency = self.__start_frequency
#         self.__current_level = self.__start_level
#         self.__levels_cursor = 0
#         self.__asteroid_probabilities = self._generate_probabilities(
#             len(self.__asteroid_types),
#             self.__start_level + 1,
#         )
import math
from typing import List


def _generate_probabilities(length: int, k: float = 1.0) -> List[float]:
    probabilities: List[float] = [
        (k ** i * math.e ** (-k)) / math.factorial(i)
        for i in range(1, length + 1)
    ]

    return probabilities


def _generate_probabilities_2(length: int, k: float = 1.0) -> List[float]:
    probabilities: List[float] = [
        (i ** k * math.e ** (-i)) / math.factorial(k)
        for i in range(1, length + 1)
    ]

    return probabilities


l = _generate_probabilities_2(4, 1)
print(l)
print(sum(l))
