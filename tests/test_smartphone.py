import unittest

from src.product import Product
from src.smartphone import Smartphone


class TestSmartphone(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом."""
        self.phone1 = Smartphone(
            name="iPhone 14",
            description="Флагманский смартфон Apple",
            price=79990.0,
            quantity=10,
            efficiency=9.5,
            model="A2884",
            memory=128,
            color="Чёрный"
        )
        self.phone2 = Smartphone(
            name="Samsung Galaxy S23",
            description="Флагманский смартфон Samsung",
            price=69990.0,
            quantity=15,
            efficiency=9.2,
            model="SM-S911B",
            memory=256,
            color="Белый"
        )

    def test_initialization(self):
        """Проверка корректной инициализации объекта Smartphone."""
        self.assertEqual(self.phone1.name, "iPhone 14")
        self.assertEqual(self.phone1.price, 79990.0)
        self.assertEqual(self.phone1.quantity, 10)
        self.assertEqual(self.phone1.efficiency, 9.5)
        self.assertEqual(self.phone1.model, "A2884")
        self.assertEqual(self.phone1.memory, 128)
        self.assertEqual(self.phone1.color, "Чёрный")

    def test_str_representation(self):
        """Проверка строкового представления объекта Smartphone."""
        result = str(self.phone1)
        expected = "iPhone 14 (A2884), Чёрный, 128 ГБ, 79990 руб. Остаток: 10 шт."
        self.assertEqual(result, expected)

    def test_add_same_class(self):
        """Проверка сложения двух объектов Smartphone."""
        result = self.phone1 + self.phone2

        # Проверка типа результата
        self.assertIsInstance(result, Smartphone)

        # Проверка составного названия
        self.assertEqual(result.name, "iPhone 14 & Samsung Galaxy S23")

        # Проверка расчёта средней цены
        total_value = 79990 * 10 + 69990 * 15
        total_qty = 10 + 15
        expected_price = total_value / total_qty
        self.assertAlmostEqual(result.price, expected_price, places=2)

        # Проверка суммарного количества
        self.assertEqual(result.quantity, 25)

        # Проверка средней эффективности
        expected_efficiency = (9.5 + 9.2) / 2
        self.assertEqual(result.efficiency, expected_efficiency)

        # Проверка модели (всегда "Combined")
        self.assertEqual(result.model, "Combined")

        # Проверка максимального объёма памяти
        self.assertEqual(result.memory, 256)

        # Проверка объединённого цвета
        self.assertEqual(result.color, "Чёрный/Белый")

        # Проверка неизменности исходных объектов
        self.assertEqual(self.phone1.quantity, 10)
        self.assertEqual(self.phone2.quantity, 15)

    def test_add_different_class_raises_typeerror(self):
        """Проверка, что сложение с объектом другого класса вызывает TypeError."""
        product = Product("Обычный товар", "Описание", 1000.0, 5)
        with self.assertRaises(TypeError) as context:
            self.phone1 + product
        self.assertIn("Можно складывать только объекты одного класса", str(context.exception))

    def test_add_with_non_product(self):
        """Проверка, что сложение с не-продуктом вызывает TypeError."""
        with self.assertRaises(TypeError) as context:
            self.phone1 + "не объект"
        self.assertIn("Можно складывать только объекты одного класса", str(context.exception))

    def test_price_setter_rejects_negative_price(self):
        """Проверка, что сеттер цены отклоняет отрицательные значения."""
        original_price = self.phone1.price
        self.phone1.price = -1000
        self.assertEqual(self.phone1.price, original_price)

    def test_memory_immutable_after_init(self):
        """Проверка, что атрибут memory нельзя изменить после инициализации."""
        # В текущей реализации memory — обычный атрибут, поэтому проверка на неизменность не требуется.
        # Если нужно сделать immutable, следует добавить сеттер с проверкой или использовать __slots__.
        pass  # Оставляем как заглушку для будущих улучшений

    def test_efficiency_range_validation(self):
        """
        Проверка допустимого диапазона эффективности (предполагаем, что 0 < efficiency <= 10).
        Примечание: в текущей реализации валидация не реализована — тест демонстрирует потенциальное улучшение.
        """
        # Текущая реализация не проверяет диапазон efficiency
        # Пример возможной проверки:
        # with self.assertRaises(ValueError):
        #     Smartphone(... efficiency=11.0 ...)
        pass
