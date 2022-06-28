import pygame
from typing import Dict

from player import Player
from powerups import Powerup


class ActivePowerupsManager:
    """
    Менеджер активных усилений для игроков.

    Отвечается за контроль действия усилений на игрока.
    """

    def __init__(self) -> None:
        """Инициализатор класса"""

        # Ключи словаря - id игроков, значения - словари с активными
        # усилениями. id таких словарей - типы усилений, значения -
        # объекты усилений.
        self.__managed_powerups: Dict[Player, Dict[type(Powerup), Powerup]] = {}

    def control_powerups(self) -> None:
        """
        Метод контроля усилений на игроков.

        На каждой итерации игрового цикла вызывается этот метод и
        инкрементирует время действия каждого усиления. Если время действия
        какого-либо усиления заканчивается, удаляет его из словаря активных
        усилений и больше не берет в расчет.
        """

        now = pygame.time.get_ticks()
        for player, powerups in self.__managed_powerups.items():
            # Список типов истекших усилений.
            expired_powerups = []

            for powerup in powerups.values():
                # Если прошедшее время с момента активации усиления не
                # превышает времени действия усиления, продолжаем усиливать
                # игрока. Иначе возвращаем парметр игрока и удаляем усиление
                # из словаря активных усилений текущего игрока.
                if now - powerup.get_activate_time() > powerup.get_time_action():
                    powerup.rollback_param(player)
                    expired_powerups.append(type(powerup))

            # Удаляем истекшие усиления, если они есть.
            # FIXME: Возможно, есть лучшее решение для массового удаления
            #  элементов из словаря.
            self.__managed_powerups[player] = {
                type_powerup: powerup
                for type_powerup, powerup in self.__managed_powerups[player].items()
                if type_powerup not in expired_powerups
            }

    def register_player(self, player: Player) -> None:
        """
        Регистрация игрока для управления усилениями на него.

        :param player: Объект игрока.
        """

        if player not in self.__managed_powerups.keys():
            self.__managed_powerups[player] = {}

    def unregister_player(self, player: Player) -> None:
        """
        Преркащения управления усилениями на игрока.

        :param player: Объект игрока.
        """

        if player in self.__managed_powerups.keys():
            self.__managed_powerups.pop(player)

    def add_powerup(self, player: Player, new_powerup: Powerup) -> None:
        """
        Метод добавления нового активного усиления для игрока.

        :param player: Объект игрока.
        :param new_powerup: Новое усиление.
        """

        type_powerup = type(new_powerup)
        # Получаем список активных усилений текущего игрока.
        current_powerups = self.__managed_powerups[player]

        # Если усиления такого типа нет в словаре активных усилений текущего
        # игрока, добавляем его туда и оказываем эффект.
        if type_powerup not in current_powerups.keys():
            current_powerups[type_powerup] = new_powerup
            current_powerups[type_powerup].influence(player)
        # Активируем усиления, продляя время его действия.
        current_powerups[type_powerup].activate()
