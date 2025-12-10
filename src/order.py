from src.exceptions import ZeroQuantityError
from src.inventory_item import InventoryItem
from src.product import Product


class Order(InventoryItem):
    """
    Класс, описывающий заказ одного товара.
    В заказе может быть только один товар и его количество.
    """

    def __init__(self, product: Product, quantity: int):
        try:
            # Проверка на нулевое количество
            if quantity <= 0:
                raise ZeroQuantityError(product.name)

            # Проверка наличия товара на складе
            if product.quantity < quantity:
                raise ValueError(f"На складе недостаточно товара: доступно {product.quantity}, запрошено {quantity}")

            # Если все проверки пройдены
            self._product = product
            self._quantity = quantity
            # Резервируем товар на складе
            self._product.quantity -= quantity
            print(f"Товар '{self._product.name}' успешно добавлен в заказ")

        except ZeroQuantityError as zqe:
            print(zqe)

        except ValueError as ve:
            print(f"Ошибка: {ve}")

        finally:
            print("Обработка добавления товара в заказ завершена")

    @property
    def name(self) -> str:
        return f"Заказ #{hash(self) % 10000}"

    @property
    def description(self) -> str:
        return f"Покупка товара '{self._product.name}' в количестве {self._quantity} шт."

    def get_items(self) -> list:
        return [self._product]

    def total_cost(self) -> float:
        return self._product.price * self._quantity

    def item_count(self) -> int:
        return self._quantity

    def __str__(self) -> str:
        return (f"{self.name}: {self.description}, "
                f"итоговая стоимость: {self.total_cost():.2f} руб.")

    def __repr__(self) -> str:
        return (f"Order(product={repr(self._product)},"
                f"quantity={self._quantity})")
