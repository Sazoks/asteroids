"""Модуль снаряд игрока"""

import pygame
import math

import settings
from collider.collideable import Collideable


class Bullet(Collideable, pygame.sprite.Sprite):
    """Класс снаряда игркоа"""

    def __init__(
            self,
            skin: pygame.Surface,
            pos_x: int,
            pos_y: int,
            angle: float,
            damage: int,
    ) -> None:
        """
        Инициализатор класса.

        :param skin: Изображение спрайта.
        :param pos_x: Позиция по оси Х.
        :param pos_y: Позиция по оси Y.
        :param damage: Урон снаряда.
        """

        pygame.sprite.Sprite.__init__(self)

        self.__width = 15
        self.__height = 70
        self.image_orig = pygame.transform.scale(
            skin, (self.__width, self.__height),
        )
        self.image_orig.set_colorkey(settings.Collors.BLACK.value)
        self.image = self.image_orig.copy()

        self.rect = self.image.get_rect()
        self.rect.centery = pos_y
        self.rect.centerx = pos_x

        self.__damage = damage
        self.angle = angle
        self.__speed = 18
        self.rot = 0

        # Поворачиваем снаряд в нужную сторону.
        self.rotate(math.degrees(angle))

    def update(self):
        """
        Обновление состояния снаряда.

        Вызывается у через группу спрайтов у всех снарядов.
        """

        # При выходе за границы игрового поля уничтожить спрайт.
        # Он удаляется из всех групп.
        if self.rect.right < 0 or self.rect.left > settings.WIDTH \
                or self.rect.bottom < 0 or self.rect.top > settings.HEIGHT:
            self.kill()

        # Меняем положение объектов в пространстве.
        self.rect.centerx -= math.sin(self.angle) * self.__speed
        self.rect.centery -= math.cos(self.angle) * self.__speed

    def rotate(self, new_rot: float) -> None:
        """
        Установка нового угла для снаряда.

        :param new_rot: Новый угол в радианах.
        """

        self.rot = new_rot
        # Получаем новый повернутый спрайт.
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(settings.Collors.BLACK.value)
        self.rect = self.image.get_rect(center=old_center)

    def get_damage(self) -> int:
        """
        Геттер урона снаряда.

        :return: Целое число, урон снаряда.
        """

        return self.__damage

    def get_speed(self) -> float:
        """
        Геттер скорости.

        :return: Вещественное число, скорость снаряда.
        """

        return self.__speed

    def get_height(self) -> int:
        """
        Геттер высоты снаряда.

        :return: Целое число, высота снаряда в px.
        """

        return self.__height

    def get_width(self) -> int:
        """
        Геттер ширины снаряда.

        :return: Целое число, ширина снаряда в px.
        """

        return self.__width
