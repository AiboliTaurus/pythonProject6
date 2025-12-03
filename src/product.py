from src.base_product import BaseProduct
from src.creation_logger import CreationLogger


class Product(CreationLogger, BaseProduct):
    """
    Базовый класс продукта с логированием создания.
    Наследует:
    - CreationLogger (для вывода информации о создании)
    - BaseProduct (абстрактный базовый класс)
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут
        self.quantity = quantity
        # super() вызовет __init__ миксина CreationLogger,
        # который выведет информацию и передаст управление дальше
        super().__init__(name, description, price, quantity)

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None):
        required_keys = {'name', 'description', 'price', 'quantity'}
        if not required_keys.issubset(product_data.keys()):
            raise ValueError("Не все обязательные поля указаны")

        if existing_products:
            for existing in existing_products:
                if existing.name.lower() == product_data['name'].lower():
                    existing.quantity += product_data['quantity']
                    existing.price = max(existing.price, product_data['price'])
                    return existing

        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    @property
    def price(self) -> float:
        """Геттер для получения цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            while True:
                confirm = input("Цена ниже текущей. Подтвердите изменение (y/n): ").strip().lower()
                if confirm == 'y':
                    break
                elif confirm == 'n':
                    print("Изменение цены отменено")
                    return
                else:
                    print("Неверный ввод. Пожалуйста, введите 'y' или 'n'")

        self.__price = new_price

    # Реализация абстрактных методов BaseProduct
    def get_info(self) -> str:
        return f"{self.name}, {self.description}, цена: {self.price} руб., остаток: {self.quantity} шт."

    def set_price(self, new_price: float) -> None:
        self.price = new_price  # Используем существующий setter

    def get_quantity(self) -> int:
        return self.quantity

    def __str__(self) -> str:
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other) -> float:
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")
        return self.price * self.quantity + other.price * other.quantity
