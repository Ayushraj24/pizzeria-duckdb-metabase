from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
RANDOM_SEED = 42


@dataclass(frozen=True)
class MenuItem:
    item_id: int
    sku: str
    item_name: str
    category_id: int
    size_id: int
    unit_price: float


def write_csv(name: str, fieldnames: list[str], rows: list[dict]) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / f"{name}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def money(value: float) -> str:
    return f"{value:.2f}"


def iso_dt(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def make_static_dimensions() -> dict[str, list[dict]]:
    categories = [
        {"category_id": 1, "category_name": "Pizza"},
        {"category_id": 2, "category_name": "Sides"},
        {"category_id": 3, "category_name": "Drinks"},
        {"category_id": 4, "category_name": "Dessert"},
    ]
    sizes = [
        {"size_id": 1, "size_name": "Regular"},
        {"size_id": 2, "size_name": "Large"},
        {"size_id": 3, "size_name": "Bottle"},
        {"size_id": 4, "size_name": "Single"},
    ]
    menu_items = [
        MenuItem(101, "PZ-MARG-R", "Margherita Pizza", 1, 1, 9.99),
        MenuItem(102, "PZ-MARG-L", "Margherita Pizza", 1, 2, 13.99),
        MenuItem(103, "PZ-PEPP-R", "Pepperoni Pizza", 1, 1, 11.49),
        MenuItem(104, "PZ-PEPP-L", "Pepperoni Pizza", 1, 2, 15.99),
        MenuItem(105, "PZ-MEAT-R", "Meat Lovers Pizza", 1, 1, 13.69),
        MenuItem(106, "PZ-MEAT-L", "Meat Lovers Pizza", 1, 2, 19.99),
        MenuItem(201, "SD-FRIES-R", "Curly Fries", 2, 1, 3.99),
        MenuItem(202, "SD-FRIES-L", "Curly Fries", 2, 2, 5.99),
        MenuItem(203, "SD-WINGS-R", "Chicken Wings", 2, 1, 7.49),
        MenuItem(301, "DR-COKE-B", "Coke", 3, 3, 2.99),
        MenuItem(302, "DR-LEMON-B", "Lemonade", 3, 3, 3.49),
        MenuItem(401, "DS-BROWNIE-S", "Chocolate Brownie", 4, 4, 4.49),
    ]
    menu_rows = [
        {
            "item_id": item.item_id,
            "sku": item.sku,
            "item_name": item.item_name,
            "category_id": item.category_id,
            "size_id": item.size_id,
            "unit_price": money(item.unit_price),
        }
        for item in menu_items
    ]
    ingredients = [
        (1, "Dough", "grams", 15000, 60000),
        (2, "Tomato Sauce", "grams", 6000, 30000),
        (3, "Mozzarella", "grams", 7000, 35000),
        (4, "Pepperoni", "grams", 3000, 18000),
        (5, "Sausage", "grams", 2500, 15000),
        (6, "Bacon", "grams", 2000, 12000),
        (7, "Potatoes", "grams", 5000, 30000),
        (8, "Frying Oil", "milliliters", 2500, 16000),
        (9, "Chicken Wings", "grams", 3000, 16000),
        (10, "Coke Bottle", "units", 30, 220),
        (11, "Lemonade Bottle", "units", 25, 180),
        (12, "Brownie Mix", "grams", 2500, 12000),
        (13, "Pizza Box", "units", 40, 350),
    ]
    ingredient_rows = [
        {
            "ingredient_id": row[0],
            "ingredient_name": row[1],
            "unit": row[2],
            "reorder_level": row[3],
            "starting_stock_qty": row[4],
        }
        for row in ingredients
    ]
    vendors = [
        {"vendor_id": 1, "vendor_name": "Auckland Fresh Produce", "phone": "+64-09-111-0101"},
        {"vendor_id": 2, "vendor_name": "Southern Dairy Supply", "phone": "+64-09-111-0202"},
        {"vendor_id": 3, "vendor_name": "Kiwi Beverage Co", "phone": "+64-09-111-0303"},
        {"vendor_id": 4, "vendor_name": "Metro Packaging", "phone": "+64-09-111-0404"},
    ]
    staff = [
        (1, "Mia", "Wilson", "Manager", 32.0),
        (2, "Noah", "Brown", "Cashier", 24.5),
        (3, "Ava", "Taylor", "Chef", 29.0),
        (4, "Liam", "Singh", "Chef", 28.0),
        (5, "Olivia", "Patel", "Driver", 23.0),
        (6, "Ethan", "Martin", "Driver", 23.0),
    ]
    staff_rows = [
        {
            "staff_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "role": row[3],
            "hourly_rate": money(row[4]),
        }
        for row in staff
    ]
    recipes = [
        (101, 1, 280), (101, 2, 90), (101, 3, 140), (101, 13, 1),
        (102, 1, 380), (102, 2, 130), (102, 3, 210), (102, 13, 1),
        (103, 1, 280), (103, 2, 90), (103, 3, 130), (103, 4, 55), (103, 13, 1),
        (104, 1, 390), (104, 2, 130), (104, 3, 210), (104, 4, 85), (104, 13, 1),
        (105, 1, 300), (105, 2, 95), (105, 3, 170), (105, 4, 45), (105, 5, 45), (105, 6, 35), (105, 13, 1),
        (106, 1, 430), (106, 2, 145), (106, 3, 260), (106, 4, 70), (106, 5, 70), (106, 6, 55), (106, 13, 1),
        (201, 7, 220), (201, 8, 20),
        (202, 7, 360), (202, 8, 35),
        (203, 9, 320), (203, 8, 25),
        (301, 10, 1),
        (302, 11, 1),
        (401, 12, 110),
    ]
    recipe_rows = [
        {
            "recipe_id": idx + 1,
            "item_id": item_id,
            "ingredient_id": ingredient_id,
            "quantity_used": qty,
        }
        for idx, (item_id, ingredient_id, qty) in enumerate(recipes)
    ]
    return {
        "item_categories": categories,
        "item_sizes": sizes,
        "menu_items": menu_rows,
        "ingredients": ingredient_rows,
        "vendors": vendors,
        "staff": staff_rows,
        "recipes": recipe_rows,
    }


def make_addresses_and_customers(rng: random.Random) -> dict[str, list[dict]]:
    first_names = ["Amelia", "Jack", "Sophie", "Lucas", "Isla", "Oliver", "Harper", "Leo", "Ella", "Mason"]
    last_names = ["Smith", "Williams", "Jones", "Brown", "Taylor", "Wilson", "Singh", "Patel", "Martin", "Chen"]
    streets = ["Queen Street", "Ponsonby Road", "Dominion Road", "K Road", "Tamaki Drive", "Great North Road"]
    cities = ["Auckland Central", "Ponsonby", "Mount Eden", "Parnell", "Newmarket", "Grey Lynn"]
    addresses = []
    customers = []
    for address_id in range(1, 81):
        city = rng.choice(cities)
        addresses.append(
            {
                "address_id": address_id,
                "street": f"{rng.randint(10, 399)} {rng.choice(streets)}",
                "city": city,
                "postcode": rng.choice(["1010", "1021", "1023", "1052", "1024"]),
                "latitude": f"{-36.85 + rng.uniform(-0.06, 0.06):.6f}",
                "longitude": f"{174.76 + rng.uniform(-0.08, 0.08):.6f}",
            }
        )
        first = rng.choice(first_names)
        last = rng.choice(last_names)
        customers.append(
            {
                "customer_id": address_id,
                "first_name": first,
                "last_name": last,
                "phone": f"+64-21-{rng.randint(1000000, 9999999)}",
                "email": f"{first.lower()}.{last.lower()}{address_id}@example.com",
                "address_id": address_id,
            }
        )
    return {"addresses": addresses, "customers": customers}


def make_staff_shifts(start_date: date, days: int) -> list[dict]:
    rows = []
    shift_id = 1
    shift_templates = [
        (1, time(10, 0), time(18, 0)),
        (2, time(10, 0), time(18, 0)),
        (3, time(10, 0), time(18, 0)),
        (4, time(16, 0), time(23, 0)),
        (5, time(17, 0), time(23, 0)),
        (6, time(17, 0), time(23, 0)),
    ]
    for offset in range(days):
        day = start_date + timedelta(days=offset)
        for staff_id, start_t, end_t in shift_templates:
            if day.weekday() < 5 and staff_id == 6:
                continue
            start_dt = datetime.combine(day, start_t)
            end_dt = datetime.combine(day, end_t)
            rows.append(
                {
                    "shift_id": shift_id,
                    "staff_id": staff_id,
                    "shift_start": iso_dt(start_dt),
                    "shift_end": iso_dt(end_dt),
                }
            )
            shift_id += 1
    return rows


def make_purchases(start_date: date, days: int, rng: random.Random) -> list[dict]:
    ingredient_vendor = {
        1: 1, 2: 1, 3: 2, 4: 1, 5: 1, 6: 1, 7: 1,
        8: 1, 9: 1, 10: 3, 11: 3, 12: 2, 13: 4,
    }
    base_cost = {
        1: 0.010, 2: 0.014, 3: 0.022, 4: 0.030, 5: 0.028, 6: 0.032,
        7: 0.006, 8: 0.008, 9: 0.018, 10: 1.10, 11: 1.25, 12: 0.015, 13: 0.42,
    }
    base_qty = {
        1: 93000, 2: 36000, 3: 49000, 4: 16000, 5: 11000, 6: 9000,
        7: 34000, 8: 13000, 9: 18000, 10: 260, 11: 220, 12: 11000, 13: 290,
    }
    rows = []
    purchase_id = 1
    for offset in range(0, days, 3):
        purchase_date = start_date + timedelta(days=offset)
        for ingredient_id, vendor_id in ingredient_vendor.items():
            if rng.random() < 0.82:
                qty = base_qty[ingredient_id] * rng.uniform(0.65, 1.35)
                unit_cost = base_cost[ingredient_id] * rng.uniform(0.92, 1.12)
                purchased_at = datetime.combine(purchase_date, time(rng.randint(7, 11), rng.choice([0, 15, 30, 45])))
                rows.append(
                    {
                        "purchase_id": purchase_id,
                        "vendor_id": vendor_id,
                        "ingredient_id": ingredient_id,
                        "purchased_at": iso_dt(purchased_at),
                        "quantity": f"{qty:.3f}",
                        "unit_cost": f"{unit_cost:.4f}",
                    }
                )
                purchase_id += 1
    return rows


def make_orders(start_date: date, days: int, rng: random.Random) -> dict[str, list[dict]]:
    pizza_items = [101, 102, 103, 104, 105, 106]
    side_items = [201, 202, 203]
    drink_items = [301, 302]
    dessert_items = [401]
    price_lookup = {
        101: 9.99, 102: 13.99, 103: 11.49, 104: 15.99, 105: 13.69, 106: 19.99,
        201: 3.99, 202: 5.99, 203: 7.49, 301: 2.99, 302: 3.49, 401: 4.49,
    }
    orders = []
    order_items = []
    order_id = 1
    order_item_id = 1
    payment_methods = ["Card", "Cash", "Online"]
    statuses = ["Completed", "Completed", "Completed", "Completed", "Cancelled"]
    for offset in range(days):
        day = start_date + timedelta(days=offset)
        weekday = day.weekday()
        daily_orders = rng.randint(35, 55) if weekday < 4 else rng.randint(65, 95)
        for _ in range(daily_orders):
            hour_weights = [11, 12, 12, 13, 17, 18, 18, 19, 19, 20, 21]
            hour = rng.choice(hour_weights)
            ordered_at = datetime.combine(day, time(hour, rng.randint(0, 59), rng.randint(0, 59)))
            order_type = rng.choices(["Pickup", "Delivery"], weights=[0.55, 0.45], k=1)[0]
            discount = 0 if rng.random() > 0.12 else rng.choice([2.0, 3.0, 5.0])
            delivery_fee = 0 if order_type == "Pickup" else rng.choice([3.5, 4.0, 4.5])
            orders.append(
                {
                    "order_id": order_id,
                    "customer_id": rng.randint(1, 80),
                    "staff_id": rng.choice([2, 2, 3, 4]),
                    "ordered_at": iso_dt(ordered_at),
                    "order_type": order_type,
                    "payment_method": rng.choice(payment_methods),
                    "delivery_fee": money(delivery_fee),
                    "discount": money(discount),
                    "order_status": rng.choice(statuses),
                }
            )
            pizza_count = rng.choices([1, 2, 3], weights=[0.72, 0.24, 0.04], k=1)[0]
            for _ in range(pizza_count):
                item_id = rng.choice(pizza_items)
                qty = rng.choices([1, 2], weights=[0.9, 0.1], k=1)[0]
                order_items.append(
                    {
                        "order_item_id": order_item_id,
                        "order_id": order_id,
                        "item_id": item_id,
                        "quantity": qty,
                        "item_price": money(price_lookup[item_id]),
                    }
                )
                order_item_id += 1
            if rng.random() < 0.52:
                item_id = rng.choice(side_items)
                order_items.append(
                    {
                        "order_item_id": order_item_id,
                        "order_id": order_id,
                        "item_id": item_id,
                        "quantity": rng.choice([1, 1, 2]),
                        "item_price": money(price_lookup[item_id]),
                    }
                )
                order_item_id += 1
            if rng.random() < 0.64:
                item_id = rng.choice(drink_items)
                order_items.append(
                    {
                        "order_item_id": order_item_id,
                        "order_id": order_id,
                        "item_id": item_id,
                        "quantity": rng.choice([1, 2, 2, 3]),
                        "item_price": money(price_lookup[item_id]),
                    }
                )
                order_item_id += 1
            if rng.random() < 0.18:
                item_id = rng.choice(dessert_items)
                order_items.append(
                    {
                        "order_item_id": order_item_id,
                        "order_id": order_id,
                        "item_id": item_id,
                        "quantity": 1,
                        "item_price": money(price_lookup[item_id]),
                    }
                )
                order_item_id += 1
            order_id += 1
    return {"orders": orders, "order_items": order_items}


def make_inventory_adjustments(start_date: date, days: int, rng: random.Random) -> list[dict]:
    rows = []
    adjustment_id = 1
    reasons = ["Waste", "Spoilage", "Staff meal", "Stock count correction"]
    for offset in range(days):
        if rng.random() < 0.55:
            day = start_date + timedelta(days=offset)
            for _ in range(rng.randint(1, 3)):
                ingredient_id = rng.choice([1, 2, 3, 7, 8, 10, 11, 12, 13])
                qty = rng.uniform(20, 500) if ingredient_id not in [10, 11, 13] else rng.randint(1, 5)
                rows.append(
                    {
                        "adjustment_id": adjustment_id,
                        "ingredient_id": ingredient_id,
                        "adjusted_at": iso_dt(datetime.combine(day, time(22, rng.randint(0, 45)))),
                        "quantity": f"{qty:.3f}",
                        "reason": rng.choice(reasons),
                    }
                )
                adjustment_id += 1
    return rows


def main() -> None:
    rng = random.Random(RANDOM_SEED)
    start_date = date(2026, 1, 1)
    days = 90

    tables = {}
    tables.update(make_static_dimensions())
    tables.update(make_addresses_and_customers(rng))
    tables["staff_shifts"] = make_staff_shifts(start_date, days)
    tables["purchases"] = make_purchases(start_date, days, rng)
    tables.update(make_orders(start_date, days, rng))
    tables["inventory_adjustments"] = make_inventory_adjustments(start_date, days, rng)

    fields = {
        "addresses": ["address_id", "street", "city", "postcode", "latitude", "longitude"],
        "customers": ["customer_id", "first_name", "last_name", "phone", "email", "address_id"],
        "item_categories": ["category_id", "category_name"],
        "item_sizes": ["size_id", "size_name"],
        "menu_items": ["item_id", "sku", "item_name", "category_id", "size_id", "unit_price"],
        "ingredients": ["ingredient_id", "ingredient_name", "unit", "reorder_level", "starting_stock_qty"],
        "recipes": ["recipe_id", "item_id", "ingredient_id", "quantity_used"],
        "vendors": ["vendor_id", "vendor_name", "phone"],
        "purchases": ["purchase_id", "vendor_id", "ingredient_id", "purchased_at", "quantity", "unit_cost"],
        "staff": ["staff_id", "first_name", "last_name", "role", "hourly_rate"],
        "staff_shifts": ["shift_id", "staff_id", "shift_start", "shift_end"],
        "orders": [
            "order_id",
            "customer_id",
            "staff_id",
            "ordered_at",
            "order_type",
            "payment_method",
            "delivery_fee",
            "discount",
            "order_status",
        ],
        "order_items": ["order_item_id", "order_id", "item_id", "quantity", "item_price"],
        "inventory_adjustments": ["adjustment_id", "ingredient_id", "adjusted_at", "quantity", "reason"],
    }

    for name, fieldnames in fields.items():
        write_csv(name, fieldnames, tables[name])

    print(f"Generated {len(fields)} CSV files in {RAW_DIR}")
    print(f"Orders: {len(tables['orders'])}")
    print(f"Order items: {len(tables['order_items'])}")
    print(f"Purchases: {len(tables['purchases'])}")


if __name__ == "__main__":
    main()
