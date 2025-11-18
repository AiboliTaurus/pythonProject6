import json
from typing import Any

from src.category import Category
from src.product import Product


def load_data_from_json(filepath: str) -> Any:
    """
    Загружает данные из JSON-файла и создаёт объекты классов Product и Category.

    Args:
        filepath (str): путь к JSON-файлу.

    Returns:
        List[Category]: список объектов класса Category с заполненными товарами.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)  # читаем и парсим JSON
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {filepath}. Проверьте путь и наличие файла.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON: {e}")

    categories = []

    for category_data in data:
        products = []
        for product_data in category_data['products']:
            # Создаём объект Product из данных JSON
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )
            products.append(product)

        # Создаём объект Category с собранными продуктами
        category = Category(
            name=category_data['name'],
            description=category_data['description'],
            products=products
        )
        categories.append(category)

    return categories


if __name__ == '__main__':  # Исправлено: добавлена закрывающая кавычка
    try:
        categories = load_data_from_json('data/products.json')

        # Выведем информацию для проверки
        for category in categories:
            print(f"Категория: {category.name}")
            print(f"Описание: {category.description}")
            print("Товары:")
            for product in category.products:
                print(f"!  - {product.name}: {product.price} руб., {product.quantity} шт.")
            print()

    except Exception as e:
        print(f"Ошибка: {e}")
