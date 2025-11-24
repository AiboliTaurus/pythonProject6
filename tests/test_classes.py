import unittest.mock

import pytest

from src.category import Category
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


def test_category_add_product_validation():
    """Проверяет валидацию при добавлении товара."""
    category = Category("Категория", "Описание", [])

    # Корректный продукт
    product = Product("Корректный", "Описание", 100, 1)

    # Убедимся, что product — это действительно объект Product
    assert isinstance(product, Product)

    category.add_product(product)

    # Проверяем, что продукт добавился
    assert len(category.products_list) == 1
    assert category.products_list[0] == product  # Дополнительно: проверка содержимого

    # Некорректный тип
    with pytest.raises(TypeError, match="Можно добавлять только Product"):
        category.add_product("Не продукт")


# --- Тесты для счётчиков ---

def test_category_count_increment():
    """Проверяет, что category_count увеличивается при создании новой категории."""
    Category.category_count = 0
    Category.product_count = 0

    Category("Cat1", "Desc1", [])
    Category("Cat2", "Desc2", [])
    assert Category.category_count == 2


def test_product_count_increment():
    """Проверяет, что product_count увеличивается на количество товаров в категории."""
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("P1", "", 0, 0)
    p2 = Product("P2", "", 0, 0)
    p3 = Product("P3", "", 0, 0)

    Category("Cat1", "", [p1, p2])  # +2
    Category("Cat2", "", [p3])        # +1
    Category("Cat3", "", [])         # +0

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
