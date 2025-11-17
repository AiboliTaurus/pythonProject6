class Category:
    # Атрибуты класса (общие для всех объектов)
    category_count = 0  # счётчик количества категорий
    product_count = 0   # счётчик общего количества товаров во всех категориях

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.products = products

        # Автоматическое увеличение атрибутов класса, при инициализации объекта
        Category.category_count += 1  # увеличиваем счётчик категорий
        Category.product_count += len(products)  # добавляем количество товаров из списка
