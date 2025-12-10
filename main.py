import json
from typing import Any
from src.exceptions import ZeroQuantityError  # Импортируем кастомное исключение

# Импортируем все необходимые классы
from src.category import Category
from src.product import Product


def load_data_from_json(filepath: str) -> Any:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {filepath}. Проверьте путь и наличие файла.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON: {e}")

    # Проверяем, что данные являются списком
    if not isinstance(data, list):
        raise ValueError("Данные в JSON файле должны быть списком категорий")

    categories = []
    for category_data in data:
        # Проверяем наличие обязательных полей для категории
        if not all(key in category_data for key in ['name', 'description', 'products']):
            raise ValueError("В данных категории отсутствуют обязательные поля")

        products = []
        for product_data in category_data['products']:
            # Проверяем наличие обязательных полей для продукта
            if not all(key in product_data for key in ['name', 'description', 'price', 'quantity']):
                raise ValueError("В данных продукта отсутствуют обязательные поля")

            try:
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    quantity=product_data['quantity']
                )
                products.append(product)
            except ZeroQuantityError as zqe:
                print(f"Ошибка при создании продукта: {zqe}")

        category = Category(
            name=category_data['name'],
            description=category_data['description'],
            products=products
        )
        categories.append(category)

    return categories


if __name__ == '__main__':
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(f"Возникла ошибка ValueError, прерывающая работу программы"
              f" при попытке добавить продукт с нулевым количеством: {e}")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])
    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())
