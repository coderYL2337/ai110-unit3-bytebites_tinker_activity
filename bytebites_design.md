# ByteBites UML-Style Class Diagrams

## 1. Customer

```
+-------------------------------------------+
|               Customer                    |
+-------------------------------------------+
| - customer_id: Integer                    |
| - name: String                            |
| - email: String                           |
| - purchase_history: List<Order>           |
+-------------------------------------------+
| + get_customer_id(): Integer              |
| + get_name(): String                      |
| + get_email(): String                     |
| + get_purchase_history(): List            |
| + add_to_history(order: Order)            |
| + place_order(order: Order)               |
| + receive_order(order: Order)             |
| + cancel_order(order: Order)              |
| + reorder(order: Order): Order            |
+-------------------------------------------+
```

## 2. Item

```
+-----------------------------------+
|              Item                 |
+-----------------------------------+
| - item_id: Integer                |
| - name: String                    |
| - price: Float                    |
| - category: String               |
| - popularity_rating: Float        |
+-----------------------------------+
| + get_item_id(): Integer          |
| + get_name(): String              |
| + get_price(): Float              |
| + get_category(): String          |
| + get_popularity_rating(): Float  |
+-----------------------------------+
```

## 3. Menu

```
+-----------------------------------+
|              Menu                 |
+-----------------------------------+
| - items: List<Item>               |
+-----------------------------------+
| + get_items(): List<Item>         |
| + add_item(item: Item)            |
| + remove_item(item: Item)         |
| + filter_by_category(category:    |
|       String): List<Item>         |
+-----------------------------------+
```

## 4. Order

```
+----------------------------------------------+
|                   Order                      |
+----------------------------------------------+
| - order_id: Integer                          |
| - items: Dict<Item, Integer>                 |
| - status_history: Dict<String, DateTime>     |
+----------------------------------------------+
| + get_order_id(): Integer                    |
| + get_items(): Dict<Item, Integer>           |
| + add_item(item: Item, quantity: Integer)    |
| + remove_item(item: Item)                    |
| + compute_total(): Float                     |
| + get_status_history(): Dict<String,DateTime>|
| + get_current_status(): String               |
| + set_status(status: String)                 |
+----------------------------------------------+
```
