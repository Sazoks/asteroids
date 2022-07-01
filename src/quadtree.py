"""Модуль для работы с квадродеревом"""

import pygame
from typing import (
    Optional,
    List,
)

import settings
from utils.geometry import (
    Area,
    Point,
)
from collider.collideable import Collideable


class Quadtree:
    """
    Структура данных квадродерева.

    Необходима для поиска столкновений объектов.
    """

    class QuadtreeNode:
        """Узел квадродерева"""

        def __init__(
                self,
                area: Area,
                quadtree: 'Quadtree',
                search_accuracy: int = 10,
                parent: Optional['Quadtree.QuadtreeNode'] = None,
        ) -> None:
            """
            Инициализатор класса.

            :param area: Текущая секция.
            :param quadtree:
                Объект квадродерева. Каждый узел имеет доступ к общему дереву
                для добавления коллизийных узлов в общий список коллизийных
                узлов.
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
            """
            Геттер для получения родительского узла.

            :return: Объект родительского узла квадродерева.
            """

            return self.__parent

        def get_section(self) -> Area:
            """
            Геттер для получения объекта секции.

            :return: Объект секции узла квадродерева.
            """

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

            section = self.get_section()

            return checked_object.rect.colliderect(
                pygame.rect.Rect((
                    section.top_left.x,
                    section.top_left.y,
                    section.get_width(),
                    section.get_height(),
                ))
            )

        def clear(self):
            """Очистка узла дерева от даных и подузлов"""

            self.__nodes = []
            self.__data = []

        def add(self, added_object: Collideable) -> None:
            """
            Добавление объекта в узел.

            :param added_object: Добавляемый объект.
            """

            # Итерируемся по каждой подноде в текущей ноде.
            for node in self.get_nodes():
                # Если объект входит в секцию ноды.
                if node.in_section(added_object):
                    # Если в нод нет других объектов.
                    if node.is_empty():
                        # Если в ноде нет ни объектов, ни других нод, просто
                        # добавляем объект в текущую ноду. Эта нода становится
                        # листом.
                        if len(node.get_nodes()) == 0:
                            node.set_data([added_object])
                        # Иначе если есть другие подноды, повторяем процедуру
                        # добавления уже для этой ноды и ее поднод.
                        else:
                            node.add(added_object)
                    # Иначе, если в нод есть другие объекты.
                    else:
                        # Если размеры секции в текущей ноде больше
                        # минимального размера неделимой ноды.
                        if node.get_section().get_width() > self.get_search_accuracy():
                            # Тогда сохраняем текущие данные.
                            saved_objects = node.get_data()
                            # Разбиваем текущую ноду на 4 подноды.
                            node.create_nodes()
                            # Добавляем в подноды текущей ноды старые данные.
                            for saved_object in saved_objects:
                                node.add(saved_object)
                            # Добавляем новый объект.
                            node.add(added_object)
                        # Если размер секции в ноде является минимально
                        # возможным, т.е. нода неделима, тогда просто добавляем
                        # новый объект в ноду и получаем ноду с возможной
                        # коллизией. Эту ноду мы заносим в общий список
                        # нод с возможными коллизиями объектов.
                        else:
                            node.get_data().append(added_object)
                            self.__quadtree.add_collision_node(node)

        def create_nodes(self) -> None:
            """Создает новые узлы в текущей ноде и удаляет данные"""

            # Очищаем данные.
            self.__data = []

            # Создаем 4 новых узла, вычисляя для каждого новые площади.
            section = self.get_section()
            self.__nodes = [
                Quadtree.QuadtreeNode(
                    area=Area(
                        top_left=section.top_left,
                        bottom_right=Point(
                            x=section.top_left.x + section.get_width() // 2,
                            y=section.top_left.y + section.get_height() // 2,
                        )
                    ),
                    quadtree=self.__quadtree,
                    search_accuracy=self.get_search_accuracy(),
                    parent=self,
                ),
                Quadtree.QuadtreeNode(
                    area=Area(
                        top_left=Point(
                            x=section.top_left.x + section.get_width() // 2,
                            y=section.top_left.y,
                        ),
                        bottom_right=Point(
                            x=section.top_left.x + section.get_width(),
                            y=section.top_left.y + section.get_height() // 2,
                        )
                    ),
                    quadtree=self.__quadtree,
                    search_accuracy=self.get_search_accuracy(),
                    parent=self,
                ),
                Quadtree.QuadtreeNode(
                    area=Area(
                        top_left=Point(
                            x=section.top_left.x,
                            y=section.top_left.y + section.get_height() // 2,
                        ),
                        bottom_right=Point(
                            x=section.top_left.x + section.get_width() // 2,
                            y=section.top_left.y + section.get_height(),
                        )
                    ),
                    quadtree=self.__quadtree,
                    search_accuracy=self.get_search_accuracy(),
                    parent=self,
                ),
                Quadtree.QuadtreeNode(
                    area=Area(
                        top_left=Point(
                            x=section.top_left.x + section.get_width() // 2,
                            y=section.top_left.y + section.get_height() // 2,
                        ),
                        bottom_right=section.bottom_right,
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

    def __init__(self, area: Area, search_accuracy: int) -> None:
        """
        Инициализатор класса.

        :param area: Исходная область.
        :param search_accuracy:
            Точность поиска столкновений в px. Задает минимальный размер
            секции, в которой находятся объекты.
        """

        self.__search_accuracy = search_accuracy
        # Создаем корневую ноду. Каждая нода имеет доступ к экземпляру
        # квадродерева для добавления коллизийных нод в общий список.
        # Этот список мы достаем из дерева и обрабатываем столкновения
        # объектов только в тех нодах, где это может быть.
        self.__first_node = Quadtree.QuadtreeNode(
            area=area,
            quadtree=self,
            search_accuracy=search_accuracy,
        )
        self.__collisions: List['Quadtree.QuadtreeNode'] = []

    def add_collision_node(self, node: QuadtreeNode) -> None:
        """Добавление ноды в список коллизийных нод"""

        self.__collisions.append(node)

    def remove_collision_node(self, node: QuadtreeNode) -> None:
        """Удаление ноды из списка коллизийных нод"""

        self.__collisions.remove(node)

    def get_collision_nodes(self) -> List[QuadtreeNode]:
        """
        Получение списка нод с возможными коллизиями объектов.

        :return:
            Список нод квадродерева, в которых объекты, вероятно, столкнуться.
        """

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
        :param node: Нода, откуда нужно начинать искать.
        """

        # Определяем текущие ноды, в которых находится объект.
        removed_nodes = self.find_sections(removed_object) \
            if node is None else [node]

        # Очищаем все ноды от объекта, где он есть.
        for node in removed_nodes:
            node.clear()

        # Если у родителя, содержащего текущую ноду, нет больше данных,
        # удаляем и этого родителя.
        for node in removed_nodes:
            parent = node.get_parent()
            empty_node = True
            for child_node in parent.get_nodes():
                if not child_node.is_empty() \
                        or len(child_node.get_nodes()) != 0:
                    empty_node = False
                    break
            if empty_node:
                parent.clear()
                self.remove(removed_object, parent)

    def find_sections(self, found_object: Collideable,
                      start_node: Optional[QuadtreeNode] = None) \
            -> List[QuadtreeNode]:
        """
        Поиск всех секций, где есть указанный объект.

        :param found_object: Объект, по которому ищем секции.
        :param start_node: Стартовый узел, с которого начинается поиск.
        :return: Список секций, где был обнаружен объект, или None.
        """

        # Проверяем текущую секцию.
        if start_node:
            for current_object in start_node.get_data():
                if found_object is current_object:
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
            if node.in_section(found_object):
                founded_nodes.extend(self.find_sections(found_object, node))

        return founded_nodes

    def draw_quadtree(self, screen: pygame.display) -> None:
        """
        Отрисовка квадродерева на экран.

        :param screen: Объект экрана, куда нужно отрисовывать квадродерево.
        """

        def draw_node(node: Quadtree.QuadtreeNode) -> None:
            """
            Функция отрисовки секции в ноде.

            :param node: Нода, чью секцию необходимо отрисовать на экран.
            """

            section = node.get_section()

            # Через секцию в ноде получаем координаты ребер этой секции.
            top_line = (section.top_left.x, section.top_left.y), \
                       (section.bottom_right.x, section.top_left.y)
            left_line = (section.bottom_right.x - 1, section.top_left.y), \
                        (section.bottom_right.x - 1, section.bottom_right.y)
            bottom_line = (section.top_left.x, section.bottom_right.y - 1), \
                          (section.bottom_right.x, section.bottom_right.y - 1)
            right_line = (section.top_left.x, section.top_left.y), \
                         (section.top_left.x, section.bottom_right.y)

            # Отрисовка линий секции по найденным координатам.
            pygame.draw.line(screen, settings.Collors.YELLOW.value,
                             top_line[0], top_line[1], 1)
            pygame.draw.line(screen, settings.Collors.YELLOW.value,
                             left_line[0], left_line[1], 1)
            pygame.draw.line(screen, settings.Collors.YELLOW.value,
                             bottom_line[0], bottom_line[1], 1)
            pygame.draw.line(screen, settings.Collors.YELLOW.value,
                             right_line[0], right_line[1], 1)

            # Отрисовка каждой подноды в текущей ноде.
            for child_node in node.get_nodes():
                draw_node(child_node)

        # Начинаем отрисовку квадродерева с корневой ноды.
        draw_node(self.get_first_node())
