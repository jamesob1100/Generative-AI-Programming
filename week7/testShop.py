import io
import sys
import unittest

from shop import Shop


class TestShop(unittest.TestCase):
    def setUp(self):
        self.shop = Shop("Test Shop")

    def test_add_product_success_and_duplicate(self):
        self.assertTrue(self.shop.add_product("Widget", 10))
        self.assertTrue(self.shop.add_product("Gadget", 2))
        self.assertFalse(self.shop.add_product("Widget", 5))
        widget = next(p for p in self.shop.products if p.name == "Widget")
        gadget = next(p for p in self.shop.products if p.name == "Gadget")
        self.assertEqual(widget.stock, 10)
        self.assertEqual(gadget.stock, 2)

    def test_add_product_invalid_name_or_stock(self):
        with self.assertRaises(ValueError):
            self.shop.add_product("", 1)
        with self.assertRaises(ValueError):
            self.shop.add_product("Thing", -1)
        with self.assertRaises(ValueError):
            self.shop.add_product("Thing", "5")

    def test_remove_product(self):
        self.shop.add_product("Widget", 10)
        self.assertTrue(self.shop.remove_product("Widget"))
        self.assertFalse(self.shop.remove_product("Widget"))

    def test_restock_success_and_errors(self):
        self.shop.add_product("Gadget", 2)
        self.assertTrue(self.shop.restock("Gadget", 5))
        self.assertEqual(self.shop._find_product("Gadget").stock, 7)

        with self.assertRaises(KeyError):
            self.shop.restock("Thing", 1)

        with self.assertRaises(ValueError):
            self.shop.restock("Gadget", 0)

        with self.assertRaises(ValueError):
            self.shop.restock("Gadget", -1)

        with self.assertRaises(ValueError):
            self.shop.restock("Gadget", "3")

    def test_sell_success_and_errors(self):
        self.shop.add_product("Widget", 10)
        self.assertTrue(self.shop.sell("Widget", 3))
        self.assertEqual(self.shop._find_product("Widget").stock, 7)

        with self.assertRaises(ValueError):
            self.shop.sell("Widget", 20)

        with self.assertRaises(KeyError):
            self.shop.sell("Thing", 1)

        with self.assertRaises(ValueError):
            self.shop.sell("Widget", 0)

        with self.assertRaises(ValueError):
            self.shop.sell("Widget", -2)

        with self.assertRaises(ValueError):
            self.shop.sell("Widget", "3")

    def test_print_product_list_outputs(self):
        self.shop.add_product("Widget", 10)
        self.shop.add_product("Gadget", 2)

        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            self.shop.print_product_list()
        finally:
            sys.stdout = sys_stdout

        out = captured.getvalue()
        self.assertIn("Product list for shop 'Test Shop':", out)
        self.assertIn("Widget", out)
        self.assertIn("Gadget", out)

    def test_print_product_list_low_stock_only(self):
        self.shop.add_product("Widget", 10)
        self.shop.add_product("Gadget", 2)

        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            self.shop.print_product_list(low_stock_only=True)
        finally:
            sys.stdout = sys_stdout

        out = captured.getvalue()
        self.assertNotIn("Widget", out)
        self.assertIn("Gadget", out)

    def test_print_product_list_no_products(self):
        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            self.shop.print_product_list()
        finally:
            sys.stdout = sys_stdout

        self.assertIn("No products to show", captured.getvalue())


if __name__ == "__main__":
    unittest.main()
