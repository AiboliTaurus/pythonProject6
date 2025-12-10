class ZeroQuantityError(Exception):
    """Пользовательское исключение для товара с нулевым количеством"""
    def __init__(self, product_name):
        self.product_name = product_name
        self.message = f"Невозможно добавить товар '{product_name}' с нулевым количеством"
        super().__init__(self.message)

    def __str__(self):
        return self.message
