from src.exceptions import ZeroQuantityError
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
        try:
            # Проверяем тип продукта
            if not isinstance(product, Product):
                raise TypeError(
                    f"Можно добавлять только объекты класса Product или его наследников. "
                    f"Получен тип: {type(product).__name__}"
                )

            # Проверяем количество товара
            if product.quantity == 0:
                raise ZeroQuantityError(product.name)

            self._products.append(product)
            Category.product_count += 1
            print(f"Товар '{product.name}' успешно добавлен")

        except ValueError as ve:
            raise ZeroQuantityError(str(ve)) from ve
        except ZeroQuantityError as zqe:
            print(zqe)
            raise

    def middle_price(self) -> float:
        """
        Подсчитывает среднюю цену всех товаров в категории.
        Обрабатывает случай отсутствия товаров.
        """
        if not self._products:
            return 0.0

        total_price = sum(product.price for product in self._products)
        return total_price / len(self._products)
