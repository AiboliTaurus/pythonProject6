import sys
import unittest.mock
from io import StringIO

import pytest

from src.category import Category
from src.exceptions import ZeroQuantityError
from src.order import Order
from src.product import Product
from src.сategory_iterator import CategoryIterator

# --- Тесты для класса Product ---


def test_product_initialization():
    """Проверяет, что объект Product корректно инициализируется."""
    product = Product(
        name="Смартфон",
        description="Современный смартфон",
        price=29999.99,
        quantity=10
    )
    assert product.name == "Смартфон"
    assert product.description == "Современный смартфон"
    assert product.price == 29999.99
    assert product.quantity == 10


def test_product_price_float():
    """Проверяет, что цена может быть дробной (float)."""
    product = Product("Товар", "Описание", 999.50, 5)
    assert isinstance(product.price, float)


def test_product_quantity_int():
    """Проверяет, что количество — целое число (int)."""
    product = Product("Товар", "Описание", 1000, 3)
    assert isinstance(product.quantity, int)


def test_product_price_validation():
    """Проверяет валидацию цены при установке."""
    product = Product("Тест", "Описание", 100, 1)

    # Отрицательная цена — не принимается
    product.price = -100
    assert product.price == 100

    # Нулевая цена — не принимается
    product.price = 0
    assert product.price == 100

    # Положительная цена — принимается
    product.price = 200
    assert product.price == 200


def test_product_price_decrease_with_confirmation():
    """Проверяет запрос подтверждения при снижении цены."""
    product = Product("Тест", "Описание", 1000, 1)

    # Пользователь согласился
    with unittest.mock.patch('builtins.input', return_value='y'):
        product.price = 900
        assert product.price == 900

    # Пользователь отказался
    with unittest.mock.patch('builtins.input', return_value='n'):
        product.price = 800
        assert product.price == 900  # Осталась прежняя

    # Некорректный ввод, затем согласие
    with unittest.mock.patch('builtins.input', side_effect=['x', 'y']):
        product.price = 700
        assert product.price == 700


def test_product_new_product_method():
    """Проверяет работу класс-метода new_product."""
    existing_products = [
        Product("новый товар", "Старое описание", 100, 3)
    ]

    new_data = {
        "name": "новый товар",
        "description": "Другое описание",
        "price": 150,
        "quantity": 5
    }

    # Должен обновиться: цена (макс), количество (сумма), описание (новое)
    updated = Product.new_product(new_data, existing_products)

    assert updated.price == 150          # Максимальная цена
    assert updated.quantity == 8        # 3 + 5
    assert updated.description == "Старое описание"
    assert len(existing_products) == 1  # Новый не добавлен, обновлён существующий


# --- Тесты для класса Category ---

def test_category_initialization():
    """Проверяет, что объект Category корректно инициализируется."""
    product1 = Product("P1", "Desc1", 100, 5)
    product2 = Product("P2", "Desc2", 200, 3)
    category = Category(
        name="Электроника",
        description="Электронные товары",
        products=[product1, product2]
    )

    assert category.name == "Электроника"
    assert category.description == "Электронные товары"
    assert len(category.products_list) == 2  # Внутренний список


def test_category_empty_products():
    """Проверяет инициализацию категории с пустым списком товаров."""
    category = Category("Пустая", "Нет товаров", [])
    assert len(category.products_list) == 0
    assert category.name == "Пустая"


def test_category_product_formatting():
    """Проверяет форматирование вывода товаров."""
    product = Product("Товар", "Описание", 199.99, 5)
    category = Category("Категория", "Описание", [product])

    output = category.products  # Строковое представление
    expected = "Товар, 199 руб. Остаток: 5 шт.\n"
    assert output == expected


def test_category_empty_products_message():
    """Проверяет сообщение при пустом списке товаров."""
    category = Category("Пустая", "Нет товаров", [])
    assert category.products == "Список товаров пуст\n"


def test_category_add_valid_product():
    """
    Проверяет корректное добавление товара в категорию
    """
    category = Category("Категория", "Описание", [])
    product = Product("Корректный", "Описание", 100, 1)

    category.add_product(product)
    assert len(category.products_list) == 1
    assert category.products_list[0] == product


def test_category_count_and_product_count():
    """Тест подсчёта категорий и товаров."""
    products1 = [Product("P1", "Desc", 100, 1), Product("P2", "Desc", 200, 2)]
    products2 = [Product("P3", "Desc", 300, 3)]
    Category("Cat1", "Desc", products1)
    Category("Cat2", "Desc", products2)
    assert Category.category_count == 2
    assert Category.product_count == 3


# --- Тесты для счётчиков ---

def test_category_count_increment():
    """Проверяет, что category_count увеличивается при создании новой категории."""
    Category.category_count = 0
    Category.product_count = 0

    Category("Cat1", "Desc1", [])
    Category("Cat2", "Desc2", [])
    assert Category.category_count == 2


def test_product_count_increment():
    """
    Проверяет, что product_count увеличивается на количество товаров в категории.
    """
    Category.category_count = 0
    Category.product_count = 0

    # Используем валидные значения количества (не нулевые)
    p1 = Product("P1", "", 0, 1)  # Изменили количество с 0 на 1
    p2 = Product("P2", "", 0, 1)  # Изменили количество с 0 на 1
    p3 = Product("P3", "", 0, 1)  # Изменили количество с 0 на 1

    Category("Cat1", "", [p1, p2])  # +2
    Category("Cat2", "", [p3])      # +1
    Category("Cat3", "", [])       # +0

    assert Category.product_count == 3


def test_product_count_with_empty_category():
    """Проверяет, что пустая категория не увеличивает product_count."""
    Category.category_count = 0
    Category.product_count = 0

    Category("Пустая", "Нет товаров", [])
    assert Category.product_count == 0
    assert Category.category_count == 1


# --- Комплексный тест ---

def test_full_scenario():
    """Комплексная проверка: создаём несколько категорий и проверяем счётчики."""
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("iPhone", "Смартфон", 79990.0, 10)
    p2 = Product("Galaxy", "Смартфон", 69990.0, 15)
    p3 = Product("Ноутбук", "ПК", 89990.0, 5)

    cat1 = Category("Смартфоны", "Мобильные устройства", [p1, p2])
    cat2 = Category("Ноутбуки", "Компьютеры", [p3])
    cat3 = Category("Пустая категория", "Нет товаров", [])

    assert Category.category_count == 3
    assert Category.product_count == 3

    assert cat1.name == "Смартфоны"
    assert len(cat1.products_list) == 2
    assert cat2.name == "Ноутбуки"
    assert len(cat2.products_list) == 1
    assert cat3.name == "Пустая категория"


# === ТЕСТЫ ДЛЯ CategoryIterator ===

def test_iterator_initialization(category_with_two_products):
    """Проверяет, что итератор корректно создаётся."""
    iterator = CategoryIterator(category_with_two_products)
    assert iterator._category is category_with_two_products
    assert iterator._index == 0


def test_iterator_is_iterable(category_with_two_products):
    """Проверяет, что итератор реализует __iter__ и возвращает себя."""
    iterator = CategoryIterator(category_with_two_products)
    result = iter(iterator)
    assert result is iterator  # должен возвращать сам себя


def test_next_returns_first_product(category_with_two_products, product_a):
    """Проверяет, что __next__ возвращает первый товар."""
    iterator = CategoryIterator(category_with_two_products)
    first = next(iterator)
    assert first is product_a


def test_next_returns_second_product(category_with_two_products, product_b):
    """Проверяет, что при повторном вызове __next__ возвращается второй товар."""
    iterator = CategoryIterator(category_with_two_products)
    next(iterator)  # пропускаем первый
    second = next(iterator)
    assert second is product_b


def test_next_raises_stopiteration_after_last_product(category_with_two_products):
    """Проверяет, что после последнего товара вызывается StopIteration."""
    iterator = CategoryIterator(category_with_two_products)

    # Проходим по всем товарам
    next(iterator)  # первый
    next(iterator)  # второй

    # Следующий вызов должен вызвать StopIteration
    with pytest.raises(StopIteration):
        next(iterator)


def test_iteration_via_for_loop(category_with_two_products, product_a, product_b):
    """Проверяет работу итератора в цикле for."""
    iterator = CategoryIterator(category_with_two_products)
    products = list(iterator)

    assert len(products) == 2
    assert products[0] is product_a
    assert products[1] is product_b


def test_empty_category_iterator(empty_category):
    """Проверяет итератор для категории без товаров — сразу StopIteration."""
    iterator = CategoryIterator(empty_category)

    with pytest.raises(StopIteration):
        next(iterator)


def test_iterator_does_not_modify_original_list(category_with_two_products, product_a, product_b):
    """Проверяет, что итерация не изменяет исходный список товаров."""
    original_products = category_with_two_products._products.copy()
    iterator = CategoryIterator(category_with_two_products)

    list(iterator)  # проходим по всем

    # Проверяем, что список не изменился
    assert category_with_two_products._products == original_products


def test_multiple_iterations_independent(category_with_two_products, product_a, product_b):
    """Проверяет, что несколько итераторов работают независимо."""
    iterator1 = CategoryIterator(category_with_two_products)
    iterator2 = CategoryIterator(category_with_two_products)

    assert next(iterator1) is product_a
    assert next(iterator2) is product_a  # оба начинают с первого
    assert next(iterator1) is product_b  # первый продолжает
    assert next(iterator2) is product_b  # второй тоже продолжает


def test_iterator_reuse_after_stopiteration(category_with_two_products, product_a):
    """Проверяет, что после StopIteration итератор нельзя использовать повторно."""
    iterator = CategoryIterator(category_with_two_products)

    next(iterator)  # первый товар
    next(iterator)  # второй товар

    with pytest.raises(StopIteration):
        next(iterator)  # третий вызов — ошибка

    # Даже если попытаться ещё раз — всё равно ошибка
    with pytest.raises(StopIteration):
        next(iterator)


# Тесты для проверки обработки нулевого количества при создании продукта
def test_zero_quantity_product():
    """
    Проверяет, что при попытке создания продукта с нулевым количеством
    возникает исключение ValueError с соответствующим сообщением
    """
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Неверный товар", "Описание", 100, 0)


# Тесты для проверки метода middle_price
def test_middle_price_non_empty():
    """
    Проверяет корректность расчета средней цены для непустой категории
    """
    product1 = Product("Товар 1", "Описание", 100, 5)
    product2 = Product("Товар 2", "Описание", 200, 3)
    category = Category("Тестовая", "Описание", [product1, product2])

    expected_price = (100 + 200) / 2
    assert category.middle_price() == expected_price


def test_middle_price_empty():
    """
    Проверяет, что для пустой категории возвращается 0.0
    """
    category = Category("Пустая категория", "Описание")
    assert category.middle_price() == 0.0


# Тесты для проверки обработки исключений при добавлении товара в категорию
def test_add_product_zero_quantity():
    """
    Проверяет, что при попытке создать продукт с нулевым количеством
    возникает исключение ValueError
    """
    category = Category("Тестовая", "Описание")

    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        category.add_product(Product("Неверный товар", "Описание", 100, 0))


def test_add_valid_product():
    """
    Проверяет корректное добавление товара в категорию
    """
    category = Category("Тестовая", "Описание")
    product = Product("Корректный товар", "Описание", 100, 5)
    category.add_product(product)
    assert len(category.products_list) == 1
    assert category.products_list[0] == product


# Тест для проверки обработки заказа с нулевым количеством
def test_order_zero_quantity_with_capsys(capsys):
    """
    Проверяет обработку нулевого количества с использованием capsys
    """
    product = Product("Товар", "Описание", 100, 5)

    try:
        Order(product, 0)
    except ZeroQuantityError:
        # Получаем вывод в консоль
        captured = capsys.readouterr()
        assert "Невозможно добавить товар" in captured.out


# Тест для проверки корректного создания заказа
def test_valid_order():
    """
    Проверяет корректное создание заказа с валидными данными
    """
    product = Product("Товар", "Описание", 100, 5)
    order = Order(product, 2)
    assert order.item_count() == 2
    assert order.total_cost() == 200


# Тест для проверки обработки заказа с превышением количества на складе
def test_order_exceed_stock():
    """
    Проверяет, что при попытке создать заказ с количеством,
    превышающим остаток на складе, возникает исключение ValueError
    и выводится соответствующее сообщение
    """
    product = Product("Товар", "Описание", 100, 3)

    # Сохраняем оригинальный stdout
    captured_output = StringIO()
    sys.stdout = captured_output

    try:
        Order(product, 5)
    except ValueError:
        # Проверяем, что сообщение об ошибке было выведено
        output = captured_output.getvalue()
        assert "На складе недостаточно товара" in output
    finally:
        # Восстанавливаем оригинальный stdout
        sys.stdout = sys.__stdout__


def test_middle_price_empty_category():
    category = Category("Пустая категория", "Описание")
    assert category.middle_price() == 0.0


def test_middle_price_single_product():
    category = Category("Одна позиция", "Описание")
    category.add_product(Product("Товар1", "Описание", 100, 1))
    assert category.middle_price() == 100.0


def test_middle_price_multiple_products():
    category = Category("Несколько товаров", "Описание")
    category.add_product(Product("Товар1", "Описание", 100, 1))
    category.add_product(Product("Товар2", "Описание", 200, 1))
    category.add_product(Product("Товар3", "Описание", 300, 1))
    assert category.middle_price() == 200.0


def test_middle_price_float_result():
    category = Category("Дробный результат", "Описание")
    category.add_product(Product("Товар1", "Описание", 150, 1))
    category.add_product(Product("Товар2", "Описание", 250, 1))
    assert category.middle_price() == 200.0
