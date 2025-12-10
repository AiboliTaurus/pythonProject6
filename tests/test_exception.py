from src.exceptions import ZeroQuantityError


def test_zero_quantity_error_creation():
    """
    Проверяет создание исключения с корректным именем товара
    """
    product_name = "Тестовый товар"
    error = ZeroQuantityError(product_name)

    assert error.product_name == product_name
    assert error.message == f"Невозможно добавить товар '{product_name}' с нулевым количеством"


def test_zero_quantity_error_str_representation():
    """
    Проверяет корректность строкового представления исключения
    """
    product_name = "Тестовый товар"
    error = ZeroQuantityError(product_name)

    assert str(error) == f"Невозможно добавить товар '{product_name}' с нулевым количеством"


def test_zero_quantity_error_inheritance():
    """
    Проверяет наследование от базового класса Exception
    """
    product_name = "Тестовый товар"
    error = ZeroQuantityError(product_name)

    assert isinstance(error, Exception)
    assert isinstance(error, ZeroQuantityError)


def test_zero_quantity_error_message():
    """
    Проверяет корректность формирования сообщения об ошибке
    """
    test_cases = [
        ("Товар 1", "Невозможно добавить товар 'Товар 1' с нулевым количеством"),
        ("Другой товар", "Невозможно добавить товар 'Другой товар' с нулевым количеством"),
        ("", "Невозможно добавить товар '' с нулевым количеством")
    ]

    for product_name, expected_message in test_cases:
        error = ZeroQuantityError(product_name)
        assert error.message == expected_message
        assert str(error) == expected_message


def test_zero_quantity_error_context():
    """
    Проверяет работу исключения в контексте обработки ошибок
    """
    product_name = "Тестовый товар"

    try:
        raise ZeroQuantityError(product_name)
    except ZeroQuantityError as e:
        assert e.product_name == product_name
        assert str(e) == f"Невозможно добавить товар '{product_name}' с нулевым количеством"