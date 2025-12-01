import unittest

from src.lawngrass import LawnGrass
from src.product import Product


class TestLawnGrass(unittest.TestCase):

    def setUp(self):
        """
        Подготовка тестовых данных перед каждым тестом.
        Создаёт два экземпляра LawnGrass с различными характеристиками.
        """
        self.grass1 = LawnGrass(
            name="Газонная трава Премиум",
            description="Высококачественная трава для газона",
            price=500.0,
            quantity=20,
            country="Россия",
            germination_period="7–10 дней",
            color="Изумрудный"
        )
        self.grass2 = LawnGrass(
            name="Трава выносливая",
            description="Устойчива к засухе",
            price=450.0,
            quantity=15,
            country="США",
            germination_period="5–8 дней",
            color="Тёмно‑зелёный"
        )

    def test_initialization(self):
        """
        Проверка корректной инициализации объекта LawnGrass.
        Убеждается, что все атрибуты установлены верно при создании экземпляра.
        """
        self.assertEqual(self.grass1.name, "Газонная трава Премиум")
        self.assertEqual(self.grass1.price, 500.0)
        self.assertEqual(self.grass1.quantity, 20)
        self.assertEqual(self.grass1.country, "Россия")
        self.assertEqual(self.grass1.germination_period, "7–10 дней")
        self.assertEqual(self.grass1.color, "Изумрудный")

    def test_str_representation(self):
        """
        Проверка строкового представления объекта LawnGrass.
        Убеждается, что метод __str__ возвращает строку, содержащую ключевые атрибуты объекта.
        """
        result = str(self.grass1)
        self.assertIn("Газонная трава Премиум", result)
        self.assertIn("Изумрудный", result)
        self.assertIn("Россия", result)
        self.assertIn("7–10 дней", result)
        self.assertIn("500 руб.", result)
        self.assertIn("20 шт.", result)

    def test_add_same_class(self):
        """
        Проверка сложения двух объектов LawnGrass.
        Тестирует:
        - возврат объекта того же класса;
        - формирование составного названия;
        - расчёт средней цены;
        - суммирование количества;
        - объединение атрибутов;
        - неизменность исходных объектов.
        """
        result = self.grass1 + self.grass2

        self.assertIsInstance(result, LawnGrass)
        self.assertEqual(result.name, "Газонная трава Премиум & Трава выносливая")

        total_value = 500 * 20 + 450 * 15
        total_qty = 20 + 15
        expected_price = total_value / total_qty
        self.assertAlmostEqual(result.price, expected_price, places=2)

        self.assertEqual(result.quantity, 35)
        self.assertEqual(result.country, "Россия/США")
        self.assertEqual(result.germination_period, "avg")
        self.assertEqual(result.color, "Изумрудный/Тёмно‑зелёный")

        # Проверка на неизменность исходных объектов
        self.assertEqual(self.grass1.quantity, 20)
        self.assertEqual(self.grass2.quantity, 15)

    def test_add_different_class_raises_typeerror(self):
        """
        Проверка, что сложение с объектом другого класса (Product) вызывает TypeError.
        Убеждается, что сообщение исключения содержит ожидаемый текст.
        """
        product = Product("Обычный товар", "Описание", 100.0, 10)
        with self.assertRaises(TypeError) as context:
            self.grass1 + product
        self.assertIn("Можно складывать только объекты одного класса", str(context.exception))

    def test_add_with_non_product(self):
        """
        Проверка, что сложение с не-продуктом (строкой) вызывает TypeError.
        Убеждается, что сообщение исключения содержит ожидаемый текст.
        """
        with self.assertRaises(TypeError) as context:
            self.grass1 + "не объект"
        self.assertIn("Можно складывать только объекты одного класса", str(context.exception))

    def test_price_setter_rejects_negative_price(self):
        """
        Проверка, что сеттер цены отклоняет отрицательные значения.
        Убеждается, что при попытке установить отрицательную цену:
        - цена остаётся неизменной;
        - исключение не выбрасывается (сеттер только игнорирует значение).
        """
        original_price = self.grass1.price
        self.grass1.price = -100
        self.assertEqual(self.grass1.price, original_price)

    def test_price_setter_rejects_zero_price(self):
        """
        Проверка, что сеттер цены отклоняет нулевую цену.
        Убеждается, что при попытке установить цену 0.0:
        - цена остаётся неизменной (исходное значение сохраняется);
        - исключение не выбрасывается (сеттер только игнорирует значение).
        """
        temp_grass = LawnGrass(
            name="Тест",
            description="Для проверки цены",
            price=100.0,
            quantity=1,
            country="РФ",
            germination_period="10 дней",
            color="Зелёный"
        )

        # Пытаемся установить нулевую цену
        temp_grass.price = 0.0

        # Проверяем, что цена НЕ изменилась
        self.assertEqual(temp_grass.price, 100.0)
