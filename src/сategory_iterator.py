class CategoryIterator:
    def __init__(self, category):
        self._category = category
        self._index = 0  # Текущая позиция в списке товаров

    def __iter__(self):
        """Возвращает сам итератор (себя)"""
        return self

    def __next__(self):
        """Возвращает следующий товар из категории"""
        # Проверяем, не вышли ли за пределы списка товаров
        if self._index >= len(self._category._products):
            raise StopIteration  # Завершаем итерацию

        # Получаем текущий товар и увеличиваем индекс
        product = self._category._products[self._index]
        self._index += 1
        return product
