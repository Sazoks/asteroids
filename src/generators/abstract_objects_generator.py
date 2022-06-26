from typing import Generic, TypeVar
from abc import (
    ABC,
    abstractmethod,
)


F = TypeVar('F')
D = TypeVar('D')


class AbstractObjectsGenerator(Generic[F, D], ABC):
    """
    Абстрактный класс генератора игровых объектов.
    """

    def generate(self) -> F:

