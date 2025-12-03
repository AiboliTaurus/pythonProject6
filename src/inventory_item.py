from abc import ABC, abstractmethod


class InventoryItem(ABC):
    """
    Абстрактный базовый класс для объектов, хранящих коллекцию товаров
    (например, Заказ или Категория).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает название объекта."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Возвращает описание объекта."""
        pass

    @abstractmethod
    def get_items(self) -> list:
        """Возвращает список товаров, связанных с объектом."""
        pass

    @abstractmethod
    def total_cost(self) -> float:
        """Рассчитывает итоговую стоимость всех товаров."""
        pass

    @abstractmethod
    def item_count(self) -> int:
        """Возвращает количество товаров (или единиц товара)."""
        pass
