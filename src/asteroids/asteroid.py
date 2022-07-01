import random
import pygame
import math
from typing import (
    List,
    Optional,
    Tuple,
)

import settings
from collider.collideable import Collideable


class Asteroid(Collideable, pygame.sprite.Sprite):
    """Класс астероидов"""

    # Значение в px, при котором астероид не должен делиться.
    __min_radius = 30
    # Минимальное и максимальное кол-во астероидов после деления
    # большего астероида.
    __min_max_new_asteroids = (2, 4)

    def __init__(
            self,
            skin: pygame.Surface,
            size: int,
            speed: float,
            pos_x: Optional[int] = None,
            pos_y: Optional[int] = None,
            angle: Optional[float] = None,
    ) -> None:
        """
        Инициализатор класса.

        :param skin: Скин астероида.
        :param size: Радиус астероида.
        :param speed: Скорость астероида.
        :param pos_x: Позиция по оси х астероида.
        :param pos_y: Позиция по оси у астероида.
        :param angle: Угол полета астероида.
        """

        pygame.sprite.Sprite.__init__(self)

        # Задаем радиус и представление объекта.
        self.radius = size
        self.image = pygame.transform.scale(skin, (size * 2, size * 2))
        # Игнорируем черный цвет и не отрисовываем его.
        self.image.set_colorkey(settings.Collors.BLACK.value)

        # Задаем позицию, угол и скорость астероида.
        self.__pos_x = random.randint(self.radius, settings.WIDTH - self.radius) \
            if pos_x is None else pos_x
        self.__pos_y = random.randint(self.radius, settings.HEIGHT - self.radius) \
            if pos_y is None else pos_y
        self.__speed = speed
        self.angle = random.random() * random.choice([-1, 1]) \
            if angle is None else angle
        self.rect = self.image.get_rect(center=(self.__pos_x, self.__pos_y))

        self.__source_health = size
        self.__health = size
        self.__reward = size

    def get_weight(self) -> float:
        """Масса объекта равна объему шара"""

        return math.pi * (self.radius ** 3) / 3

    @classmethod
    def get_min_size(cls) -> int:
        """
        Геттер для получения минимального значения,
        при котором астероид делиться не будет.
        """

        return cls.__min_radius

    def update(self) -> None:
        """
        Определяет поведение объекта при каждом игровом цикле.
        """

        # Учет столкновения объекта со стенками.
        if self.__pos_x + self.radius < 0 \
                or self.__pos_x - self.radius > settings.WIDTH \
                or self.__pos_y + self.radius < 0 \
                or self.__pos_y - self.radius > settings.HEIGHT:
            self.kill()

        # Меняем положение объектов в пространстве.
        self.__pos_x += math.sin(self.angle) * self.__speed
        self.__pos_y -= math.cos(self.angle) * self.__speed
        self.rect.center = round(self.__pos_x), round(self.__pos_y)

    def draw_health_bar(self, screen: pygame.Surface) -> None:
        """
        Отрисовка полоски здоровья астероида.

        :param screen: Экран, на который нужно рисовать.
        """

        if self.health < 0:
            self.health = 0
        BAR_LENGTH = 45
        BAR_HEIGHT = 10

        # Отрисовка полоски здоровья.
        remaining_health_percent = self.health * 100 / self.__source_health
        fill = remaining_health_percent * BAR_LENGTH / 100
        outline_rect = pygame.Rect(
            self.__pos_x - BAR_LENGTH // 2,
            self.__pos_y + self.radius + 5,
            BAR_LENGTH, BAR_HEIGHT
        )
        fill_rect = pygame.Rect(
            self.__pos_x - BAR_LENGTH // 2,
            self.__pos_y + self.radius + 5,
            fill, BAR_HEIGHT
        )

        # Отрисовка здоровья астероида цифрами.
        health_text = settings.health_font.render(
            f'{self.health}xp',
            True,
            settings.Collors.WHITE.value,
        )
        settings.screen.blit(
            health_text,
            (self.__pos_x - BAR_LENGTH // 2 + BAR_LENGTH + 1,
             self.__pos_y + self.radius + 5),
        )

        pygame.draw.rect(screen, settings.Collors.RED.value, fill_rect)
        pygame.draw.rect(screen, settings.Collors.WHITE.value, outline_rect, 2)

    def split_asteroid(self) -> List['Asteroid']:
        """Метод разбиения астероида на два меньших"""

        # Выбираем случайное кол-во астероидов.
        count_new_asteroids = random.randint(*self.__min_max_new_asteroids)
        # Высчитываем новый вес и размеры астероидов.
        new_weight = self.get_weight() // (count_new_asteroids + 2)
        new_radius = math.ceil((3 * new_weight / math.pi) ** (1 / 3))

        # Формируем список новых астероидов.
        new_small_asteroids: List[Asteroid] = []
        for _ in range(count_new_asteroids):
            # Немного замедлим новые астероиды после взрыва большего.
            new_speed = self.__speed * 0.9
            # Выбираем случайный скин.
            skin_level = random.choice(list(settings.asteroid_skins.keys()))
            random_skin = random.choice(settings.asteroid_skins[skin_level])
            new_small_asteroids.append(Asteroid(
                skin=random_skin,
                size=new_radius,
                speed=new_speed,
                pos_x=self.__pos_x,
                pos_y=self.__pos_y,
            ))

        return new_small_asteroids

    @property
    def pos_x(self) -> int:
        return self.__pos_x

    @pos_x.setter
    def pos_x(self, new_pos_x: int) -> None:
        self.__pos_x = new_pos_x

    @property
    def pos_y(self) -> int:
        return self.__pos_y

    @pos_y.setter
    def pos_y(self, new_pos_y: int) -> None:
        self.__pos_y = new_pos_y

    @property
    def speed(self) -> float:
        return self.__speed

    @speed.setter
    def speed(self, new_speed: float) -> None:
        self.__speed = new_speed

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, new_health: float) -> None:
        self.__health = new_health

    def get_source_health(self) -> int:
        return self.__source_health

    def get_reward(self) -> int:
        return self.__reward

    def __repr__(self) -> str:
        return f'Asteroid(x={self.rect.centerx}, y={self.rect.centery})'


class AsteroidType:
    """
    Класс, задающий тип астероидов.

    На основе данных этого класса будут генирироваться экземпляры
    класса Asteroid с различными значениями.
    """

    def __init__(
            self,
            min_max_radius: Tuple[int, int],
            min_max_speed: Tuple[int, int],
            skins: List[pygame.Surface],
    ) -> None:
        """
        Инициализатор класса.

        :param min_max_radius:
            Минимальная и максимальная размерность астероидов.
        :param min_max_speed:
            Минимальная и максимальная скорость астероидов.
        :param skins: Скины на астероиды этого типа.
        """

        # TODO: Добавить проверку, что min_max[0] < min_max[1].
        self.__min_max_radius = min_max_radius
        self.__min_max_speed = min_max_speed
        self.__skins = skins

    def create_asteroid(self) -> Asteroid:
        """
        Метод создания нового астероида на основе этого типа.

        :return: Новый астероид.
        """

        radius = random.randint(*self.__min_max_radius)
        speed = random.randint(*self.__min_max_speed) / 100
        skin = random.choice(self.__skins)
        angle = math.pi + random.uniform(0, math.pi / 4) \
                * random.choice([-1, 1])
        new_asteroid = Asteroid(
            skin=skin, size=radius,
            speed=speed, pos_y=-radius + 1,
            angle=angle,
        )

        return new_asteroid
