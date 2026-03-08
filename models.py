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
