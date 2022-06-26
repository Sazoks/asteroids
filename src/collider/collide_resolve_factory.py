from typing import Optional

from . import resolves
from .collideable import Collideable
from .abstract_collide_resolve_factory import AbstractCollideResolveFactory


class CollideResolveFactory(AbstractCollideResolveFactory):
    """Фабрика решений коллизий объектов"""

    # Список доступных решений в фабрике.
    # Список предоставляет классы, которые решают столкновений двух объектов
    # определенного типа.
    __allowed_resolves = [
        resolves.AsteroidCollideResolve,
        resolves.AsteroidPlayerCollideResolve,
        resolves.AsteroidBulletCollideResolve,
        resolves.PowerupPlayerCollideResolve,
    ]

    @classmethod
    def create_resolve(cls, obj_1: Collideable, obj_2: Collideable) \
            -> Optional[resolves.AbstractCollideResolve]:
        """
        Создание объекта решения коллизии двух объектов.

        Решение определяется, когда имена классов двух объектов
        совпадают с именами классов объектов в очередном решении.

        :param obj_1: Объект 1.
        :param obj_2: Объект 2.
        :return: Объект решения коллизии двух объектов.
        """

        object_types = (type(obj_1), type(obj_2))

        # TODO:
        #  Подумать над тем, чтобы сделать список решений. Это может
        #  пригодиться, когда может сработать более одного обработчика.
        # Сравниваем имена классов объектов с именами классов
        # объектов, с которыми работает очередное решение.
        for resolve in cls.__allowed_resolves:
            resolve_types = resolve.get_object_types()
            # Если типы не равны, возможно, их нужно поменять местами.
            if not cls._check_types(resolve_types, object_types):
                object_types_tmp = object_types[1], object_types[0]
                # Если после замены местами типы совпадают, решаем коллизию.
                if cls._check_types(resolve_types, object_types_tmp):
                    return resolve(obj_2, obj_1)
            else:
                # Если типы совпали сразу.
                return resolve(obj_1, obj_2)

    @staticmethod
    def _check_types(resolve_types: tuple, object_types: tuple) -> bool:
        """
        Проверка кортежей с классами.

        :param resolve_types: Кортеж с классами решения.
        :param object_types: Кортеж с классами переданных объектов.
        :return:
            True, если класс переданных объектов являются классами или
            подклассами классов решения.
        """

        # PyCharm немного глупый, и зря подчеркивает resolve_types красным.
        return issubclass(object_types[0], resolve_types[0]) \
               and issubclass(object_types[1], resolve_types[1])
