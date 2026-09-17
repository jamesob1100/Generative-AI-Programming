from shop import Shop


class ShopUI:
    """A simple command-line interface for managing shop.py inventory.
    
    Tests:
    >>> shop = Shop("Test Shop")
    >>> ui = ShopUI(shop)
    """
    def __init__(self, shop: Shop):
        self.shop = shop

    def manage_shop(self):
        while True:
            print("\nShop Manager")
            print("1. Add product")
            print("2. Remove product")
            print("3. Restock product")
            print("4. Sell product")
            print("5. Show all products")
            print("6. Show low-stock products")
            print("7. Quit")
            choice = input("Select an option: ").strip()

            try:
                if choice == "1":
                    name = input("Product name: ").strip()
                    stock = int(input("Starting stock: ").strip())
                    if self.shop.add_product(name, stock):
                        print("Product added.")
                    else:
                        print("Product already exists.")
                elif choice == "2":
                    name = input("Product name: ").strip()
                    if self.shop.remove_product(name):
                        print("Product removed.")
                    else:
                        print("Product not found.")
                elif choice == "3":
                    name = input("Product name: ").strip()
                    q = int(input("Quantity to add: ").strip())
                    self.shop.restock(name, q)
                    print("Product restocked.")
                elif choice == "4":
                    name = input("Product name: ").strip()
                    q = int(input("Quantity to sell: ").strip())
                    self.shop.sell(name, q)
                    print("Product sold.")
                elif choice == "5":
                    self.shop.print_product_list(low_stock_only=False)
                elif choice == "6":
                    self.shop.print_product_list(low_stock_only=True)
                elif choice == "7":
                    print("Goodbye.")
                    break
                else:
                    print("Invalid option.")
            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    shop = Shop("My Shop")
    ui = ShopUI(shop)
    ui.manage_shop()