from src.inventory_item import InventoryItem
from src.product import Product


class MockInventoryItem(InventoryItem):
    """Мок-класс для тестирования абстрактного класса."""
    def __init__(self, name, description, items):
        self._name = name
        self._description = description
        self._items = items

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    def get_items(self):
        return self._items

    def total_cost(self):
        return sum(item.price * item.quantity for item in self._items)

    def item_count(self):
        return len(self._items)


def test_inventory_item_abstract_methods():
    """Проверка реализации абстрактных методов."""
    products = [Product("P1", "Desc", 100, 1), Product("P2", "Desc", 200, 2)]
    item = MockInventoryItem("Test", "Desc", products)
    assert item.name == "Test"
    assert item.description == "Desc"
    assert item.get_items() == products
    assert item.total_cost() == 500  # 100*1 + 200*2
    assert item.item_count() == 2
