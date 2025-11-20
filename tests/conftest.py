import pytest

from src.category import Category
from src.product import Product

# === ФИКСТУРЫ ===


@pytest.fixture
def sample_product():
    """Возвращает стандартный объект Product для тестов."""
    return Product("Смартфон", "Современный смартфон", 79990.0, 10)


@pytest.fixture
def another_product():
    """Другой продукт для проверки списков."""
    return Product("Ноутбук", "Игровой ноутбук", 89990.0, 5)


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


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасывает счётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def existing_products():
    """Список существующих продуктов для проверки дубликатов."""
    return [
        Product("Товар 1", "Описание 1", 1000, 5),
        Product("Товар 2", "Описание 2", 2000, 10)
    ]


@pytest.fixture
def product_data():
    """Данные для создания нового продукта."""
    return {
        "name": "Новый товар",
        "description": "Новое описание",
        "price": 1500,
        "quantity": 8
    }


@pytest.fixture
def duplicate_product_data():
    """Данные для проверки дублирования продукта."""
    return {
        "name": "Товар 1",  # Совпадает с существующим
        "description": "Обновленное описание",
        "price": 1200,
        "quantity": 3
    }


@pytest.fixture
def low_price_product():
    """Продукт с низкой ценой для тестирования валидации."""
    return Product("Тест", "Описание", 500, 5)


@pytest.fixture
def zero_price_product():
    """Продукт с нулевой ценой для тестирования валидации."""
    return Product("Тест", "Описание", 0, 5)
