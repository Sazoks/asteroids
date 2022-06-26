import pygame
import random
from typing import Tuple

import settings
from player import Player
from explosion import Explosion
from game_objects import GameObjects
from asteroids.asteroid import Asteroid
from .abstract_collide_resolve import AbstractCollideResolve


class AsteroidPlayerCollideResolve(AbstractCollideResolve):
    """Класс для разрешения коллизий игрока с астероидом"""

    def __init__(self, player: Player, asteroid: Asteroid) -> None:
        """
        Инициализатор класса.

        :param player: Объект игрока.
        :param asteroid: Объект астероида.
        """

        self.__player = player
        self.__asteroid = asteroid

    @staticmethod
    def get_object_types() -> Tuple[str, str]:
        """
        Геттер для получения имен классов объектов, столкновения
        которых может решать этот резолвер.

        :return:
            Кортеж имен классов объектов, которые могут сталкиваться.
        """

        return Player.__name__, Asteroid.__name__

    def resolve(self) -> None:
        """Обработка столкновения двух объектов"""

        if pygame.sprite.collide_circle(self.__player, self.__asteroid):
            game_objects = GameObjects()

            self.__player.health -= self.__asteroid.radius
            if self.__player.health <= 0:
                self.__player.health = 0
                self.__player.kill()
                game_objects.quadtree.remove(self.__player)

                # Создаем анимацию взрыва на месте игрока.
                settings.chunky_expl.play()
                exp = Explosion(self.__player.rect.center,
                                self.__player.radius * 15,
                                frame_rate=150)
                game_objects.explosions_sprites.add(exp)

            self.__asteroid.kill()
            game_objects.quadtree.remove(self.__asteroid)
            if self.__asteroid.radius >= self.__asteroid.get_min_size():
                new_asteroids = self.__asteroid.split_asteroid()
                for asteroid in new_asteroids:
                    game_objects.asteroids_sprites.add(asteroid)

            # Создаем анимацию взрыва на месте астероида.
            random.choice(settings.expl_sounds).play()
            exp = Explosion(self.__asteroid.rect.center, self.__asteroid.radius * 2.2)
            game_objects.explosions_sprites.add(exp)
