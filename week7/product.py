class Product:
    """Represents a product in the shop.py with a name and stock quantity.
    
    Tests:
    >>> p = Product("Widget", 10)
    >>> p.name
    'Widget'
    >>> p.stock
    10
    >>> p.stock_is_low()
    False
    >>> p.stock = 2
    >>> p.stock_is_low()
    True
    >>> p.stock = -5
    Traceback (most recent call last):
    ...
    ValueError: Stock must be a non-negative integer
    """
    _LOW_STOCK_MARK = 3

    def __init__(self, name: str, stock: int):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string")
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("Stock must be a non-negative integer")
        self._name = name.strip()
        self._stock = stock

    @property
    def name(self) -> str:
        return self._name

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Stock must be a non-negative integer")
        self._stock = value

    def stock_is_low(self) -> bool:
        return self.stock <= Product._LOW_STOCK_MARK

    def __repr__(self):
        return f"Product(name={self.name!r}, stock={self.stock})"