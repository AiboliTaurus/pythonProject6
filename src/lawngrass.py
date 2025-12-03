from src.product import Product


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def get_info(self) -> str:
        return (f"{self.name}, цвет: {self.color}, произв.: {self.country}, "
                f"прорастание: {self.germination_period}, цена: {self.price} руб., "
                f"остаток: {self.quantity} шт.")

    def __str__(self) -> str:
        return (f"{self.name}, {self.color}, произв.: {self.country}, "
                f"прорастание: {self.germination_period}, "
                f"{int(self.price)} руб. Остаток: {self.quantity} шт.")

    def __add__(self, other):
        if type(other) is not type(self):
            raise TypeError("Можно складывать только объекты одного класса")

        total_quantity = self.quantity + other.quantity
        total_value = self.price * self.quantity + other.price * other.quantity
        avg_price = total_value / total_quantity

        return LawnGrass(
            name=f"{self.name} & {other.name}",
            description=self.description,
            price=avg_price,
            quantity=total_quantity,
            country=f"{self.country}/{other.country}",
            germination_period="avg",
            color=f"{self.color}/{other.color}"
        )
