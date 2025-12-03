from src.product import Product


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def get_info(self) -> str:
        return (f"{self.name} ({self.model}), {self.color}, "
                f"{self.memory} ГБ, эффективность: {self.efficiency}, "
                f"цена: {self.price} руб., остаток: {self.quantity} шт.")

    def __str__(self) -> str:
        return (f"{self.name} ({self.model}), {self.color}, "
                f"{self.memory} ГБ, {int(self.price)} руб. Остаток: {self.quantity} шт.")

    def __add__(self, other):
        if type(other) is not type(self):
            raise TypeError("Можно складывать только объекты одного класса")

        total_quantity = self.quantity + other.quantity
        total_value = self.price * self.quantity + other.price * other.quantity
        avg_price = total_value / total_quantity

        return Smartphone(
            name=f"{self.name} & {other.name}",
            description=self.description,
            price=avg_price,
            quantity=total_quantity,
            efficiency=(self.efficiency + other.efficiency) / 2,
            model="Combined",
            memory=max(self.memory, other.memory),
            color=f"{self.color}/{other.color}"
        )
