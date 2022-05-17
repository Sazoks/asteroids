import pygame
from pathlib import Path

import settings
from asteroid import (
    Asteroid,
    AsteroidType,
)
from player import Player
from collider.collide_resolve_factory import CollideResolveFactory
from collider.collide_resolver import CollideResolver
from asteroid_level_manager import AsteroidLevelManager


def main():
    """Главная функция программы"""

    # Создаем и настраиваем коллайдер.
    collide_resolver = CollideResolver(collide_resolve_factory=CollideResolveFactory())

    # Создаем типы астероидов.
    asteroid_types = [
        AsteroidType(
            min_max_radius=(10, 20),
            min_max_speed=(250, 350),
            skins=settings.asteroid_skins['tiny'],
        ),
        AsteroidType(
            min_max_radius=(21, 30),
            min_max_speed=(210, 300),
            skins=settings.asteroid_skins['small'],
        ),
        AsteroidType(
            min_max_radius=(31, 40),
            min_max_speed=(150, 230),
            skins=settings.asteroid_skins['medium'],
        ),
        AsteroidType(
            min_max_radius=(41, 70),
            min_max_speed=(120, 180),
            skins=settings.asteroid_skins['large'],
        ),
    ]
    # Создаем менеджер астероидов.
    asteroid_manager = AsteroidLevelManager(
        start_frequency=2500,
        frequency_delta=450,
        asteroid_types=asteroid_types,
        score_levels=[500, 1000, 2000, 5000, 10000],
    )

    # Создаем игрока.
    player = Player(skin=settings.player_skin,
                    bullet_skin=settings.bullet_skin,
                    health=200, speed=2.5, damage=25,
                    radius=25, shoot_delay=300, score=5000)
    settings.players_group.add(player)

    # Цикл игры.
    running = True
    while running:
        # Держим цикл на правильной скорости.
        settings.clock.tick(settings.FPS)
        # Ввод процесса (события).
        for event in pygame.event.get():
            # Проверка события закрытия игры.
            if event.type == pygame.QUIT:
                running = False
            if player.health > 0 and event.type == pygame.MOUSEBUTTONDOWN \
                    and event.button == 1:
                player.shoot()

        # Менеджер астероидов контролирует создание астероидов,
        # их типы, их частоту появления.
        if asteroid_manager.level_complete(player.score):
            asteroid_manager.level_up()
        new_asteroid = asteroid_manager.start()
        if new_asteroid is not None:
            settings.asteroids_sprites.add(new_asteroid)

        # Обновление.
        # Добавляем в квадродерево астероиды.
        settings.quadtree.clear()
        for obj in settings.asteroids_sprites:
            settings.quadtree.add(obj)
        # Добавляем в квадродерево игрока.
        if player.health > 0:
            settings.quadtree.add(player)
        # Добавляем в квадродерево снаряды игрока.
        for bullet in settings.bullets_group:
            settings.quadtree.add(bullet)

        # Решение коллизий.
        # Выбираем все листы дерева, где больше 1 элемента, и проверяем
        # на наличие коллизий. Если есть - решаем их.
        collision_nodes = settings.quadtree.get_collision_nodes()
        for node in collision_nodes:
            node_objects = node.get_data()
            for i in range(len(node_objects) - 1):
                for k in range(i + 1, len(node_objects)):
                    collide_resolver.resolve(node_objects[i], node_objects[k])

        # Обновляем все спрайты.
        settings.explosions_sprites.update()
        settings.asteroids_sprites.update()
        player.update()
        settings.bullets_group.update()
        # Обновляем текст со счетом.
        score_text = settings.my_font.render(f'Score: {int(player.score)}', True,
                                             settings.Collors.WHITE.value)
        # Обновляем уровень.
        current_level_text = settings.my_font.render(
            f'Level: {asteroid_manager.get_current_level()}',
            True, settings.Collors.WHITE.value,
        )

        # Отрисовка спрайтов.
        # Отрисовка заднего фона.
        for y in range(0, settings.HEIGHT, settings.background.get_height()):
            for x in range(0, settings.WIDTH, settings.background.get_width()):
                settings.screen.blit(settings.background, (x, y))

        # Отрисовка всех спрайтов и квадродерева.
        # Отрисовка игрока и его здоровья.
        settings.players_group.draw(settings.screen)
        if player.health > 0:
            player.draw_health_bar(settings.screen)
        # Отрисовка всех пуль.
        settings.bullets_group.draw(settings.screen)
        # Отрисовка астероидов и их здоровья.
        settings.asteroids_sprites.draw(settings.screen)
        for astr in settings.asteroids_sprites:
            astr.draw_health_bar(settings.screen)
        # Отрисовка всех взрывов.
        settings.explosions_sprites.draw(settings.screen)
        # Отрисовка квадродерева.
        # settings.quadtree.draw_quadtree(settings.screen)

        # Отрисовка счета игрока.
        settings.screen.blit(score_text, (10, settings.HEIGHT - 50))

        # Отрисовка уровня.
        settings.screen.blit(current_level_text, (10, settings.HEIGHT - 90))

        # После отрисовки всего, переворачиваем экран.
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
