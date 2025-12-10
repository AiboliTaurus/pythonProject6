from src.exceptions import ZeroQuantityError
from src.order import Order
from src.product import Product


def test_order_creation():
    """
    Проверяет корректное создание заказа
    """
    product = Product("Товар", "Описание", 100, 5)
    order = Order(product, 2)

    assert order._product == product
    assert order._quantity == 2
    assert product.quantity == 3  # Проверяем уменьшение количества на складе


def test_order_zero_quantity(capsys):
    """
    Проверяет обработку нулевого количества
    """
    product = Product("Товар", "Описание", 100, 5)

    try:
        Order(product, 0)
    except ZeroQuantityError:
        captured = capsys.readouterr()
        assert f"Невозможно добавить товар '{product.name}' с нулевым количеством" in captured.out


def test_order_negative_quantity(capsys):
    """
    Проверяет обработку отрицательного количества
    """
    product = Product("Товар", "Описание", 100, 5)

    try:
        Order(product, -1)
    except ZeroQuantityError:
        captured = capsys.readouterr()
        assert f"Невозможно добавить товар '{product.name}' с нулевым количеством" in captured.out


def test_order_insufficient_stock(capsys):
    """
    Проверяет обработку недостаточного количества на складе
    """
    product = Product("Товар", "Описание", 100, 3)

    try:
        Order(product, 5)
    except ValueError:
        captured = capsys.readouterr()
        expected_message = "Ошибка: На складе недостаточно товара: доступно 3, запрошено 5"
        assert expected_message in captured.out


def test_order_total_cost():
    """
    Проверяет расчет общей стоимости заказа
    """
    product = Product("Товар", "Описание", 100, 5)
    order = Order(product, 2)

    assert order.total_cost() == 200.0


def test_order_item_count():
    """
    Проверяет количество единиц товара в заказе
    """
    product = Product("Товар", "Описание", 100, 5)
    order = Order(product, 2)

    assert order.item_count() == 2


def test_order_get_items():
    """
    Проверяет получение списка товаров в заказе
    """
    product = Product("Товар", "Описание", 100, 5)
    order = Order(product, 2)

    assert order.get_items() == [product]


def test_order_str_representation():
    """
    Проверяет строковое представление заказа
    """
    product = Product("Товар", "Описание", 100, 5)
    order = Order(product, 2)

    expected_str = (f"Заказ #{hash(order) % 10000}: "
                    f"Покупка товара 'Товар' в количестве 2 шт., "
                    f"итоговая стоимость: 200.00 руб.")

    assert str(order) == expected_str


def test_order_repr_representation():
    """
    Проверяет представление заказа для отладки
    """
    product = Product("Товар", "Описание", 100, 5)
    order = Order(product, 2)

    expected_repr = f"Order(product={repr(product)},quantity=2)"
    assert repr(order) == expected_repr


# Тест с захватом вывода консоли
def test_order_creation_output(capsys):
    """
    Проверяет вывод сообщений при создании заказа
    """
    product = Product("Товар", "Описание", 100, 5)
    Order(product, 2)

    captured = capsys.readouterr()
    assert "Товар 'Товар' успешно добавлен в заказ" in captured.out
    assert "Обработка добавления товара в заказ завершена" in captured.out
