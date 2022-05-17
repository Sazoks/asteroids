import random
import pygame
import math
from typing import (
    List,
    Dict,
    Optional,
    Tuple,
)

import settings


class Asteroid(pygame.sprite.Sprite):
    """Класс астероидов"""

    # Значение, при котором астероид не должен делиться.
    __min_radius = 30
    __min_max_new_asteroids = (2, 6)

    def __init__(self,
                 skin: pygame.Surface,
                 size: int, speed: float,
                 pos_x: Optional[int] = None,
                 pos_y: Optional[int] = None,
                 angle: Optional[float] = None) -> None:
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
        self.image.set_colorkey(settings.Collors.BLACK.value)

        # Задаем позицию, угол и скорость астероида.
        self.x = random.randint(self.radius, settings.WIDTH - self.radius) \
            if pos_x is None else pos_x
        self.y = random.randint(self.radius, settings.HEIGHT - self.radius) \
            if pos_y is None else pos_y
        self.speed = speed
        self.angle = random.random() * random.choice([-1, 1]) \
            if angle is None else angle
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.source_health = size
        self.health = size
        self.reward = size

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
        if self.x + self.radius < 0 or self.x - self.radius > settings.WIDTH \
                or self.y + self.radius < 0 or self.y - self.radius > settings.HEIGHT:
            self.kill()

        # if self.x > settings.WIDTH - self.radius:
        #     self.x = 2 * (settings.WIDTH - self.radius) - self.x
        #     self.angle = - self.angle
        # elif self.x < self.radius:
        #     self.x = 2 * self.radius - self.x
        #     self.angle = - self.angle
        # if self.y > settings.HEIGHT - self.radius:
        #     self.y = 2 * (settings.HEIGHT - self.radius) - self.y
        #     self.angle = math.pi - self.angle
        # elif self.y < self.radius:
        #     self.y = 2 * self.radius - self.y
        #     self.angle = math.pi - self.angle

        # Меняем положение объектов в пространстве.
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.rect.center = round(self.x), round(self.y)

    def draw_health_bar(self, screen: pygame.Surface) -> None:
        """
        Отрисовка полоски здоровья астероида.

        :param screen: Экран, на который нужно рисовать.
        """
        if self.health < 0:
            self.health = 0
        BAR_LENGTH = 45
        BAR_HEIGHT = 10
        # Получаем оставшееся здоровье астероида в процентах.
        remaining_health_percent = self.health * 100 / self.source_health
        fill = remaining_health_percent * BAR_LENGTH / 100
        outline_rect = pygame.Rect(
            self.x - BAR_LENGTH // 2,
            self.y + self.radius + 5,
            BAR_LENGTH, BAR_HEIGHT
        )
        fill_rect = pygame.Rect(
            self.x - BAR_LENGTH // 2,
            self.y + self.radius + 5,
            fill, BAR_HEIGHT
        )
        pygame.draw.rect(screen, settings.Collors.RED.value, fill_rect)
        pygame.draw.rect(screen, settings.Collors.WHITE.value, outline_rect, 2)

    def split_asteroid(self) -> List['Asteroid']:
        """Метод разбиения астероида на два меньших"""

        count_new_asteroids = random.randint(*self.__min_max_new_asteroids)
        new_weight = self.get_weight() // (count_new_asteroids + 2)
        new_radius = (3 * new_weight / math.pi) ** (1 / 3)

        new_small_asteroids: List[Asteroid] = []
        for _ in range(count_new_asteroids):
            new_speed = self.speed * 0.9
            level = random.choice(list(settings.asteroid_skins.keys()))
            random_skin = random.choice(settings.asteroid_skins[level])
            new_small_asteroids.append(Asteroid(random_skin, new_radius, new_speed,
                                                self.x, self.y))

        return new_small_asteroids

    @classmethod
    def generate_asteroids(cls: 'Asteroid', skins: Dict[str, List[pygame.Surface]],
                           count: int, min_size: int, max_size: int,
                           min_speed: int, max_speed: int) -> List['Asteroid']:
        """
        Метод генерации игроков.

        :param count: Количество генерируемых астероидов.
        :param min_size: Минимальный размер.
        :param max_size: Максимальный размер.
        :param min_speed: Минимальная скорость.
        :param max_speed: Максимальная скорость.
        :return: Список объектов Player.
        """

        asteroids = []
        for _ in range(count):
            random_size = random.randint(min_size, max_size)
            random_speed = random.randint(min_speed, max_speed) / 100
            level = random.choice(list(skins.keys()))
            random_skin = random.choice(skins[level])
            new_asteroid = Asteroid(random_skin,
                                    random_size, random_speed)
            asteroids.append(new_asteroid)

        return asteroids

    def __repr__(self) -> str:
        return f'Asteroid(x={self.rect.centerx}, y={self.rect.centery})'


class AsteroidType:
    """Класс, задающий какой-то тип астероидов"""

    def __init__(self,
                 min_max_radius: Tuple[int, int],
                 min_max_speed: Tuple[int, int],
                 skins: List[pygame.Surface]) -> None:
        """
        Инициализатор класса.

        :param min_max_radius:
            Минимальная и максимальная размерность астероидов.
        :param min_max_speed:
            Минимальная и максимальная скорость астероидов.
        :param skins: Скины на астероиды этого типа.
        """

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
        angle = math.pi + random.uniform(0, math.pi / 4) * random.choice([-1, 1])
        new_asteroid = Asteroid(skin=skin, size=radius,
                                speed=speed, pos_y=-radius + 1,
                                angle=angle)

        return new_asteroid
