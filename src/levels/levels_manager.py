from typing import (
    List,
    Iterable,
    Optional,
    Dict,
)

from .level import Level
from .abstract_managing_levels import ManagingLevels


class LevelsManager(ManagingLevels):
    """
    Класс для управления уровнями игры.

    Отвечает за контроль текущего уровня игры, а также за управление
    уровнями игровых объектов. Например, генераторы астероидов, усилений или
    другие менеджеры уровней.
    """

    def __init__(self, levels: List[Level],
                 managed_objects: Optional[Iterable[ManagingLevels]] = None) -> None:
        """
        Инициализатор класса.

        :param levels: Список уровней.
        :param managed_objects:
            Список объектов, чей уровень нужно контролировать.
        """

        assert len(levels) > 0

        if managed_objects is None:
            self.__managed_objects = {}
        else:
            # Для обеспечения уникальности объектов используем словарь с
            # id() объектов в качестве ключей. Использовать set() я решил
            # не целесообразным, т.к. тогда логика обеспечения уникальности
            # будет зависеть от методов __eq__ и __hash__. В случае с словарем
            # мы по факту обеспечиваем уникальность объектов с помощью их
            # адреса в памяти и только.
            self.__managed_objects \
                = self._create_dict_managed_objects(managed_objects)


        self.__levels = self._validate_levels(levels)
        self.__level_cursor = 0

    def get_levels(self) -> List[Level]:
        return self.__levels

    def get_managed_objects(self) -> Dict[int, ManagingLevels]:
        return self.__managed_objects

    def level_complete(self, score: int) -> bool:
        """
        Проверяет, что переданный счет больше либо равен счет, необходимого
        для прохождения текущего уровня.

        :param score: Счет для проверки.
        :return: True, если уровень пройден, иначе False.
        """

        return score >= self.__levels[self.__level_cursor].score

    def get_current_level(self) -> int:
        return self.__level_cursor

    def level_up(self) -> None:
        """Повышение уровня"""

        # Если есть, куда повышать уровень.
        if self.__level_cursor < len(self.__levels) - 1:
            self.__level_cursor += 1
            for obj in self.__managed_objects.values():
                obj.level_up()

    def level_down(self) -> None:
        """Понижение уровня"""

        # Если есть, куда понижать уровень.
        if self.__level_cursor > 0:
            self.__level_cursor -= 1
            for obj in self.__managed_objects.values():
                obj.level_down()

    def reset_levels(self) -> None:
        """Сброс уровней"""

        self.__level_cursor = 0
        for obj in self.__managed_objects.values():
            obj.reset_levels()

    @staticmethod
    def _create_dict_managed_objects(
            managed_objects: Iterable[ManagingLevels]
    ) -> Dict[int, ManagingLevels]:
        """
        Создание словаря для контролируемых объектов.

        Суть такого словаря в том, что мы не должны иметь в последовательности
        два одинаковых объекта, т.к. в таком случае получится, что мы дважды
        повысим уровень одному и тому же объекту.

        :param managed_objects:
            Список объектов, чей уровень нужно контролировать.
        :return:
            Словарь, ключи которого - id объектов в Python, а значения -
            сами объекты.
        """

        dict_managed_objects: Dict[int, ManagingLevels] = {}
        for obj in managed_objects:
            dict_managed_objects[id(obj)] = obj

        return dict_managed_objects

    @staticmethod
    def _validate_levels(levels: List[Level]) -> List[Level]:
        """
        Валидация списка уровней.

        :param levels: Список уровней.
        :return: Отвалидированный список уровней.
        """

        # Сортировка списка уровней по возрастанию.
        levels = sorted(levels, key=lambda level: level.score)

        return levels

    def register_object(self, new_object: ManagingLevels) -> None:
        """
        Добавление объекта в менеджер для контроля его уровней.

        :param new_object: Объект, чей уровень необходимо контролировать.
        """

        self.__managed_objects[id(new_object)] = new_object

    def unregister_object(self, unregistered_object: ManagingLevels) -> None:
        """
        Удаление объекта из словаря контролируемых объектов.

        :param unregistered_object:
            Объект, над которым нужно прекратить контроль уровней.
        """

        object_id = id(unregistered_object)
        if object_id in self.__managed_objects.keys():
            self.__managed_objects.pop(object_id)

    def __repr__(self) -> str:
        """Информация об объекте в читаемом виде"""

        return f'count levels: {len(self.__levels)}\n' \
               f'levels: {self.__levels}\n' \
               f'count managed objects: {len(self.__managed_objects.keys())}\n' \
               f'managed objects: {self.__managed_objects}\n'
