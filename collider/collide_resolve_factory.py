from typing import Optional

from . import resolves
from my_annotation.collideable import Collideable
from .abstract_collide_resolve_factory import AbstractCollideResolveFactory


class CollideResolveFactory(AbstractCollideResolveFactory):
    """Фабрика решений коллизий объектов"""

    # Список доступных решений в фабрике.
    __allowed_resolves = [
        resolves.AsteroidCollideResolve,
        resolves.AsteroidPlayerCollideResolve,
        resolves.AsteroidBulletCollideResolve,
    ]

    @classmethod
    def create_resolve(cls, obj_1: Collideable, obj_2: Collideable) \
            -> Optional[resolves.AbstractCollideResolve]:
        """
        Создание решения коллизии двух объектов.

        Решение определяется, когда имена классов двух объектов
        совпадают с именами классов объектов в очередном решении.

        :param obj_1: Объект 1.
        :param obj_2: Объект 2.
        :return: Объект решения коллизии двух объектов.
        """

        object_types = (
            type(obj_1).__name__,
            type(obj_2).__name__,
        )

        # Сравниваем имена классов объектов с именами классов
        # объектов, с которыми работает очередное решение.
        for resolve in cls.__allowed_resolves:
            resolve_types = resolve.get_object_types()
            # Если типы не равны, возможно, их нужно поменять местами.
            if object_types != resolve_types:
                object_types_tmp = object_types[1], object_types[0]
                # Если после замены местами типы совпадают, решаем коллизию.
                if object_types_tmp == resolve_types:
                    return resolve(obj_2, obj_1)
            else:
                # Если типы совпали сразу.
                return resolve(obj_1, obj_2)