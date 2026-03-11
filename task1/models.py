from abc import ABC, abstractmethod


class Item(ABC):
    def __init__(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = price

    @abstractmethod
    def get_info(self):
        """Abstract method to return item info"""
        pass


class Product(Item):
    def __init__(self, item_id, name, price, quantity, category):
        super().__init__(item_id, name, price)
        self.__quantity = quantity
        self.category = category

    def update_quantity(self, amount):
        """Increment quantity by amount"""
        self.__quantity += amount

    def set_quantity(self, new_quantity):
        """Setter method to directly set product quantity"""
        self.__quantity = new_quantity

    def get_quantity(self):
        """Getter method for product quantity"""
        return self.__quantity

    def get_info(self):
        return f"{self.item_id} - {self.name}, ${self.price}, Qty: {self.__quantity}, Category: {self.category}"


class Inventory:
    def __init__(self):
        self.__products = {}

    def add_product(self, product):
        """Add a product object to inventory"""
        self.__products[product.item_id] = product

    def remove_product(self, item_id):
        """Remove a product by its ID"""
        if item_id in self.__products:
            del self.__products[item_id]
            return True
        return False

    def search_product(self, item_id):
        """Search for a product by ID"""
        return self.__products.get(item_id, None)

    def list_all_products(self):
        """Return list of product info strings"""
        return [p.get_info() for p in self.__products.values()]

    def category_summary(self):
        """Return dictionary of category -> total quantity"""
        summary = {}
        for p in self.__products.values():
            summary[p.category] = summary.get(p.category, 0) + p.get_quantity()
        return summary

    def total_quantity(self):
        """Return total quantity of all products"""
        return sum(p.get_quantity() for p in self.__products.values())

    def low_stock_count(self, threshold=10):
        """Return count of products below threshold"""
        return sum(1 for p in self.__products.values() if p.get_quantity() < threshold)

    def avg_price(self):
        """Return average price of products"""
        if not self.__products:
            return 0
        return sum(p.price for p in self.__products.values()) / len(self.__products)

    def category_count(self):
        """Return number of distinct categories"""
        return len(set(p.category for p in self.__products.values()))

    def update_product(self, item_id, new_price=None, new_quantity=None):
        """Update product price and/or quantity by item_id"""
        product = self.__products.get(item_id)
        if not product:
            return False  # product not found

        if new_price is not None:
            product.price = new_price
        if new_quantity is not None:
            product.set_quantity(new_quantity)
        return True
