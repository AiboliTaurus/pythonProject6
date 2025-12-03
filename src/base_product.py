from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def get_info(self) -> str:
        """Возвращает полную информацию о продукте."""
        pass

    @abstractmethod
    def set_price(self, new_price: float) -> None:
        """Устанавливает новую цену продукта с валидацией."""
        pass

    @abstractmethod
    def get_quantity(self) -> int:
        """Возвращает текущее количество товара."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление продукта."""
        pass
