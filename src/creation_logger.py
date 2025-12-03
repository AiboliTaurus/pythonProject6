class CreationLogger:
    """
    Миксин для логирования создания объектов.
    Выводит в консоль информацию о классе и переданных параметрах при инициализации.
    """

    def __init__(self, *args, **kwargs):
        # Получаем имя класса
        class_name = self.__class__.__name__

        # Формируем строку с позиционными аргументами
        args_str = ', '.join(repr(arg) for arg in args)

        # Формируем строку с именованными аргументами (если есть)
        kwargs_str = ', '.join(f"{k}={repr(v)}" for k, v in kwargs.items())

        # Объединяем все параметры
        if args_str and kwargs_str:
            params_str = f"{args_str}, {kwargs_str}"
        elif args_str:
            params_str = args_str
        else:
            params_str = kwargs_str

        # Выводим информацию о создании
        print(f"{class_name}({params_str})")
