import pytest

from src.category import Category
from src.product import Product

# === ФИКСТУРЫ ===


@pytest.fixture
def sample_product():
    """Стандартный продукт для базовых тестов."""
    return Product("Смартфон", "Современный смартфон", 79990.0, 10)


@pytest.fixture
def another_product():
    """Второй продукт для проверки списков и сложения."""
    return Product("Ноутбук", "Игровой ноутбук", 89990.0, 5)


@pytest.fixture
def third_product():
    """Третий продукт для расширенных тестов списков."""
    return Product("Планшет", "10-дюймовый планшет", 29990.0, 8)


@pytest.fixture
def empty_category():
    """Категория без товаров."""
    return Category("Пустая", "Нет товаров", [])


@pytest.fixture
def category_with_products(sample_product, another_product):
    """Категория с двумя товарами."""
    return Category(
        name="Электроника",
        description="Электронные устройства",
        products=[sample_product, another_product]
    )


@pytest.fixture
def large_category(sample_product, another_product, third_product):
    """Категория с тремя товарами для тестов на итерацию и подсчёт."""
    return Category(
        name="Большая категория",
        description="Много товаров",
        products=[sample_product, another_product, third_product]
    )


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасывает счётчики категорий и товаров перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def existing_products():
    """Список существующих продуктов для проверки дубликатов и обновления."""
    return [
        Product("Товар 1", "Описание 1", 1000, 5),
        Product("Товар 2", "Описание 2", 2000, 10)
    ]


@pytest.fixture
def product_data():
    """Данные для создания нового продукта через new_product."""
    return {
        "name": "Новый товар",
        "description": "Новое описание",
        "price": 1500,
        "quantity": 8
    }


@pytest.fixture
def duplicate_product_data():
    """Данные для проверки обновления существующего продукта (дубликат по имени)."""
    return {
        "name": "Товар 1",  # совпадает с existing_products[0]
        "description": "Обновлённое описание",
        "price": 1200,
        "quantity": 3
    }


@pytest.fixture
def low_price_product():
    """Продукт с низкой ценой для тестирования валидации setter price."""
    return Product("Тест", "Описание", 500, 5)


@pytest.fixture
def zero_price_product():
    """Продукт с нулевой ценой — граничный случай для валидации."""
    return Product("Тест", "Описание", 0, 5)


@pytest.fixture
def negative_price_product():
    """Продукт с отрицательной ценой — недопустимый случай."""
    return Product("Тест", "Описание", -100, 5)


@pytest.fixture
def out_of_stock_product():
    """Продукт с нулевым остатком — проверка граничного состояния."""
    return Product("Закончился", "Нет в наличии", 1000, 0)


@pytest.fixture
def high_quantity_product():
    """Продукт с большим количеством — проверка суммирования стоимости."""
    return Product("Оптовый товар", "Большая партия", 500, 1000)


@pytest.fixture
def invalid_product_name():
    """Данные с пустым именем — проверка валидации."""
    return {
        "name": "",
        "description": "Описание",
        "price": 1000,
        "quantity": 5
    }


@pytest.fixture
def incomplete_product_data():
    """Неполные данные — проверка на отсутствие обязательных полей."""
    return {
        "name": "Неполный",
        "price": 1000,
        "quantity": 5
        # отсутствует description
    }


@pytest.fixture
def category_iterator(large_category):
    """Итератор по категории для тестирования протокола итерации."""
    return iter(large_category)


@pytest.fixture
def single_product_category(sample_product):
    """Категория с одним продуктом — для тестов крайних случаев."""
    return Category(
        name="Одиночный товар",
        description="Только один продукт",
        products=[sample_product]
    )


@pytest.fixture
def multi_price_products():
    """Продукты с разной ценой для теста сложения (__add__)."""
    return [
        Product("Дешёвый", "Низкая цена", 100, 10),
        Product("Дорогой", "Высокая цена", 10000, 2)
    ]


# Фикстуры для тестов
@pytest.fixture
def product_a():
    return Product("Товар A", "Описание A", 1000, 5)


@pytest.fixture
def product_b():
    return Product("Товар B", "Описание B", 2000, 3)


@pytest.fixture
def category_with_two_products(product_a, product_b):
    return Category(
        name="Категория с двумя товарами",
        description="Тестовая категория",
        products=[product_a, product_b]
    )


@pytest.fixture
def sample_category(sample_product):
    return Category("Образец", "Описание", [sample_product])
