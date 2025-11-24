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


if __name__ == '__main__':
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)
