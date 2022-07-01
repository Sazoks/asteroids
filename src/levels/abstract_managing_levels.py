"""Модуль интерфейса управления уровнями"""

from abc import (
    ABC,
    abstractmethod,
)


class ManagingLevels(ABC):
    """
    Абстрактный класс (интерфейс) для управления уровнями.

    Классы, наследующий этот абстрактынй класс, могут повышать и понижать
    свои уровни. Логику, которая выполняется при повышении/понижении уровня,
    классы определяют сами.
    """

    @abstractmethod
    def level_up(self) -> None:
        pass

    @abstractmethod
    def level_down(self) -> None:
        pass

    @abstractmethod
    def reset_levels(self) -> None:
        pass

    @abstractmethod
    def get_current_level(self) -> int:
        pass
