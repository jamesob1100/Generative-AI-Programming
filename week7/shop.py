from product import Product


class Shop:
    """A class representing a shop that manages a collection of products.
    
    Tests:
    >>> shop = Shop("Test Shop")
    >>> shop.add_product("Widget", 10)
    True
    >>> shop.add_product("Gadget", 2)
    True
    >>> shop.add_product("Widget", 5)
    False
    >>> shop.restock("Gadget", 5)
    True
    >>> shop.sell("Widget", 3)
    True
    >>> shop.sell("Widget", 20)
    Traceback (most recent call last):
    ...
    ValueError: Not enough stock to sell
    >>> shop.sell("Thing", 1)
    Traceback (most recent call last):
    ...
    KeyError: "Product 'Thing' not found"
    >>> shop.print_product_list()
    Product(name='Widget', stock=7)
    Product(name='Gadget', stock=7)
    """
    def __init__(self, shop_name: str):
        if not isinstance(shop_name, str) or not shop_name.strip():
            raise ValueError("Shop name must be a non-empty string")
        self.name = shop_name.strip()
        self.products = []  # list[Product]

    def _find_product(self, prod_name: str):
        prod_name = prod_name.strip() if isinstance(prod_name, str) else ""
        if not prod_name:
            return None
        for p in self.products:
            if p.name == prod_name:
                return p
        return None

    def add_product(self, prod_name: str, stock: int) -> bool:
        if not isinstance(prod_name, str) or not prod_name.strip():
            raise ValueError("Product name must be a non-empty string")
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("Stock must be a non-negative integer")
        if self._find_product(prod_name):
            return False
        self.products.append(Product(prod_name.strip(), stock))
        return True

    def remove_product(self, prod_name: str) -> bool:
        p = self._find_product(prod_name)
        if not p:
            return False
        self.products.remove(p)
        return True

    def restock(self, prod_name: str, quantity: int) -> bool:
        p = self._find_product(prod_name)
        if not p:
            raise KeyError(f"Product '{prod_name}' not found")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        p.stock += quantity
        return True

    def sell(self, prod_name: str, quantity: int) -> bool:
        p = self._find_product(prod_name)
        if not p:
            raise KeyError(f"Product '{prod_name}' not found")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        if quantity > p.stock:
            raise ValueError("Not enough stock to sell")
        p.stock -= quantity
        return True

    def print_product_list(self, low_stock_only=False):
        products_to_show = (
            [p for p in self.products if p.stock_is_low()]
            if low_stock_only
            else list(self.products)
        )
        if not products_to_show:
            print("No products to show")
            return
        print(f"Product list for shop '{self.name}':")
        print(f"{'Name':<20} {'Stock':<5} {'Status'}")
        print("-" * 35)
        for p in products_to_show:
            status = "LOW STOCK" if p.stock_is_low() else ""
            print(f"{p.name:<20} {p.stock:<5} {status}")
