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
