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
    assert category.name == "Электроника"
    assert category.description == "Электронные товары"
    assert len(category.products) == 2
    assert category.products[0].name == "P1"
    assert category.products[1].name == "P2"


def test_category_empty_products():
    """Проверяет инициализацию категории с пустым списком товаров."""
    category = Category("Пустая", "Нет товаров", [])
    assert len(category.products) == 0
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
    assert len(cat1.products) == 2
    assert cat2.name == "Ноутбуки"
    assert len(cat2.products) == 1
    assert cat3.name == "Пустая категория"
    assert len(cat3.products) == 0
