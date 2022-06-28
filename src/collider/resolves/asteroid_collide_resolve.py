import math

from asteroids.asteroid import Asteroid
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
    def get_object_types() -> tuple:
        """
        Геттер для получения имен классов объектов, столкновения
        которых может решать этот резолвер.

        :return:
            Кортеж имен классов объектов, которые могут сталкиваться.
        """

        return Asteroid, Asteroid

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

            # Проверка на приближение объектов.
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

                # Чтобы объекты не слипались, высчитываем перекрытие их
                # друг другом и отодвигаем еще на 2px.
                overlap = 0.5 * (self.__asteroid_1.radius
                                 + self.__asteroid_2.radius - distance + 2)
                self.__asteroid_1.x += math.sin(angle) * overlap
                self.__asteroid_1.y -= math.cos(angle) * overlap
                self.__asteroid_2.x -= math.sin(angle) * overlap
                self.__asteroid_2.y += math.cos(angle) * overlap
