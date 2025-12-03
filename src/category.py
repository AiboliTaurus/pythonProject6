from src.product import Product
from src.сategory_iterator import CategoryIterator


class Category:
    # Атрибуты класса (счётчики)
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list = None):
        # Инициализируем основной список продуктов
        self._products = []

        self.name = name
        self.description = description

        # Добавляем начальные продукты через add_product для проверки типов
        if products is not None:
            for product in products:
                self.add_product(product)

        # Увеличиваем счётчик категорий
        Category.category_count += 1

    @property
    def products_list(self) -> list:
        """Возвращает список продуктов (для совместимости с тестами)."""
        return self._products

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
        """
        Добавляет продукт в категорию.
        Проверяет, что объект является экземпляром Product или его наследником.
        Обновляет счётчик product_count.
        """
        # Проверка типа: product должен быть экземпляром Product или его подкласса
        if not isinstance(product, Product):
            raise TypeError(
                f"Можно добавлять только объекты класса Product или его наследников. "
                f"Получен тип: {type(product).__name__}"
            )

        # Добавляем продукт в список
        self._products.append(product)

        # Увеличиваем общий счётчик продуктов
        Category.product_count += 1
