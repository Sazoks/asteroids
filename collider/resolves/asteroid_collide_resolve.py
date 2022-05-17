import math
import pygame
from typing import Tuple

from asteroid import Asteroid
from .abstract_collide_resolve import AbstractCollideResolve


class AsteroidCollideResolve(AbstractCollideResolve):
    """Класс для разрешения столкновений астероидов"""

    def __init__(self, asteroid_1: Asteroid, asteroid_2: Asteroid) -> None:
        """
        Инициализатор класса.

        :param asteroid_1: Астероид 1.
        :param asteroid_2: Астероид 2.
        """

        self.__asteroid_1 = asteroid_1
        self.__asteroid_2 = asteroid_2

    @staticmethod
    def get_object_types() -> Tuple[str, str]:
        """
        Геттер для получения имен классов объектов, столкновения
        которых может решать этот резолвер.

        :return:
            Кортеж имен классов объектов, которые могут сталкиваться.
        """

        return Asteroid.__name__, Asteroid.__name__

    def resolve(self) -> None:
        """Обработка столкновения объекта с другим объектом"""

        # Проверять коллизию шара с самим с собой не имеет смысла.
        if self.__asteroid_1 is not self.__asteroid_2:
            dx = self.__asteroid_1.x - self.__asteroid_2.x
            dy = self.__asteroid_1.y - self.__asteroid_2.y

            # Дистанция между границами объектов.
            distance = math.hypot(dx, dy)

            # Если шары столкнулись при следующем шаге.
            new_x_1 = self.__asteroid_1.x + self.__asteroid_1.speed \
                      * math.sin(self.__asteroid_1.angle)
            new_y_1 = self.__asteroid_1.y - self.__asteroid_1.speed \
                      * math.cos(self.__asteroid_1.angle)
            new_x_2 = self.__asteroid_2.x + self.__asteroid_2.speed \
                      * math.sin(self.__asteroid_2.angle)
            new_y_2 = self.__asteroid_2.y - self.__asteroid_2.speed \
                      * math.cos(self.__asteroid_2.angle)
            new_distance = math.sqrt((new_x_1 - new_x_2) ** 2 + (new_y_1 - new_y_2) ** 2)

            # Проверка на прближение объектов.
            if self.__asteroid_1.radius + self.__asteroid_2.radius > new_distance:
                # Угол столкновения объектов.
                angle = math.atan2(dy, dx) + 0.5 * math.pi
                # Общая масса двух объектов.
                total_mass = self.__asteroid_1.get_weight() + self.__asteroid_2.get_weight()

                # Вычисляем новые скорости с учетом масс объектов.
                new_speed_1 = (self.__asteroid_1.speed * (self.__asteroid_1.get_weight()
                                                          - self.__asteroid_2.get_weight())
                               + 2 * self.__asteroid_2.get_weight()
                               * self.__asteroid_2.speed) / total_mass
                new_speed_2 = (self.__asteroid_2.speed * (self.__asteroid_2.get_weight()
                                                          - self.__asteroid_1.get_weight())
                               + 2 * self.__asteroid_1.get_weight()
                               * self.__asteroid_1.speed) / total_mass

                # Меняем векторы скорости
                self.__asteroid_1.speed, self.__asteroid_2.speed = \
                    new_speed_1, new_speed_2

                # Меняем углы движений объектов.
                self.__asteroid_1.angle += angle
                self.__asteroid_2.angle += angle + math.pi

                # Чтобы объекты не слипались, отодвигаем их на 1px и учитываем перекрытие.
                overlap = 0.5 * (self.__asteroid_1.radius
                                 + self.__asteroid_2.radius - distance + 2)
                self.__asteroid_1.x += math.sin(angle) * overlap
                self.__asteroid_1.y -= math.cos(angle) * overlap
                self.__asteroid_2.x -= math.sin(angle) * overlap
                self.__asteroid_2.y += math.cos(angle) * overlap

                # # Вариант 2.
                # angle = math.atan2(dy, dx) + 0.5 * math.pi
                # # Чтобы объекты не слипались, отодвигаем их на 1px и учитываем перекрытие.
                # overlap = 0.5 * (self.__asteroid_1.radius
                #                  + self.__asteroid_2.radius - distance + 2)
                # self.__asteroid_1.x += math.sin(angle) * overlap
                # self.__asteroid_1.y -= math.cos(angle) * overlap
                # self.__asteroid_2.x -= math.sin(angle) * overlap
                # self.__asteroid_2.y += math.cos(angle) * overlap
                #
                # N = pygame.Vector2(dx, dy)
                # uN = N.normalize()
                # uT = pygame.Vector2(-uN.y, uN.x)
                #
                # V1 = pygame.Vector2(math.sin(self.__asteroid_1.angle) * self.__asteroid_1.speed,
                #                     -math.cos(self.__asteroid_1.angle) * self.__asteroid_1.speed)
                # V2 = pygame.Vector2(math.sin(self.__asteroid_2.angle) * self.__asteroid_2.speed,
                #                     -math.cos(self.__asteroid_2.angle) * self.__asteroid_2.speed)
                #
                # V1n = uN.dot(V1)
                # V1t = uT.dot(V1)
                # V2n = uN.dot(V2)
                # V2t = uT.dot(V2)
                #
                # m1, m2 = self.__asteroid_1.get_weight(), \
                #          self.__asteroid_2.get_weight()
                #
                # V1t_ = V1t
                # V2t_ = V2t
                # V1n_ = (V1n * (m1 - m2) + 2 * m2 * V2n) / (m1 + m2)
                # V2n_ = (V2n * (m2 - m1) + 2 * m1 * V1n) / (m1 + m2)
                #
                # newV1n = V1n_ * uN
                # newV1t = V1t_ * uT
                # newV2n = V2n_ * uN
                # newV2t = V2t_ * uT
                #
                # newV1FINAL = newV1n + newV1t
                # newV2FINAL = newV2n + newV2t
                #
                # speed_1 = newV1FINAL.length()
                # speed_x_1, speed_y_1 = newV1FINAL
                # cp_speed_x_1, cp_speed_y_1 = abs(speed_x_1), abs(speed_y_1)
                # cp_newV1FINAL = pygame.Vector2(cp_speed_x_1, cp_speed_y_1)
                # angle_1 = cp_newV1FINAL.angle_to(pygame.Vector2(0, 1)) \
                #           * (cp_speed_x_1 // speed_x_1) * (cp_speed_y_1 // speed_y_1)
                #
                # speed_2 = newV2FINAL.length()
                # speed_x_2, speed_y_2 = newV2FINAL
                # cp_speed_x_2, cp_speed_y_2 = abs(speed_x_2), abs(speed_y_2)
                # cp_newV2FINAL = pygame.Vector2(cp_speed_x_2, cp_speed_y_2)
                # angle_2 = cp_newV2FINAL.angle_to(pygame.Vector2(0, 1)) \
                #           * (cp_speed_x_2 // speed_x_2) * (cp_speed_y_2 // speed_y_2)
                #
                # self.__asteroid_1.speed = speed_1
                # self.__asteroid_1.angle = angle_1
                # self.__asteroid_2.speed = speed_2
                # self.__asteroid_2.angle = angle_2
