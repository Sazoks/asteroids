"""Модуль класса уровня"""


class Level:
    """Класс уровня"""

    def __init__(self, score: int) -> None:
        """
        Инициализатор класса.

        :param score: Счет для прохождения уровня.
        """

        self.__score = score

    @property
    def score(self) -> int:
        """
        Геттер счета уровня.

        :return: Целое число, счет уровня.
        """

        return self.__score

    def __repr__(self) -> str:
        """
        Читаемое представление объекта в виде строки.

        :return: Объект строки с информацией об объекте.
        """

        return str(self.__score)
