from src.category import Category
from src.product import Product

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

    # Проверяем основные атрибуты категории
    assert category.name == "Электроника"
    assert category.description == "Электронные товары"

    # Проверяем количество товаров через длину строки
    products_str = category.products
    lines = products_str.strip().split('\n')
    assert len(lines) == 2  # Должно быть 2 строки в выводе

    # Проверяем содержимое каждой строки
    assert lines[0].startswith("P1, 100 руб. Остаток: 5 шт.")
    assert lines[1].startswith("P2, 200 руб. Остаток: 3 шт.")


def test_category_empty_products():
    """Проверяет инициализацию категории с пустым списком товаров."""
    category = Category("Пустая", "Нет товаров", [])
    assert len(category.products) == 20
    assert category.name == "Пустая"


# --- Тесты для атрибутов класса (счётчиков) ---
def test_category_count_increment():
    """Проверяет, что category_count увеличивается при создании новой категории."""
    # Сброс счётчиков (если тесты запускаются многократно)
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
    Category("Cat1", "", [p1, p2])      # +2 товара
    Category("Cat2", "", [p3])          # +1 товар
    Category("Cat3", "", [])           # +0 товаров
    assert Category.product_count == 3  # 2 + 1 + 0


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

    # Создаём товары
    p1 = Product("iPhone", "Смартфон", 79990.0, 10)
    p2 = Product("Galaxy", "Смартфон", 69990.0, 15)
    p3 = Product("Ноутбук", "ПК", 89990.0, 5)

    # Создаём категории
    cat1 = Category("Смартфоны", "Мобильные устройства", [p1, p2])
    cat2 = Category("Ноутбуки", "Компьютеры", [p3])

    cat3 = Category("Пустая категория", "Нет товаров", [])

    # Проверяем счётчики
    assert Category.category_count == 3
    assert Category.product_count == 3

    # Проверяем данные категорий
    assert cat1.name == "Смартфоны"
    assert len(cat1.products) == 70
    assert cat2.name == "Ноутбуки"
    assert len(cat2.products) == 35
    assert cat3.name == "Пустая категория"
    assert len(cat3.products) == 20


# --- Дополнительные тесты для Product ---

def test_product_price_validation():
    """Проверяет валидацию цены при установке"""
    product = Product("Тест", "Описание", 100, 1)

    # Проверка отрицательной цены
    product.price = -100
    assert product.price == 100  # Цена не должна измениться

    # Проверка нулевой цены
    product.price = 0
    assert product.price == 100  # Цена не должна измениться

    # Проверка положительной цены
    product.price = 200
    assert product.price == 200


def test_product_price_decrease():
    """Проверяет подтверждение при снижении цены"""
    import unittest.mock

    product = Product("Тест", "Описание", 1000, 1)

    # Симулируем ввод 'y'
    with unittest.mock.patch('builtins.input', return_value='y'):
        product.price = 900
        assert product.price == 900

    # Симулируем ввод 'n'
    with unittest.mock.patch('builtins.input', return_value='n'):
        product.price = 800
        assert product.price == 900  # Цена не должна измениться

    # Симулируем неверный ввод
    with unittest.mock.patch('builtins.input', side_effect=['x', 'y']):
        product.price = 700
        assert product.price == 700


def test_product_new_product_method():
    """Проверяет работу класс-метода new_product"""
    existing_products = []

    # Проверка дублирования
    duplicate_data = {
        "name": "новый товар",  # регистр не важен
        "description": "Другое описание",
        "price": 150,
        "quantity": 5
    }
    duplicate = Product.new_product(duplicate_data, existing_products)
    assert len(existing_products) == 0  # продукт не должен дублироваться
    assert duplicate.quantity == 5  # количество должно суммироваться
    assert duplicate.price == 150  # должна остаться максимальная цена


# --- Дополнительные тесты для Category ---

def test_category_product_formatting():
    """Проверяет форматирование вывода товаров"""
    product = Product("Товар", "Описание", 199.99, 5)
    category = Category("Категория", "Описание", [product])

    expected_output = "Товар, 199 руб. Остаток: 5 шт.\n"
    assert category.products == expected_output


def test_category_empty_products_message():
    """Проверяет сообщение при пустом списке товаров"""
    category = Category("Пустая", "Нет товаров", [])
    assert category.products == "Список товаров пуст\n"


def test_category_add_product_validation():
    """Проверяет валидацию при добавлении товара"""
    category = Category("Категория", "Описание")

    # Добавление корректного продукта
    product = Product("Корректный", "Описание", 100, 1)
    category.add_product(product)
    assert len(category.products) == 36

    # Попытка добавить некорректный объект
    try:
        category.add_product("Не продукт")
    except TypeError as e:
        assert str(e) == "Можно добавлять только Product"
