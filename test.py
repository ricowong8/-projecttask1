from models import Product, Inventory

inv = Inventory()

# Add new product
p1 = Product("001", "Laptop",5000,10,"Electronics")
inv.add_product(p1)

print("Before update", inv.list_all_products())

inv.update_product("001",new_price=5500, new_quantity=15)

print("After update" , inv.list_all_products())