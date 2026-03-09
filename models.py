# ByteBites Models
#
# Customer  – A registered user with an id, name, email, and purchase history.
#              Can place, cancel, or reorder orders.
# Item      – A food/drink product with an id, name, price, category, and popularity rating.
# Menu      – A collection of Items that supports browsing and filtering by category.
# Order     – A transaction grouping Items with quantities, tracking cost and status history.

from datetime import datetime


class Item:
    def __init__(self, item_id, name, price, category, popularity_rating):
        self._item_id = item_id
        self._name = name
        self._price = price
        self._category = category
        self._popularity_rating = popularity_rating

    def get_item_id(self):
        return self._item_id

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_category(self):
        return self._category

    def get_popularity_rating(self):
        return self._popularity_rating


class Menu:
    def __init__(self):
        self._items = []

    def get_items(self):
        return self._items

    def add_item(self, item):
        self._items.append(item)

    def remove_item(self, item):
        self._items.remove(item)

    def filter_by_category(self, category):
        return [item for item in self._items if item.get_category() == category]

    # Return items sorted by price (ascending by default); does not mutate the menu.
    def sort_by_price(self, ascending=True):
        return sorted(self._items, key=lambda item: item.get_price(), reverse=not ascending)

    # Return items sorted by popularity rating (descending by default, highest first).
    def sort_by_popularity(self, ascending=False):
        return sorted(self._items, key=lambda item: item.get_popularity_rating(), reverse=not ascending)

    # Return items sorted alphabetically by name.
    def sort_by_name(self):
        return sorted(self._items, key=lambda item: item.get_name())

    # Return items whose price falls within [min_price, max_price].
    def filter_by_price_range(self, min_price, max_price):
        return [item for item in self._items if min_price <= item.get_price() <= max_price]

    # Return items with a popularity rating >= min_rating.
    def filter_by_minimum_rating(self, min_rating):
        return [item for item in self._items if item.get_popularity_rating() >= min_rating]


class Order:
    def __init__(self, order_id):
        self._order_id = order_id
        self._items = {}              # {Item: int} mapping items to quantities
        self._status_history = {"placed": datetime.now()}

    def get_order_id(self):
        return self._order_id

    def get_items(self):
        return self._items

    def add_item(self, item, quantity=1):
        if item in self._items:
            self._items[item] += quantity
        else:
            self._items[item] = quantity

    def remove_item(self, item):
        if item in self._items:
            del self._items[item]

    def compute_total(self):
        return sum(item.get_price() * qty for item, qty in self._items.items())

    # Return (Item, quantity) tuples sorted by item price (ascending by default).
    def sort_items_by_price(self, ascending=True):
        return sorted(self._items.items(), key=lambda pair: pair[0].get_price(), reverse=not ascending)

    # Return the total cost including tax; tax_rate is a decimal (e.g. 0.08 for 8%).
    def compute_total_with_tax(self, tax_rate):
        return round(self.compute_total() * (1 + tax_rate), 2)

    # Return the total number of items (sum of all quantities) in the order.
    def get_item_count(self):
        return sum(self._items.values())

    def get_status_history(self):
        return self._status_history

    def get_current_status(self):
        return list(self._status_history.keys())[-1]

    def set_status(self, status):
        self._status_history[status] = datetime.now()


class Customer:
    def __init__(self, customer_id, name, email):
        self._customer_id = customer_id
        self._name = name
        self._email = email
        self._purchase_history = []

    def get_customer_id(self):
        return self._customer_id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def get_purchase_history(self):
        return self._purchase_history

    def add_to_history(self, order):
        self._purchase_history.append(order)

    def place_order(self, order):
        order.set_status("placed")
        self._purchase_history.append(order)

    def cancel_order(self, order):
        order.set_status("canceled")

    def reorder(self, order):
        new_order = Order(order.get_order_id() + 1000)
        for item, qty in order.get_items().items():
            new_order.add_item(item, qty)
        new_order.set_status("placed")
        self._purchase_history.append(new_order)
        return new_order

    # Return the total amount spent across all orders in purchase history.
    def get_total_spent(self):
        return sum(order.compute_total() for order in self._purchase_history
           if order.get_current_status() != "canceled")


# ── Quick demo scenario ──────────────────────────────────────────────
if __name__ == "__main__":
    # 1. Create items across different categories and price ranges
    burger   = Item(1, "Spicy Burger",    8.99, "Food",     4.5)
    salad    = Item(2, "Garden Salad",    6.49, "Food",     4.2)
    soda     = Item(3, "Large Soda",      2.49, "Drinks",   3.8)
    latte    = Item(4, "Iced Latte",      4.99, "Drinks",   4.6)
    cake     = Item(5, "Chocolate Cake",  5.99, "Desserts", 4.7)
    cookie   = Item(6, "Oatmeal Cookie",  1.99, "Desserts", 3.5)

    # 2. Build the menu
    menu = Menu()
    for item in [burger, salad, soda, latte, cake, cookie]:
        menu.add_item(item)

    # 3. Sorting
    print("=== Sort by price (cheapest first) ===")
    for i in menu.sort_by_price():
        print(f"  {i.get_name():20s} ${i.get_price():.2f}")

    print("\n=== Sort by popularity (best first) ===")
    for i in menu.sort_by_popularity():
        print(f"  {i.get_name():20s} rating {i.get_popularity_rating()}")

    print("\n=== Sort by name ===")
    for i in menu.sort_by_name():
        print(f"  {i.get_name()}")

    # 4. Filtering
    print("\n=== Drinks only ===")
    for i in menu.filter_by_category("Drinks"):
        print(f"  {i.get_name()}")

    print("\n=== Price $2 – $6 ===")
    for i in menu.filter_by_price_range(2, 6):
        print(f"  {i.get_name():20s} ${i.get_price():.2f}")

    print("\n=== Rating >= 4.5 ===")
    for i in menu.filter_by_minimum_rating(4.5):
        print(f"  {i.get_name():20s} rating {i.get_popularity_rating()}")

    # 5. Build an order and compute totals
    order = Order(201)
    order.add_item(burger, 2)
    order.add_item(latte, 1)
    order.add_item(cake, 3)

    print("\n=== Order #201 ===")
    print(f"  Items (sorted by price):")
    for item, qty in order.sort_items_by_price():
        print(f"    {item.get_name():20s} x{qty}  ${item.get_price() * qty:.2f}")
    print(f"  Item count:   {order.get_item_count()}")
    print(f"  Subtotal:     ${order.compute_total():.2f}")
    print(f"  Total w/ 8%:  ${order.compute_total_with_tax(0.08):.2f}")

    # 6. Customer lifetime spend (with a canceled order excluded)
    customer = Customer(1, "Alice", "alice@example.com")
    customer.place_order(order)

    small_order = Order(202)
    small_order.add_item(cookie, 2)
    customer.place_order(small_order)
    customer.cancel_order(small_order)  # this one shouldn't count

    print(f"\n=== Customer: {customer.get_name()} ===")
    print(f"  Orders:       {len(customer.get_purchase_history())}")
    print(f"  Total spent:  ${customer.get_total_spent():.2f}  (canceled order excluded)")
