from src.product import Product


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        if products:
            for product in self.__products:
                if not isinstance(product, Product):
                    raise TypeError("Все элементы должны быть Product")

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только Product")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        if not self.__products:
            return "Список товаров пуст\n"

        result = ""
        for product in self.__products:
            result += f"{product.name}, {int(product.price)} руб. Остаток: {product.quantity} шт.\n"
        return result
