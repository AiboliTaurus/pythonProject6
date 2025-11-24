from src.product import Product
from src.сategory_iterator import CategoryIterator


class Category:
    # Атрибуты класса (счётчики)
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.products_list = products if products is not None else []
        self.name = name
        self.description = description
        self._products = products  # Защищённый атрибут

        # Увеличиваем счётчик product_count на количество товаров в категории
        if products:
            Category.product_count += len(products)

        # Увеличиваем счётчик категорий
        Category.category_count += 1

    @property
    def products(self) -> str:
        if not self._products:
            return "Список товаров пуст\n"
        result = ""
        for product in self._products:
            result += str(product) + "\n"
        return result

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self._products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """Возвращает итератор для обхода товаров категории"""
        return CategoryIterator(self)

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только Product")
        self.products_list.append(product)  # Важно: добавляем в список!
