import json
from typing import Any
from src.category import Category
from src.product import Product


def load_data_from_json(filepath: str) -> Any:
    """
    Загружает данные из JSON-файла и создаёт объекты классов Product и Category.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {filepath}. Проверьте путь и наличие файла.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON: {e}")

    categories = []
    for category_data in data:
        products = []
        for product_data in category_data['products']:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )
            products.append(product)

        category = Category(
            name=category_data['name'],
            description=category_data['description'],
            products=products
        )
        categories.append(category)

    return categories


if __name__ == "__main__":
    # Демонстрация работы с ручным созданием объектов
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print("Исходный список товаров:")
    print(category1.products)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)

    print("\nОбновлённый список товаров:")
    print(category1.products)
    print(f"Количество товаров в категории: {category1.product_count}")

    # Демонстрация работы с new_product
    new_product_data = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5
    }
    new_product = Product.new_product(new_product_data)

    print("\nИнформация о новом продукте:")
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    # Тестирование валидации цены
    print("\nТестирование валидации цены:")
    new_product.price = 800
    print(f"Новая цена: {new_product.price}")

    new_product.price = -100
    print(f"Попытка установить отрицательную цену: {new_product.price}")

    new_product.price = 0
    print(f"Попытка установить нулевую цену: {new_product.price}")
