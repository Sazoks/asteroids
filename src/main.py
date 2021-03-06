"""
Главный модуль программы.

Содержит точку входа в программу.
"""


import pygame

import settings
from player import Player
from global_game_objects import GlobalGameObjects
from asteroids.asteroid import AsteroidType
from collider.collide_resolver import CollideResolver
from collider.collide_resolve_factory import CollideResolveFactory
from levels.level import Level
from levels.levels_manager import LevelsManager
from generators.asteroids_generator import AsteroidsGenerator
from generators.powerups_generator import PowerupsGenerator


def main():
    """
    Главная функция программы.

    Является точкой входа в программу.
    """

    # Инициализируем единственный экземпляр класса игровых объектов.
    # Этот класс служит глобальной точкой получения общих игровых объектов
    # по типу групп спрайтов, экрана игры и прочего.
    game_objects = GlobalGameObjects()

    # Создаем и настраиваем коллайдер.
    # Коллайдер использует внутри себя фабрику решений, которая по типам
    # столкнувшихся объектов выбирает нужное решение.
    collide_resolver = CollideResolver(
        collide_resolve_factory=CollideResolveFactory(),
    )

    # Создаем список уровней.
    levels = [Level(score=100 * (i + 1)) for i in range(100)]

    # Создаем менеджер уровней. Менеджер отвечает за контроль уровня игры
    # и контролирует уровни зарегестрированных в нем игровых объектов по типу
    # генераторов.
    levels_manager = LevelsManager(levels=levels)

    # Создаем типы астероидов. На основе этих объектов генератор астероидов
    # будет генерировать астероиды.
    asteroid_types = [
        AsteroidType(
            min_max_radius=(10, 20),
            min_max_speed=(380, 480),
            skins=settings.asteroid_skins['tiny'],
        ),
        AsteroidType(
            min_max_radius=(21, 30),
            min_max_speed=(340, 430),
            skins=settings.asteroid_skins['small'],
        ),
        AsteroidType(
            min_max_radius=(31, 40),
            min_max_speed=(280, 360),
            skins=settings.asteroid_skins['medium'],
        ),
        AsteroidType(
            min_max_radius=(41, 70),
            min_max_speed=(250, 310),
            skins=settings.asteroid_skins['large'],
        ),
    ]
    # Создаем генератор астероидов.
    asteroid_generator = AsteroidsGenerator(
        start_frequency=2500,
        end_frequency=150,
        asteroid_types=asteroid_types,
        max_level=len(levels),
    )
    # Регистрируем генератор астероидов в менджере уровней.
    levels_manager.register_object(asteroid_generator)

    # Создаем генератор усилений.
    powerups_generator = PowerupsGenerator(
        start_frequency=10000,
        end_frequency=4000,
        max_level=len(levels),
    )
    levels_manager.register_object(powerups_generator)

    # Создаем игрока.
    player = Player(
        skin=settings.player_skin,
        bullet_skin=settings.bullet_skin,
        health=200, speed=2.7, damage=22,
        radius=25, shoot_delay=420, score=0,
    )
    game_objects.players_group.add(player)
    # Регистрируем игрока в менджере активных усилений.
    game_objects.active_powerups_manager.register_player(player)

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

        # ============================================
        # Обновление.
        # Проверяем, нужно ли повышать уровень игры.
        if levels_manager.level_complete(player.score):
            levels_manager.level_up()

        # Контролируем работу активных усилений на игрока.
        game_objects.active_powerups_manager.control_powerups()

        # Генерируем новый астероид.
        new_asteroid = asteroid_generator.generate()
        if new_asteroid is not None:
            game_objects.asteroids_group.add(new_asteroid)

        # Генерируем новое усиление.
        new_powerup = powerups_generator.generate()
        if new_powerup is not None:
            game_objects.powerups_group.add(new_powerup)

        # Стрельба игрока.
        new_player_bullet = player.shoot()
        if new_player_bullet is not None:
            pygame.mixer.Channel(0).play(settings.shoot_sound)
            game_objects.bullets_group.add(new_player_bullet)

        # Добавляем в квадродерево астероиды.
        # FIXME:
        #  Сделать удаление объектов из квадродерева вместо полного отчищения.
        game_objects.quadtree.clear()
        # Добавляем в квадродерево усиления.
        for powerup in game_objects.powerups_group:
            game_objects.quadtree.add(powerup)
        # Добавляем в квадродерево астероиды.
        for obj in game_objects.asteroids_group:
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
        game_objects.powerups_group.update()
        game_objects.explosions_group.update()
        game_objects.asteroids_group.update()
        player.update()
        game_objects.bullets_group.update()

        # Обновляем текст со счетом.
        score_text = settings.main_font.render(
            f'Score: {int(player.score)}',
            True,
            settings.Collors.WHITE.value,
        )
        # Обновляем уровень.
        current_level_text = settings.main_font.render(
            f'Level: {levels_manager.get_current_level()}',
            True,
            settings.Collors.WHITE.value,
        )

        # ============================================
        # Отрисовка спрайтов.
        # Отрисовка заднего фона.
        for y in range(0, settings.HEIGHT, settings.background.get_height()):
            for x in range(0, settings.WIDTH, settings.background.get_width()):
                settings.screen.blit(settings.background, (x, y))

        # Отрисовка всех спрайтов и квадродерева.
        # Отрисовка игрока и его здоровья.
        game_objects.powerups_group.draw(settings.screen)
        game_objects.players_group.draw(settings.screen)
        if player.health > 0:
            player.draw_health_bar(settings.screen)

        # Отрисовка времени действия усилений.
        game_objects.active_powerups_manager.draw_time_action_powerups()

        # Отрисовка всех пуль.
        game_objects.bullets_group.draw(settings.screen)

        # Отрисовка астероидов и их здоровья.
        game_objects.asteroids_group.draw(settings.screen)
        for astr in game_objects.asteroids_group:
            astr.draw_health_bar(settings.screen)

        # Отрисовка всех взрывов.
        game_objects.explosions_group.draw(settings.screen)

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
