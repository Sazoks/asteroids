import pygame

import settings
from player import Player
from game_objects import GameObjects
from src.asteroids.asteroid import AsteroidType
from collider.collide_resolver import CollideResolver
from collider.collide_resolve_factory import CollideResolveFactory
from src.asteroids.asteroids_manager import AsteroidsManager


def main():
    """Главная функция программы"""

    # Инициализируем единственный экземпляр класса игровых объектов.
    # Этот класс служит глобальной точкой получения общих игровых объектов
    # по типу групп спрайтов, экрана игры и прочего.
    game_objects = GameObjects()

    # Создаем и настраиваем коллайдер.
    # Коллайдер использует внутри себя фабрику решений, которая по типам
    # столкнувшихся объектов выбирает нужное решение.
    collide_resolver = CollideResolver(
        collide_resolve_factory=CollideResolveFactory()
    )

    # Создаем типы астероидов. На основе этих объектов менеджер астероидов
    # будет генерировать астероиды.
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
    asteroid_manager = AsteroidsManager(
        start_frequency=2500,
        frequency_delta=450,
        asteroid_types=asteroid_types,
        score_levels=[500, 1000, 2000, 5000, 10000],
    )
    # Создаем игрока.
    player = Player(
        skin=settings.player_skin,
        bullet_skin=settings.bullet_skin,
        health=200, speed=2.7, damage=18,
        radius=25, shoot_delay=300, score=0,
    )
    game_objects.players_group.add(player)

    # Игровой цикл.
    running = True
    while running:
        # Держим цикл на правильной скорости.
        settings.clock.tick(settings.FPS)

        # Получений произошедших событий из списка событий игры.
        for event in pygame.event.get():
            # Проверка события закрытия игры.
            if event.type == pygame.QUIT:
                running = False
            # Обработка стельбы игрока.
            if player.health > 0 and event.type == pygame.MOUSEBUTTONDOWN \
                    and event.button == 1:
                player.shoot()

        # ============================================
        # Менеджер астероидов контролирует создание астероидов,
        # их типы, их частоту появления.
        if asteroid_manager.level_complete(player.score):
            asteroid_manager.level_up()
        new_asteroid = asteroid_manager.start()
        if new_asteroid is not None:
            game_objects.asteroids_sprites.add(new_asteroid)

        # Обновление.
        # Добавляем в квадродерево астероиды.
        game_objects.quadtree.clear()
        for obj in game_objects.asteroids_sprites:
            game_objects.quadtree.add(obj)
        # Добавляем в квадродерево игрока.
        if player.health > 0:
            game_objects.quadtree.add(player)
        # Добавляем в квадродерево снаряды игрока.
        for bullet in game_objects.bullets_group:
            game_objects.quadtree.add(bullet)

        # Решение коллизий.
        # Выбираем все листы дерева, где больше 1 элемента, и проверяем
        # на наличие коллизий. Если есть - решаем их.
        collision_nodes = game_objects.quadtree.get_collision_nodes()
        for node in collision_nodes:
            node_objects = node.get_data()
            for i in range(len(node_objects) - 1):
                for k in range(i + 1, len(node_objects)):
                    collide_resolver.resolve(node_objects[i], node_objects[k])

        # Обновляем все спрайты.
        game_objects.explosions_sprites.update()
        game_objects.asteroids_sprites.update()
        player.update()
        game_objects.bullets_group.update()
        # Обновляем текст со счетом.
        score_text = settings.my_font.render(f'Score: {int(player.score)}', True,
                                             settings.Collors.WHITE.value)
        # Обновляем уровень.
        current_level_text = settings.my_font.render(
            f'Level: {asteroid_manager.get_current_level()}',
            True, settings.Collors.WHITE.value,
        )

        # ============================================
        # Отрисовка спрайтов.
        # Отрисовка заднего фона.
        for y in range(0, settings.HEIGHT, settings.background.get_height()):
            for x in range(0, settings.WIDTH, settings.background.get_width()):
                settings.screen.blit(settings.background, (x, y))

        # Отрисовка всех спрайтов и квадродерева.
        # Отрисовка игрока и его здоровья.
        game_objects.players_group.draw(settings.screen)
        if player.health > 0:
            player.draw_health_bar(settings.screen)
        # Отрисовка всех пуль.
        game_objects.bullets_group.draw(settings.screen)
        # Отрисовка астероидов и их здоровья.
        game_objects.asteroids_sprites.draw(settings.screen)
        for astr in game_objects.asteroids_sprites:
            astr.draw_health_bar(settings.screen)
        # Отрисовка всех взрывов.
        game_objects.explosions_sprites.draw(settings.screen)
        # Отрисовка квадродерева.
        game_objects.quadtree.draw_quadtree(settings.screen)

        # Отрисовка счета игрока.
        settings.screen.blit(score_text, (10, settings.HEIGHT - 50))

        # Отрисовка уровня.
        settings.screen.blit(current_level_text, (10, settings.HEIGHT - 90))

        # После отрисовки всего, переворачиваем экран.
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
