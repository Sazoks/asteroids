from abc import (
    ABC,
    abstractmethod,
)

from .resolves import AbstractCollideResolve
from my_annotation.collideable import Collideable


class AbstractCollideResolveFactory(ABC):
    """Абстрактная фабрика решений коллизий"""

    @classmethod
    @abstractmethod
    def create_resolve(cls, obj_1: Collideable , obj_2: Collideable) \
            -> AbstractCollideResolve:
        pass
