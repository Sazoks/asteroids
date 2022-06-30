import pygame
import math

import settings


class Bullet(pygame.sprite.Sprite):
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
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.right < 0 or self.rect.left > settings.WIDTH \
                or self.rect.bottom < 0 or self.rect.top > settings.HEIGHT:
            self.kill()

        # Меняем положение объектов в пространстве.
        self.rect.centerx -= math.sin(self.angle) * self.__speed
        self.rect.centery -= math.cos(self.angle) * self.__speed

    def rotate(self, new_rot: float) -> None:
        self.rot = new_rot
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(settings.Collors.BLACK.value)
        self.rect = self.image.get_rect(center=old_center)

    def get_damage(self) -> int:
        return self.__damage

    def get_speed(self) -> float:
        return self.__speed

    def get_height(self) -> int:
        return self.__height

    def get_width(self) -> int:
        return self.__width
