"""Модуль классов для работы с геометрией"""

from dataclasses import dataclass


@dataclass
class Point:
    """Класс точки с координатами"""

    x: int
    y: int

    def __floordiv__(self, divider: int) -> 'Point':
        """
        Перегрузка метода целочисленного деления //.

        :param divider: Делитель.
        :return: Новый объект с новыми значениями.
        """

        new_x = self.x // divider
        new_y = self.y // divider

        return Point(new_x, new_y)


@dataclass
class Area:
    """
    Класс секции.

    Задается верхней левой и правой нижней точками.
    """

    top_left: Point
    bottom_right: Point

    def get_width(self) -> int:
        """
        Геттер для получения ширины секции.

        :return: Ширина секции.
        """

        return self.bottom_right.x - self.top_left.x

    def get_height(self) -> int:
        """
        Геттер для получения высоты секции.

        :return: Высота секции.
        """

        return self.bottom_right.y - self.top_left.y

    def __contains__(self, point: Point) -> bool:
        """
        Дандер-метод для оператора in.

        :param point: Объект точки.
        :return: True, если точка входит в секцию, иначе False.
        """

        return point.x >= self.top_left.x \
               and point.y >= self.top_left.y \
               and point.x <= self.bottom_right.x \
               and point.y <= self.bottom_right.y
