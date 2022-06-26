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
        return self.__score

    def __repr__(self) -> str:
        return str(self.__score)
