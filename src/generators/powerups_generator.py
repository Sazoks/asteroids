from levels.abstract_managing_levels import ManagingLevels


class PowerupsGenerator(ManagingLevels):
    """
    Класс генератора усилений.
    """

    def __init__(self) -> None:
        ...

    def generate(self):
        

    def get_current_level(self) -> int:
        ...

    def level_up(self) -> None:
        ...

    def level_down(self) -> None:
        ...

    def reset_levels(self) -> None:
        ...
