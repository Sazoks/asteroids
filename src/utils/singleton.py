class Singleton(type):
    """Мета-класс, реализующий паттерн Singleton"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Дандер-метод для вызова объекта"""

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
