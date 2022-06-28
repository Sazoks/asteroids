import pygame
import random
from typing import Tuple

import settings
from bullets.bullet import Bullet
from animations.explosion import Explosion
from global_game_objects import GlobalGameObjects
from asteroids.asteroid import Asteroid
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
    def get_object_types() -> tuple:
        """
        Геттер для получения имен классов объектов, столкновения
        которых может решать этот резолвер.

        :return:
            Кортеж имен классов объектов, которые могут сталкиваться.
        """

        return Asteroid, Bullet

    def resolve(self) -> None:
        """Обработка столкновения двух объектов"""

        if pygame.sprite.collide_mask(self.__bullet, self.__asteroid):
            game_objects = GlobalGameObjects()

            self.__bullet.kill()
            game_objects.quadtree.remove(self.__bullet)

            self.__asteroid.health -= self.__bullet.damage

            # Анимация взрыва при попадании в астероид.
            random.choice(settings.expl_sounds).play()
            exp = Explosion(self.__bullet.rect.center, self.__bullet.height)
            game_objects.explosions_group.add(exp)

            if self.__asteroid.health <= 0:
                self.__asteroid.kill()
                game_objects.quadtree.remove(self.__asteroid)

                # Начисляем игроку очки.
                if len(game_objects.players_group.sprites()) > 0:
                    game_objects.players_group.sprites()[0].score += self.__asteroid.reward

                # Разбиваем астероид на два меньших.
                if self.__asteroid.radius >= self.__asteroid.get_min_size():
                    new_asteroids = self.__asteroid.split_asteroid()
                    for asteroid in new_asteroids:
                        game_objects.asteroids_group.add(asteroid)

                # Создаем анимацию взрыва на месте астероида.
                random.choice(settings.expl_sounds).play()
                exp = Explosion(self.__asteroid.rect.center,
                                self.__asteroid.radius * 2.2)
                game_objects.explosions_group.add(exp)
