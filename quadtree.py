import pygame
from typing import (
    Optional,
    List,
)

import settings
from my_dataclasses import (
    Point,
    Area,
)
from collider.collideable import Collideable


class Quadtree:
    """
    Структура данных квадродерева.

    Необходима для поиска столкновений объектов.
    """

    class QuadtreeNode:
        """Узел квадродерева"""

        def __init__(self, area: Area,
                     quadtree: 'Quadtree',
                     search_accuracy: int = 10,
                     parent: Optional['Quadtree.QuadtreeNode'] = None) -> None:
            """
            Инициализатор класса.

            :param area: Текущая секция.
            :param search_accuracy: Точность поиска в секции.
            :param parent: Родительский узел.
            """

            self.__quadtree = quadtree
            self.__parent = parent
            self.__area = area
            self.__search_accuracy = search_accuracy
            self.__data: List[Collideable] = []
            self.__nodes: List['Quadtree.QuadtreeNode'] = []

        def get_parent(self) -> Optional['Quadtree.QuadtreeNode']:
            return self.__parent

        def get_section(self) -> Area:
            return self.__area

        def get_search_accuracy(self) -> int:
            """
            Геттер для получения точности поиска в секции.

            :return: Точность поиска в секции в px.
            """

            return self.__search_accuracy

        def get_data(self) -> List[Collideable]:
            """
            Геттер для получения данных об объектах в ноде.

            :return: Список объектов.
            """

            return self.__data

        def set_data(self, new_data: List[Collideable]) -> None:
            """
            Сеттер для установки данных в узел.

            :param new_data: Новый данные.
            """

            self.__data = new_data

        def get_nodes(self) -> List['Quadtree.QuadtreeNode']:
            """
            Геттер для получения всех подузлов.

            :return: Список всех подузлов.
            """

            return self.__nodes

        def in_section(self, checked_object: Collideable) -> bool:
            """
            Вхождение объекта в секцию.

            :param checked_object: Проверяемый объект.
            :return: True, если объект входит в текущую секуцию, иначе False.
            """

            return checked_object.rect.colliderect(
                pygame.rect.Rect((self.get_section().top_left.x, self.get_section().top_left.y,
                                  self.get_section().get_width(), self.get_section().get_height()))
            )

        def clear(self):
            self.__nodes = []
            self.__data = []

        def add(self, added_object: Collideable) -> None:
            # Делаем проверки для первых двух добавляемых объектов.
            # Если объектов нет и узлов тоже нет, значит добавляем объект
            # на самый главный узел.
            # Если объекты есть, а узлов нет, значит у нас всего 1 объект и мы
            # хотим добавить второй. Остальные случае обрабатываются в цикле
            # (больше 2 объектов).
            for node in self.get_nodes():
                if node.in_section(added_object):
                    if node.is_empty():
                        if len(node.get_nodes()) == 0:
                            node.set_data([added_object])
                        else:
                            node.add(added_object)
                    else:
                        # FIXME: Сделать абстрактный класс 2d объектов вместо Player'a.
                        # Сохраняем объект, который уже есть в секторе, куда попал новый объект,
                        # перед разбиением этого сектора на подсекторы и удаления из него данных.
                        if node.get_section().get_width() > self.get_search_accuracy():
                            saved_objects = node.get_data()
                            node.create_nodes()
                            for saved_object in saved_objects:
                                node.add(saved_object)
                            node.add(added_object)
                        else:
                            node.get_data().append(added_object)
                            self.__quadtree.add_collision_node(node)

        def create_nodes(self) -> None:
            """Создает новые узлы в текущей ноде и удаляет данные"""

            # Очищаем данные.
            self.__data = []
            # Создаем 4 новых узла, вычисляя для каждого новые площади.
            self.__nodes = [
                Quadtree.QuadtreeNode(
                    area=Area(
                        top_left=self.get_section().top_left,
                        bottom_right=Point(
                            x=self.get_section().top_left.x + self.get_section().get_width() // 2,
                            y=self.get_section().top_left.y + self.get_section().get_height() // 2,
                        )
                    ),
                    quadtree=self.__quadtree,
                    search_accuracy=self.get_search_accuracy(),
                    parent=self,
                ),
                Quadtree.QuadtreeNode(
                    area=Area(
                        top_left=Point(
                            x=self.get_section().top_left.x + self.get_section().get_width() // 2,
                            y=self.get_section().top_left.y,
                        ),
                        bottom_right=Point(
                            x=self.get_section().top_left.x + self.get_section().get_width(),
                            y=self.get_section().top_left.y + self.get_section().get_height() // 2,
                        )
                    ),
                    quadtree=self.__quadtree,
                    search_accuracy=self.get_search_accuracy(),
                    parent=self,
                ),
                Quadtree.QuadtreeNode(
                    area=Area(
                        top_left=Point(
                            x=self.get_section().top_left.x,
                            y=self.get_section().top_left.y + self.get_section().get_height() // 2,
                        ),
                        bottom_right=Point(
                            x=self.get_section().top_left.x + self.get_section().get_width() // 2,
                            y=self.get_section().top_left.y + self.get_section().get_height(),
                        )
                    ),
                    quadtree=self.__quadtree,
                    search_accuracy=self.get_search_accuracy(),
                    parent=self,
                ),
                Quadtree.QuadtreeNode(
                    area=Area(
                        top_left=Point(
                            x=self.get_section().top_left.x + self.get_section().get_width() // 2,
                            y=self.get_section().top_left.y + self.get_section().get_height() // 2,
                        ),
                        bottom_right=self.get_section().bottom_right,
                    ),
                    quadtree=self.__quadtree,
                    search_accuracy=self.get_search_accuracy(),
                    parent=self,
                ),
            ]

        def is_empty(self) -> bool:
            """
            Проверка на пустоту секции.

            :return: True, если в текущей секции есть объекты, иначе False.
            """

            if len(self.__data) == 0:
                return True
            return False

        def __str__(self) -> str:
            if self.is_empty():
                return str(self.get_section()) + ': ' + \
                       str([str(node) for node in self.get_nodes()])
            else:
                return str(self.get_data())

    def __init__(self, area: Area, search_accuracy: int) -> None:
        """
        Инициализатор класса.

        :param area: Исходная область.
        :param search_accuracy: Точность поиска столкновений в px.
        """

        self.__search_accuracy = search_accuracy
        self.__first_node = Quadtree.QuadtreeNode(
            area=area,  # Сектор, занимаемый нодой.
            quadtree=self,  # Даем доступ нодам к дереву
                            # для добавления коллизий в общий список.
            search_accuracy=search_accuracy,  # Указываем для ноды степень разброса поиска.
        )
        self.__collisions: List['Quadtree.QuadtreeNode'] = []

    def add_collision_node(self, node: QuadtreeNode) -> None:
        self.__collisions.append(node)

    def remove_collision_node(self, node: QuadtreeNode) -> None:
        self.__collisions.remove(node)

    def get_collision_nodes(self) -> List[QuadtreeNode]:
        return self.__collisions

    def get_first_node(self) -> QuadtreeNode:
        """
        Геттер корневого узла.

        :return: Возвращает корневой узел дерева.
        """

        return self.__first_node

    def get_search_accuracy(self) -> int:
        """
        Геттер точности поиска.

        :return: Возвращает точность поиска столкновений в пикселях.
        """

        return self.__search_accuracy

    def clear(self) -> None:
        """
        Отчистка дерева.

        Перезаписывая первую ноду, сборщик мусора Python удалит
        все объекты, ссылка на которых удалились.

        Также очищаем список коллизий.
        """

        self.__first_node = Quadtree.QuadtreeNode(
            area=Area(
                top_left=self.get_first_node().get_section().top_left,
                bottom_right=self.get_first_node().get_section().bottom_right
            ),
            quadtree=self,
            search_accuracy=self.get_search_accuracy(),
        )
        self.__collisions = []

    def add(self, added_object: Collideable) -> None:
        """
        Добавление нового элемента в дерево.

        Пользуемся свойствами квадродерева и добавляем с высокой скоростью,
        сравнивая координаты добавляемого объекта с площадью областей.

        :param added_object: Добавлемый объект.
        """

        first_node = self.get_first_node()
        # Проверки для вставки в корневой узел.
        if len(first_node.get_nodes()) == 0:
            if first_node.is_empty():
                first_node.set_data([added_object])
            else:
                saved_objects = first_node.get_data()
                first_node.create_nodes()
                for saved_object in saved_objects:
                    first_node.add(saved_object)
                first_node.add(added_object)
        else:
            first_node.add(added_object)

    def remove(self, removed_object: Collideable,
               node: Optional[QuadtreeNode] = None) -> None:
        """
        Удаления узла с указанным элементом.

        :param removed_object: Удаляемый элемент.
        """

        # Определяем текущую ноду.
        removed_sections = self.find_sections(removed_object) \
            if node is None else [node]

        # Очищаем все ноды от объекта, где он есть.
        for section in removed_sections:
            section.clear()

        # Если у родителя, содержащего текущую ноду, нет больше данных,
        # удаляем и этого родителя.
        for section in removed_sections:
            parent = section.get_parent()
            empty_node = True
            for child_node in parent.get_nodes():
                if not child_node.is_empty() \
                        or not len(child_node.get_nodes()) == 0:
                    empty_node = False
                    break
            if empty_node:
                for child_node in parent.get_nodes():
                    del child_node
                self.remove(removed_object, parent)

    def find_sections(self, founded_object: Collideable,
                      start_node: Optional[QuadtreeNode] = None) \
            -> List[QuadtreeNode]:
        """
        Поиск всех секций, где есть указанный объект.

        :param founded_object: Объект, по которому ищем секции.
        :param start_node: Стартовый узел, с которого начинается поиск.
        :return: Список секций, где был обнаружен объект, или None.
        """

        # Проверяем текущую секцию.
        if start_node:
            for current_object in start_node.get_data():
                if founded_object is current_object:
                    return [start_node]

        # Если указана стартовая нода, начинаем искать с нее.
        # Иначе ищем с самого начала.
        nodes = start_node.get_nodes() if start_node \
            else self.get_first_node().get_nodes()
        if not nodes:
            return []

        # Собираем список нод, в которые входит текущий объект.
        founded_nodes = []
        for node in nodes:
            if node.in_section(founded_object):
                founded_nodes.extend(self.find_sections(founded_object, node))

        return founded_nodes

    def draw_quadtree(self, screen: pygame.display) -> None:
        # FIXME: Вынести в отдельный класс. И вообще отрефакторить тут все.
        def draw_node(node: Quadtree.QuadtreeNode) -> None:
            # Через область получаем координаты ребер области.
            top_line = (node.get_section().top_left.x, node.get_section().top_left.y), (
                node.get_section().bottom_right.x, node.get_section().top_left.y)
            left_line = (node.get_section().bottom_right.x - 1, node.get_section().top_left.y), (
                node.get_section().bottom_right.x - 1, node.get_section().bottom_right.y)
            bottom_line = (node.get_section().top_left.x, node.get_section().bottom_right.y - 1), (
                node.get_section().bottom_right.x, node.get_section().bottom_right.y - 1)
            right_line = (node.get_section().top_left.x, node.get_section().top_left.y), (
                node.get_section().top_left.x, node.get_section().bottom_right.y)

            pygame.draw.line(screen, settings.Collors.YELLOW.value, top_line[0], top_line[1], 1)
            pygame.draw.line(screen, settings.Collors.YELLOW.value, left_line[0], left_line[1], 1)
            pygame.draw.line(screen, settings.Collors.YELLOW.value, bottom_line[0], bottom_line[1], 1)
            pygame.draw.line(screen, settings.Collors.YELLOW.value, right_line[0], right_line[1], 1)

            for child_node in node.get_nodes():
                draw_node(child_node)

        draw_node(self.get_first_node())

    def __str__(self):
        return str(self.get_first_node())

