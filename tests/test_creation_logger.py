import sys
from io import StringIO

from src.creation_logger import CreationLogger


class TestCreationLogger:
    def test_only_args(self):
        """Тест: только позиционные аргументы (*args). Должен выполниться elif args_str."""
        class TestClass(CreationLogger):
            pass

        # Сохраняем stdout для перехвата print
        captured_output = StringIO()
        sys.stdout = captured_output

        obj = TestClass("arg1", "arg2", 123)
        output = captured_output.getvalue().strip()

        # Восстанавливаем stdout
        sys.stdout = sys.__stdout__

        # Проверяем, что объект создан и относится к классу TestClass
        assert isinstance(obj, TestClass)

        # Исправляем ожидаемый вывод — добавляем одинарные кавычки вокруг строк
        expected_output = "TestClass('arg1', 'arg2', 123)"
        assert output == expected_output

    def test_only_kwargs(self):
        """Тест: только именованные аргументы (**kwargs). Должен выполниться else."""
        class TestClass(CreationLogger):
            pass

        captured_output = StringIO()
        sys.stdout = captured_output

        obj = TestClass(kw1="value1", kw2="value2", kw3=456)
        output = captured_output.getvalue().strip()

        # Добавляем проверку объекта
        assert isinstance(obj, TestClass)

        sys.stdout = sys.__stdout__

        # Ожидаемый вывод уже корректно содержит кавычки для строковых значений
        expected_output = "TestClass(kw1='value1', kw2='value2', kw3=456)"
        assert output == expected_output

    def test_args_and_kwargs(self):
        """Тест: и позиционные, и именованные аргументы. Должен выполниться if args_str and kwargs_str."""
        class TestClass(CreationLogger):
            pass

        captured_output = StringIO()
        sys.stdout = captured_output

        obj = TestClass("pos1", "pos2", kw1="val1", kw2="val2")
        output = captured_output.getvalue().strip()

        # Добавляем проверку объекта
        assert isinstance(obj, TestClass)

        sys.stdout = sys.__stdout__

        # Исправляем ожидаемый вывод — добавляем одинарные кавычки вокруг строковых позиционных аргументов
        expected_output = "TestClass('pos1', 'pos2', kw1='val1', kw2='val2')"
        assert output == expected_output

    def test_no_arguments(self):
        """Тест: отсутствие аргументов. Должен корректно обработать пустой вызов."""
        class TestClass(CreationLogger):
            pass

        captured_output = StringIO()
        sys.stdout = captured_output

        obj = TestClass()
        output = captured_output.getvalue().strip()

        # Добавляем проверку объекта
        assert isinstance(obj, TestClass)

        sys.stdout = sys.__stdout__

        expected_output = "TestClass()"
        assert output == expected_output

    def test_complex_args(self):
        """Тест: сложные типы данных в аргументах (списки, словари)."""
        class TestClass(CreationLogger):
            pass

        captured_output = StringIO()
        sys.stdout = captured_output

        obj = TestClass([1, 2, 3], {"key": "value"}, name="test", data=[4, 5])
        output = captured_output.getvalue().strip()

        # Добавляем проверку объекта
        assert isinstance(obj, TestClass)

        sys.stdout = sys.__stdout__

        # Проверяем, что все аргументы корректно отображены (включая кавычки)
        assert "[1, 2, 3]" in output
        assert "{'key': 'value'}" in output
        assert "name='test'" in output
        assert "[4, 5]" in output
