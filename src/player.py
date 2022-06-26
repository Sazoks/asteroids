import pygame
import math

import settings
from game_objects import GameObjects
from bullets.bullet import Bullet


class Player(pygame.sprite.Sprite):
    """Класс игрока"""

    def __init__(self,
                 skin: pygame.Surface, bullet_skin: pygame.Surface,
                 health: float, speed: float, damage: float,
                 radius: float, shoot_delay: int, score: int) -> None:
        """
        Инициализатор класса.

        :param skin: Изображение для спрайта игрока.
        :param bullet_skin: Изображение для снарядов игрока.
        :param health: Здоровьев игрока.
        :param speed: Скорость игрока.
        :param damage: Урон от снарядов игрока.
        :param radius: Радиус спрайта игрока.
        :param shoot_delay: Скорострельность игрока.
        :param score: Счет игрока.
        """

        pygame.sprite.Sprite.__init__(self)

        # Изображение пуль.
        self.bullet_skin = bullet_skin

        # Радиус и изображение объекта.
        self.radius = radius
        self.image_orig = pygame.transform.scale(skin, (self.radius * 2,
                                                        self.radius * 2))
        self.image_orig.set_colorkey(settings.Collors.BLACK.value)
        self.image = self.image_orig.copy()

        # Координаты, скорость и здоровье корабля.
        self.x = settings.WIDTH // 2
        self.y = settings.HEIGHT // 2
        self.speed = speed
        self.health = health
        self.source_health = health
        self.score = score

        # Задержка стрельбы.
        self.shoot_delay = shoot_delay
        self.last_shot = pygame.time.get_ticks()
        self.damage = damage

        # Прямоугольник игрового объекта.
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Параметры для вращения.
        self.rot = 0

    def update(self) -> None:
        """Метод обновления состояния игрока"""

        # Считываем координаты курсора.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        # Поворачиваем спрайта игрока в сторону курсора.
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        self.rotate(angle)

        # Обработка нажатых клавиш для управления кораблем.
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_a]:
            self.x -= self.speed
            self.rect.centerx = self.x
        elif key_state[pygame.K_d]:
            self.x += self.speed
            self.rect.centerx = self.x
        if key_state[pygame.K_w]:
            self.y -= self.speed
            self.rect.centery = self.y
        elif key_state[pygame.K_s]:
            self.y += self.speed
            self.rect.centery = self.y

        # Обработка стрельбы игрока.
        mouse_state = pygame.mouse.get_pressed()
        if mouse_state[0] and self.health > 0:
            self.shoot()

    def draw_health_bar(self, screen: pygame.Surface) -> None:
        """
        Отрисовка полоски здоровья игрока.

        :param screen: Экран, на который нужно рисовать.
        """

        if self.health < 0:
            self.health = 0
        BAR_LENGTH = 60
        BAR_HEIGHT = 10
        # Получаем оставшееся здоровье игрока в процентах.
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
        pygame.draw.rect(screen, settings.Collors.GREEN.value, fill_rect)
        pygame.draw.rect(screen, settings.Collors.WHITE.value, outline_rect, 2)

    def rotate(self, new_rot: float) -> None:
        """
        Поврот спрайта игрока.

        :param new_rot: Новое значение в радианах.
        """

        self.rot = new_rot
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(settings.Collors.BLACK.value)
        self.rect = self.image.get_rect(center=old_center)

    def shoot(self) -> None:
        """Стрельба игрока"""

        # Держим правильную скорость стрельбы игрока.
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            x = self.rect.centerx - self.radius * math.sin(math.radians(self.rot))
            y = self.rect.centery - self.radius * math.cos(math.radians(self.rot))
            bullet = Bullet(skin=self.bullet_skin, x=x, y=y,
                            angle=math.radians(self.rot), damage=self.damage)
            GameObjects().bullets_group.add(bullet)
            pygame.mixer.Channel(0).play(settings.shoot_sound)
