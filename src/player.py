import pygame
import math
from typing import Optional

import settings
from bullets.bullet import Bullet


class Player(pygame.sprite.Sprite):
    """Класс игрока"""

    def __init__(
            self,
            skin: pygame.Surface,
            bullet_skin: pygame.Surface,
            health: int,
            speed: float,
            damage: int,
            radius: float,
            shoot_delay: int,
            score: int,
    ) -> None:
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

        self.__bullet_skin = bullet_skin

        self.radius = radius
        self.image_orig = pygame.transform.scale(
            skin,
            (self.radius * 2, self.radius * 2),
        )
        self.image_orig.set_colorkey(settings.Collors.BLACK.value)
        self.image = self.image_orig.copy()

        self.__pos_x = settings.WIDTH // 2
        self.__pos_y = settings.HEIGHT // 2
        self.__speed = speed
        self.__health = health
        self.__source_health = health
        self.__score = score

        self.__shoot_delay = shoot_delay
        self.__last_shot = pygame.time.get_ticks()
        self.__damage = damage

        # Прямоугольник игрового объекта.
        self.rect = self.image.get_rect(center=(self.__pos_x, self.__pos_y))

        # Параметры для вращения.
        self.rot = 0

    def update(self) -> None:
        """Метод обновления состояния игрока"""

        # Считываем координаты курсора.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.__pos_x, mouse_y - self.__pos_y
        # Поворачиваем спрайта игрока в сторону курсора.
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        self.rotate(angle)

        # Обработка нажатых клавиш для управления кораблем.
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_a]:
            self.__pos_x -= self.__speed
            self.rect.centerx = self.__pos_x
        elif key_state[pygame.K_d]:
            self.__pos_x += self.__speed
            self.rect.centerx = self.__pos_x
        if key_state[pygame.K_w]:
            self.__pos_y -= self.__speed
            self.rect.centery = self.__pos_y
        elif key_state[pygame.K_s]:
            self.__pos_y += self.__speed
            self.rect.centery = self.__pos_y

    def draw_health_bar(self, screen: pygame.Surface) -> None:
        """
        Отрисовка полоски здоровья игрока.

        :param screen: Экран, на который нужно рисовать.
        """

        if self.__health < 0:
            self.__health = 0
        BAR_LENGTH = 60
        BAR_HEIGHT = 10

        # Получаем оставшееся здоровье игрока в процентах.
        remaining_health_percent = self.__health * 100 / self.__source_health
        fill = remaining_health_percent * BAR_LENGTH / 100
        outline_rect = pygame.Rect(
            self.__pos_x - BAR_LENGTH // 2,
            self.__pos_y + self.radius + 5,
            BAR_LENGTH, BAR_HEIGHT,
        )
        fill_rect = pygame.Rect(
            self.__pos_x - BAR_LENGTH // 2,
            self.__pos_y + self.radius + 5,
            fill, BAR_HEIGHT,
        )

        # Отрисовка здоровья игрока цифрами.
        health_text = settings.health_font.render(
            f'{self.__health}xp',
            True,
            settings.Collors.WHITE.value,
        )
        settings.screen.blit(
            health_text,
            (self.__pos_x - BAR_LENGTH // 2 + BAR_LENGTH + 1,
             self.__pos_y + self.radius),
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

    def shoot(self) -> Optional[Bullet]:
        """
        Стрельба игрока.

        Вызывается на каждой итерации игрового цикла, проверяет, нажата ли
        клавиша стреьлбы, и если нажата, контролирует скорострельность.
        """

        # Обработка стрельбы игрока.
        mouse_state = pygame.mouse.get_pressed()
        if mouse_state[0] and self.__health > 0:
            # Держим правильную скорость стрельбы игрока.
            now = pygame.time.get_ticks()
            if now - self.__last_shot > self.__shoot_delay:
                self.__last_shot = now
                x = self.rect.centerx - self.radius * math.sin(math.radians(self.rot))
                y = self.rect.centery - self.radius * math.cos(math.radians(self.rot))
                bullet = Bullet(skin=self.__bullet_skin,
                                x=x, y=y,
                                angle=math.radians(self.rot),
                                damage=self.__damage)
                return bullet

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
    def shoot_delay(self) -> int:
        return self.__shoot_delay

    @shoot_delay.setter
    def shoot_delay(self, new_shoot_delay: int) -> None:
        self.__shoot_delay = new_shoot_delay

    @property
    def damage(self) -> int:
        return self.__damage

    @damage.setter
    def damage(self, new_damage: int) -> None:
        self.__damage = new_damage

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

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, new_score) -> None:
        self.__score = new_score
