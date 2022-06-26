from typing import Tuple
from abc import (
    ABC,
    abstractmethod,
)


class AbstractCollideResolve(ABC):
    """Абстрактный класс разрешения коллизии"""

    @staticmethod
    @abstractmethod
    def get_object_types() -> Tuple[str, str]:
        pass

    @abstractmethod
    def resolve(self) -> None:
        pass
