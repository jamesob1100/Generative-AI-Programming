import io
import sys
import unittest
from unittest.mock import patch

from shop import Shop
from shopUI import ShopUI


class TestShopUI(unittest.TestCase):
    def setUp(self):
        self.shop = Shop("Test Shop")
        self.ui = ShopUI(self.shop)

    def test_init(self):
        self.assertIs(self.ui.shop, self.shop)

    def test_manage_shop_add_remove_restock_sell_and_quit(self):
        inputs = [
            "1", "Widget", "5",   # add product
            "3", "Widget", "2",   # restock product
            "4", "Widget", "1",   # sell product
            "5",                     # show all products
            "7"                      # quit
        ]
        expected_outputs = [
            "Product added.",
            "Product restocked.",
            "Product sold.",
            "Product list for shop 'Test Shop':"
        ]

        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            with patch('builtins.input', side_effect=inputs):
                self.ui.manage_shop()
        finally:
            sys.stdout = sys_stdout

        output = captured.getvalue()
        for expected in expected_outputs:
            self.assertIn(expected, output)

        self.assertEqual(self.shop._find_product("Widget").stock, 6)

    def test_manage_shop_invalid_option_and_error(self):
        inputs = [
            "9",               # invalid option
            "3", "Thing", "1",  # restock missing product => error
            "7"                # quit
        ]

        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            with patch('builtins.input', side_effect=inputs):
                self.ui.manage_shop()
        finally:
            sys.stdout = sys_stdout

        output = captured.getvalue()
        self.assertIn("Invalid option.", output)
        self.assertIn("Error: \"Product 'Thing' not found\"", output)


if __name__ == "__main__":
    unittest.main()
