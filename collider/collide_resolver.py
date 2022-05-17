from my_annotation.collideable import Collideable
from .abstract_collide_resolve_factory import AbstractCollideResolveFactory


class CollideResolver:
    """Класс для разрешения столкновений объектов"""

    def __init__(self, collide_resolve_factory: AbstractCollideResolveFactory) -> None:
        """
        Инициализатор класса.

        :param collide_resolve_factory: Фабрика решений коллизий.
        """

        self.__collide_resolve_factory = collide_resolve_factory

    def resolve(self, obj_1: Collideable, obj_2: Collideable) -> None:
        """
        Метод разрешения коллизий двух объектов.

        Нужное решение генерируется в фабрике на основе
        имен классов объектов.

        :param obj_1: Объект 1.
        :param obj_2: Объект 2.
        """

        # Создаем нужное решение для двух объектов.
        current_resolve = self.__collide_resolve_factory.create_resolve(obj_1, obj_2)
        if current_resolve:
            current_resolve.resolve()
