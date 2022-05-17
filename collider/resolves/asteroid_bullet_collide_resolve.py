import pygame
import random
from typing import (
    Tuple,
    List,
)

import settings
from bullet import Bullet
from asteroid import Asteroid
from explosion import Explosion
from .abstract_collide_resolve import AbstractCollideResolve


class AsteroidBulletCollideResolve(AbstractCollideResolve):
    """Класс для разрешения коллизий игрока с астероидом"""

    def __init__(self, asteroid: Asteroid, bullet: Bullet) -> None:
        """
        Инициализатор класса.

        :param asteroid: Объект астероида.
        :param bullet: Снаряд игрока.
        """

        self.__asteroid = asteroid
        self.__bullet = bullet

    @staticmethod
    def get_object_types() -> Tuple[str, str]:
        """
        Геттер для получения имен классов объектов, столкновения
        которых может решать этот резолвер.

        :return:
            Кортеж имен классов объектов, которые могут сталкиваться.
        """

        return Asteroid.__name__, Bullet.__name__

    def resolve(self) -> None:
        if pygame.sprite.collide_mask(self.__bullet, self.__asteroid):
            self.__bullet.kill()
            settings.quadtree.remove(self.__bullet)

            self.__asteroid.health -= self.__bullet.damage

            # Анимация взрыва при попадании в астероид.
            random.choice(settings.expl_sounds).play()
            exp = Explosion(self.__bullet.rect.center, self.__bullet.height)
            settings.explosions_sprites.add(exp)

            if self.__asteroid.health <= 0:
                self.__asteroid.kill()
                settings.quadtree.remove(self.__asteroid)

                # Начисляем игроку очки.
                if len(settings.players_group.sprites()) > 0:
                    settings.players_group.sprites()[0].score += self.__asteroid.reward

                # Разбиваем астероид на два меньших.
                if self.__asteroid.radius >= self.__asteroid.get_min_size():
                    new_asteroids = self.__asteroid.split_asteroid()
                    for asteroid in new_asteroids:
                        settings.asteroids_sprites.add(asteroid)

                # Создаем анимацию взрыва на месте астероида.
                random.choice(settings.expl_sounds).play()
                exp = Explosion(self.__asteroid.rect.center,
                                self.__asteroid.radius * 2.2)
                settings.explosions_sprites.add(exp)
