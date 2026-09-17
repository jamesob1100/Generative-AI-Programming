import unittest

from product import Product


class TestProduct(unittest.TestCase):
    def test_init_and_properties(self):
        p = Product("Widget", 10)
        self.assertEqual(p.name, "Widget")
        self.assertEqual(p.stock, 10)

    def test_stock_is_low(self):
        p = Product("Widget", 10)
        self.assertFalse(p.stock_is_low())
        p.stock = 2
        self.assertTrue(p.stock_is_low())

    def test_stock_setter_validates(self):
        p = Product("Widget", 10)
        with self.assertRaises(ValueError):
            p.stock = -5

    def test_init_invalid_inputs(self):
        with self.assertRaises(ValueError):
            Product("", 5)

        with self.assertRaises(ValueError):
            Product("Widget", -1)

        with self.assertRaises(ValueError):
            Product("Widget", "1")

    def test_repr(self):
        p = Product("Widget", 10)
        self.assertEqual(repr(p), "Product(name='Widget', stock=10)")


if __name__ == "__main__":
    unittest.main()
