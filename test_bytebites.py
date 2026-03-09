import pytest
from models import Item, Menu, Order, Customer


# ── Fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def sample_items():
    burger = Item(1, "Spicy Burger", 8.99, "Food", 4.5)
    soda   = Item(2, "Large Soda", 2.49, "Drinks", 3.8)
    cake   = Item(3, "Chocolate Cake", 5.99, "Desserts", 4.7)
    return burger, soda, cake


@pytest.fixture
def loaded_menu(sample_items):
    burger, soda, cake = sample_items
    menu = Menu()
    menu.add_item(burger)
    menu.add_item(soda)
    menu.add_item(cake)
    return menu


@pytest.fixture
def loaded_order(sample_items):
    burger, soda, _ = sample_items
    order = Order(101)
    order.add_item(burger, 2)
    order.add_item(soda, 1)
    return order


# ── Item Tests ────────────────────────────────────────────────────────

class TestItem:
    def test_getters(self, sample_items):
        burger, _, _ = sample_items
        assert burger.get_item_id() == 1
        assert burger.get_name() == "Spicy Burger"
        assert burger.get_price() == 8.99
        assert burger.get_category() == "Food"
        assert burger.get_popularity_rating() == 4.5


# ── Menu Tests ────────────────────────────────────────────────────────

class TestMenu:
    def test_add_and_get_items(self, loaded_menu):
        assert len(loaded_menu.get_items()) == 3

    def test_remove_item(self, loaded_menu, sample_items):
        _, soda, _ = sample_items
        loaded_menu.remove_item(soda)
        assert len(loaded_menu.get_items()) == 2

    # -- Filtering --

    def test_filter_by_category(self, loaded_menu):
        drinks = loaded_menu.filter_by_category("Drinks")
        assert len(drinks) == 1
        assert drinks[0].get_name() == "Large Soda"

    def test_filter_by_category_no_match(self, loaded_menu):
        assert loaded_menu.filter_by_category("Appetizers") == []

    def test_filter_by_price_range(self, loaded_menu):
        result = loaded_menu.filter_by_price_range(2, 6)
        names = [i.get_name() for i in result]
        assert "Large Soda" in names
        assert "Chocolate Cake" in names
        assert "Spicy Burger" not in names

    def test_filter_by_price_range_boundary(self, loaded_menu):
        result = loaded_menu.filter_by_price_range(2.49, 5.99)
        assert len(result) == 2  # soda at 2.49 and cake at 5.99 included

    def test_filter_by_minimum_rating(self, loaded_menu):
        result = loaded_menu.filter_by_minimum_rating(4.5)
        names = [i.get_name() for i in result]
        assert "Spicy Burger" in names
        assert "Chocolate Cake" in names
        assert "Large Soda" not in names

    # -- Sorting --

    def test_sort_by_price_ascending(self, loaded_menu):
        result = loaded_menu.sort_by_price()
        prices = [i.get_price() for i in result]
        assert prices == sorted(prices)

    def test_sort_by_price_descending(self, loaded_menu):
        result = loaded_menu.sort_by_price(ascending=False)
        prices = [i.get_price() for i in result]
        assert prices == sorted(prices, reverse=True)

    def test_sort_by_popularity(self, loaded_menu):
        result = loaded_menu.sort_by_popularity()
        ratings = [i.get_popularity_rating() for i in result]
        assert ratings == sorted(ratings, reverse=True)

    def test_sort_by_name(self, loaded_menu):
        result = loaded_menu.sort_by_name()
        names = [i.get_name() for i in result]
        assert names == sorted(names)

    def test_sort_does_not_mutate(self, loaded_menu):
        original = [i.get_name() for i in loaded_menu.get_items()]
        loaded_menu.sort_by_price()
        loaded_menu.sort_by_popularity()
        loaded_menu.sort_by_name()
        assert [i.get_name() for i in loaded_menu.get_items()] == original


# ── Order Tests ───────────────────────────────────────────────────────

class TestOrder:
    def test_compute_total(self, loaded_order):
        # 8.99 * 2 + 2.49 * 1 = 20.47
        assert loaded_order.compute_total() == pytest.approx(20.47)

    def test_empty_order_total(self):
        order = Order(999)
        assert order.compute_total() == 0.0

    def test_empty_order_item_count(self):
        order = Order(999)
        assert order.get_item_count() == 0

    def test_empty_order_total_with_tax(self):
        order = Order(999)
        assert order.compute_total_with_tax(0.08) == 0.0

    def test_compute_total_with_tax(self, loaded_order):
        expected = round(20.47 * 1.08, 2)
        assert loaded_order.compute_total_with_tax(0.08) == pytest.approx(expected)

    def test_get_item_count(self, loaded_order):
        assert loaded_order.get_item_count() == 3  # 2 burgers + 1 soda

    def test_add_item_increases_quantity(self, loaded_order, sample_items):
        burger, _, _ = sample_items
        loaded_order.add_item(burger, 1)
        assert loaded_order.get_item_count() == 4

    def test_remove_item(self, loaded_order, sample_items):
        _, soda, _ = sample_items
        loaded_order.remove_item(soda)
        assert loaded_order.get_item_count() == 2
        assert loaded_order.compute_total() == pytest.approx(17.98)

    def test_sort_items_by_price_ascending(self, loaded_order):
        result = loaded_order.sort_items_by_price()
        prices = [item.get_price() for item, _ in result]
        assert prices == sorted(prices)

    def test_sort_items_by_price_descending(self, loaded_order):
        result = loaded_order.sort_items_by_price(ascending=False)
        prices = [item.get_price() for item, _ in result]
        assert prices == sorted(prices, reverse=True)

    def test_status_flow(self):
        order = Order(200)
        assert order.get_current_status() == "placed"
        order.set_status("preparing")
        assert order.get_current_status() == "preparing"


# ── Customer Tests ────────────────────────────────────────────────────

class TestCustomer:
    def test_getters(self):
        c = Customer(1, "Alice", "alice@example.com")
        assert c.get_customer_id() == 1
        assert c.get_name() == "Alice"
        assert c.get_email() == "alice@example.com"

    def test_place_order(self, loaded_order):
        c = Customer(1, "Alice", "alice@example.com")
        c.place_order(loaded_order)
        assert len(c.get_purchase_history()) == 1
        assert loaded_order.get_current_status() == "placed"

    def test_cancel_order(self, loaded_order):
        c = Customer(1, "Alice", "alice@example.com")
        c.place_order(loaded_order)
        c.cancel_order(loaded_order)
        assert loaded_order.get_current_status() == "canceled"

    def test_reorder(self, loaded_order):
        c = Customer(1, "Alice", "alice@example.com")
        c.place_order(loaded_order)
        new = c.reorder(loaded_order)
        assert new.get_order_id() == loaded_order.get_order_id() + 1000
        assert new.compute_total() == loaded_order.compute_total()
        assert len(c.get_purchase_history()) == 2

    def test_get_total_spent(self, sample_items):
        burger, soda, _ = sample_items
        c = Customer(1, "Alice", "alice@example.com")

        o1 = Order(101)
        o1.add_item(burger, 1)  # 8.99
        c.place_order(o1)

        o2 = Order(102)
        o2.add_item(soda, 2)  # 4.98
        c.place_order(o2)

        assert c.get_total_spent() == pytest.approx(13.97)

    def test_get_total_spent_excludes_canceled(self, sample_items):
        burger, soda, _ = sample_items
        c = Customer(1, "Alice", "alice@example.com")

        o1 = Order(101)
        o1.add_item(burger, 1)  # 8.99
        c.place_order(o1)

        o2 = Order(102)
        o2.add_item(soda, 2)  # 4.98
        c.place_order(o2)
        c.cancel_order(o2)

        assert c.get_total_spent() == pytest.approx(8.99)

    def test_get_total_spent_no_orders(self):
        c = Customer(1, "Alice", "alice@example.com")
        assert c.get_total_spent() == 0.0
