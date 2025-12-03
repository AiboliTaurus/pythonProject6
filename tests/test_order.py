import pytest

from src.order import Order
from src.product import Product


def test_order_creation():
    """Тест создания заказа."""
    product = Product("Test Product", "Description", 100.0, 5)
    order = Order(product, 2)
    assert order.name.startswith("Заказ #")
    assert order.description == "Покупка товара 'Test Product' в количестве 2 шт."
    assert order.item_count() == 2
    assert order.total_cost() == 200.0


def test_order_with_insufficient_quantity():
    """Тест на ошибку при заказе большего количества, чем есть на складе."""
    product = Product("Test Product", "Description", 100.0, 1)
    with pytest.raises(ValueError, match="На складе недостаточно товара"):
        Order(product, 2)


def test_order_with_zero_quantity():
    """Тест на ошибку при заказе нулевого количества товара."""
    product = Product("Test Product", "Description", 100.0, 5)
    with pytest.raises(ValueError, match="Количество товара в заказе должно быть положительным"):
        Order(product, 0)


def test_order_reserves_stock():
    """Тест резервирования товара на складе при создании заказа."""
    product = Product("Test Product", "Description", 100.0, 5)
    Order(product, 2)
    assert product.quantity == 3  # Количество на складе уменьшилось на 2
