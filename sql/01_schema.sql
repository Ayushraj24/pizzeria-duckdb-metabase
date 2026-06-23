DROP VIEW IF EXISTS vw_low_stock_alerts;
DROP VIEW IF EXISTS vw_profitability;
DROP VIEW IF EXISTS vw_staff_data;
DROP VIEW IF EXISTS vw_purchases_data;
DROP VIEW IF EXISTS vw_inventory_status;
DROP VIEW IF EXISTS vw_inventory_out;
DROP VIEW IF EXISTS vw_inventory_in;
DROP VIEW IF EXISTS vw_ingredient_usage;
DROP VIEW IF EXISTS vw_hourly_orders;
DROP VIEW IF EXISTS vw_daily_sales;
DROP VIEW IF EXISTS vw_sales_data;
DROP VIEW IF EXISTS vw_ingredient_avg_cost;

DROP TABLE IF EXISTS inventory_adjustments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS staff_shifts;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS vendors;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS item_sizes;
DROP TABLE IF EXISTS item_categories;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS addresses;

CREATE TABLE addresses (
    address_id INTEGER PRIMARY KEY,
    street VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    postcode VARCHAR NOT NULL,
    latitude DOUBLE,
    longitude DOUBLE
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    phone VARCHAR,
    email VARCHAR,
    address_id INTEGER NOT NULL REFERENCES addresses(address_id)
);

CREATE TABLE item_categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR NOT NULL
);

CREATE TABLE item_sizes (
    size_id INTEGER PRIMARY KEY,
    size_name VARCHAR NOT NULL
);

CREATE TABLE menu_items (
    item_id INTEGER PRIMARY KEY,
    sku VARCHAR NOT NULL,
    item_name VARCHAR NOT NULL,
    category_id INTEGER NOT NULL REFERENCES item_categories(category_id),
    size_id INTEGER NOT NULL REFERENCES item_sizes(size_id),
    unit_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE ingredients (
    ingredient_id INTEGER PRIMARY KEY,
    ingredient_name VARCHAR NOT NULL,
    unit VARCHAR NOT NULL,
    reorder_level DECIMAL(12, 3) NOT NULL,
    starting_stock_qty DECIMAL(12, 3) NOT NULL
);

CREATE TABLE recipes (
    recipe_id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES menu_items(item_id),
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    quantity_used DECIMAL(12, 3) NOT NULL
);

CREATE TABLE vendors (
    vendor_id INTEGER PRIMARY KEY,
    vendor_name VARCHAR NOT NULL,
    phone VARCHAR
);

CREATE TABLE purchases (
    purchase_id INTEGER PRIMARY KEY,
    vendor_id INTEGER NOT NULL REFERENCES vendors(vendor_id),
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    purchased_at TIMESTAMP NOT NULL,
    quantity DECIMAL(12, 3) NOT NULL,
    unit_cost DECIMAL(12, 4) NOT NULL
);

CREATE TABLE staff (
    staff_id INTEGER PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    hourly_rate DECIMAL(10, 2) NOT NULL
);

CREATE TABLE staff_shifts (
    shift_id INTEGER PRIMARY KEY,
    staff_id INTEGER NOT NULL REFERENCES staff(staff_id),
    shift_start TIMESTAMP NOT NULL,
    shift_end TIMESTAMP NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    staff_id INTEGER NOT NULL REFERENCES staff(staff_id),
    ordered_at TIMESTAMP NOT NULL,
    order_type VARCHAR NOT NULL,
    payment_method VARCHAR NOT NULL,
    delivery_fee DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) NOT NULL,
    order_status VARCHAR NOT NULL
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    item_id INTEGER NOT NULL REFERENCES menu_items(item_id),
    quantity INTEGER NOT NULL,
    item_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE inventory_adjustments (
    adjustment_id INTEGER PRIMARY KEY,
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    adjusted_at TIMESTAMP NOT NULL,
    quantity DECIMAL(12, 3) NOT NULL,
    reason VARCHAR NOT NULL
);

