import json
from typing import Any

# Импортируем все необходимые классы
from src.category import Category
from src.product import Product
from src.order import Order  # Добавляем импорт класса Order


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
    # Создаём продукты
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Выводим атрибуты продуктов
    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    # Создаём категорию «Смартфоны»
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    # Создаём продукт и категорию «Телевизоры»
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4]
    )

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)

    # Дополнительно: создаём заказ (пример использования нового класса Order)
    try:
        order1 = Order(product1, 2)  # Покупаем 2 шт. Samsung Galaxy S23 Ultra
        print(order1)  # Выведет информацию о заказе
        print(f"Итоговая стоимость заказа: {order1.total_cost():.2f} руб.")
    except ValueError as e:
        print(f"Ошибка при создании заказа: {e}")
