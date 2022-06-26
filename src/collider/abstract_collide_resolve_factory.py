from abc import (
    ABC,
    abstractmethod,
)

from .collideable import Collideable
from .resolves import AbstractCollideResolve


class AbstractCollideResolveFactory(ABC):
    """Абстрактная фабрика решений коллизий"""

    @classmethod
    @abstractmethod
    def create_resolve(cls, obj_1: Collideable , obj_2: Collideable) \
            -> AbstractCollideResolve:
        pass
