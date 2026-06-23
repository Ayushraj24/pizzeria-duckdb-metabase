CREATE OR REPLACE VIEW vw_sales_data AS
SELECT
    o.order_id,
    oi.order_item_id,
    CAST(o.ordered_at AS DATE) AS business_date,
    EXTRACT(hour FROM o.ordered_at) AS order_hour,
    o.ordered_at,
    o.order_status,
    o.order_type,
    o.payment_method,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    a.city,
    s.staff_id,
    s.first_name || ' ' || s.last_name AS staff_name,
    mi.item_id,
    mi.sku,
    mi.item_name,
    ic.category_name,
    isz.size_name,
    oi.quantity,
    oi.item_price,
    oi.quantity * oi.item_price AS gross_line_sales,
    o.discount,
    o.delivery_fee
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN menu_items mi ON oi.item_id = mi.item_id
JOIN item_categories ic ON mi.category_id = ic.category_id
JOIN item_sizes isz ON mi.size_id = isz.size_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN addresses a ON c.address_id = a.address_id
JOIN staff s ON o.staff_id = s.staff_id;

CREATE OR REPLACE VIEW vw_daily_sales AS
WITH order_totals AS (
    SELECT
        o.order_id,
        CAST(o.ordered_at AS DATE) AS business_date,
        SUM(oi.quantity * oi.item_price) AS item_sales,
        MAX(o.delivery_fee) AS delivery_fee,
        MAX(o.discount) AS discount
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY o.order_id, CAST(o.ordered_at AS DATE)
)
SELECT
    business_date,
    COUNT(*) AS orders,
    ROUND(SUM(item_sales), 2) AS gross_sales,
    ROUND(SUM(delivery_fee), 2) AS delivery_fees,
    ROUND(SUM(discount), 2) AS discounts,
    ROUND(SUM(item_sales + delivery_fee - discount), 2) AS net_sales,
    ROUND(AVG(item_sales + delivery_fee - discount), 2) AS avg_order_value,
    (
        SELECT SUM(oi.quantity)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_status = 'Completed'
          AND CAST(o.ordered_at AS DATE) = order_totals.business_date
    ) AS items_sold
FROM order_totals
GROUP BY business_date
ORDER BY business_date;

CREATE OR REPLACE VIEW vw_hourly_orders AS
WITH order_totals AS (
    SELECT
        o.order_id,
        CAST(o.ordered_at AS DATE) AS business_date,
        EXTRACT(hour FROM o.ordered_at) AS order_hour,
        SUM(oi.quantity * oi.item_price) + MAX(o.delivery_fee) - MAX(o.discount) AS net_sales
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY o.order_id, CAST(o.ordered_at AS DATE), EXTRACT(hour FROM o.ordered_at)
)
SELECT
    business_date,
    order_hour,
    COUNT(*) AS orders,
    ROUND(SUM(net_sales), 2) AS net_sales
FROM order_totals
GROUP BY business_date, order_hour
ORDER BY business_date, order_hour;

CREATE OR REPLACE VIEW vw_ingredient_usage AS
SELECT
    CAST(o.ordered_at AS DATE) AS business_date,
    i.ingredient_id,
    i.ingredient_name,
    i.unit,
    SUM(oi.quantity * r.quantity_used) AS quantity_used
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN recipes r ON oi.item_id = r.item_id
JOIN ingredients i ON r.ingredient_id = i.ingredient_id
WHERE o.order_status = 'Completed'
GROUP BY
    CAST(o.ordered_at AS DATE),
    i.ingredient_id,
    i.ingredient_name,
    i.unit;

CREATE OR REPLACE VIEW vw_inventory_in AS
SELECT
    p.ingredient_id,
    i.ingredient_name,
    i.unit,
    SUM(p.quantity) AS purchased_qty,
    ROUND(SUM(p.quantity * p.unit_cost), 2) AS purchase_cost
FROM purchases p
JOIN ingredients i ON p.ingredient_id = i.ingredient_id
GROUP BY p.ingredient_id, i.ingredient_name, i.unit;

CREATE OR REPLACE VIEW vw_inventory_out AS
WITH usage_out AS (
    SELECT
        ingredient_id,
        SUM(quantity_used) AS used_qty
    FROM vw_ingredient_usage
    GROUP BY ingredient_id
),
adjustments_out AS (
    SELECT
        ingredient_id,
        SUM(quantity) AS adjusted_qty
    FROM inventory_adjustments
    GROUP BY ingredient_id
)
SELECT
    i.ingredient_id,
    i.ingredient_name,
    i.unit,
    COALESCE(u.used_qty, 0) AS used_qty,
    COALESCE(a.adjusted_qty, 0) AS adjusted_qty,
    COALESCE(u.used_qty, 0) + COALESCE(a.adjusted_qty, 0) AS total_out_qty
FROM ingredients i
LEFT JOIN usage_out u ON i.ingredient_id = u.ingredient_id
LEFT JOIN adjustments_out a ON i.ingredient_id = a.ingredient_id;

CREATE OR REPLACE VIEW vw_inventory_status AS
SELECT
    i.ingredient_id,
    i.ingredient_name,
    i.unit,
    i.starting_stock_qty,
    i.reorder_level,
    COALESCE(inv_in.purchased_qty, 0) AS purchased_qty,
    COALESCE(inv_out.used_qty, 0) AS used_qty,
    COALESCE(inv_out.adjusted_qty, 0) AS adjusted_qty,
    i.starting_stock_qty + COALESCE(inv_in.purchased_qty, 0) - COALESCE(inv_out.total_out_qty, 0) AS current_stock_qty,
    ROUND(
        100.0 * (i.starting_stock_qty + COALESCE(inv_in.purchased_qty, 0) - COALESCE(inv_out.total_out_qty, 0))
        / NULLIF(i.starting_stock_qty + COALESCE(inv_in.purchased_qty, 0), 0),
        2
    ) AS stock_coverage_pct,
    CASE
        WHEN i.starting_stock_qty + COALESCE(inv_in.purchased_qty, 0) - COALESCE(inv_out.total_out_qty, 0) <= i.reorder_level THEN 'Reorder now'
        WHEN i.starting_stock_qty + COALESCE(inv_in.purchased_qty, 0) - COALESCE(inv_out.total_out_qty, 0) <= i.reorder_level * 1.5 THEN 'Watch'
        ELSE 'Healthy'
    END AS stock_status
FROM ingredients i
LEFT JOIN vw_inventory_in inv_in ON i.ingredient_id = inv_in.ingredient_id
LEFT JOIN vw_inventory_out inv_out ON i.ingredient_id = inv_out.ingredient_id;

CREATE OR REPLACE VIEW vw_low_stock_alerts AS
SELECT *
FROM vw_inventory_status
WHERE stock_status IN ('Reorder now', 'Watch');

CREATE OR REPLACE VIEW vw_ingredient_avg_cost AS
SELECT
    ingredient_id,
    SUM(quantity * unit_cost) / NULLIF(SUM(quantity), 0) AS avg_unit_cost
FROM purchases
GROUP BY ingredient_id;

CREATE OR REPLACE VIEW vw_purchases_data AS
SELECT
    p.purchase_id,
    CAST(p.purchased_at AS DATE) AS purchase_date,
    p.purchased_at,
    v.vendor_id,
    v.vendor_name,
    i.ingredient_id,
    i.ingredient_name,
    i.unit,
    p.quantity,
    p.unit_cost,
    ROUND(p.quantity * p.unit_cost, 2) AS purchase_cost
FROM purchases p
JOIN vendors v ON p.vendor_id = v.vendor_id
JOIN ingredients i ON p.ingredient_id = i.ingredient_id;

CREATE OR REPLACE VIEW vw_staff_data AS
SELECT
    ss.shift_id,
    s.staff_id,
    s.first_name || ' ' || s.last_name AS staff_name,
    s.role,
    CAST(ss.shift_start AS DATE) AS business_date,
    ss.shift_start,
    ss.shift_end,
    ROUND(date_diff('minute', ss.shift_start, ss.shift_end) / 60.0, 2) AS hours_worked,
    s.hourly_rate,
    ROUND((date_diff('minute', ss.shift_start, ss.shift_end) / 60.0) * s.hourly_rate, 2) AS labor_cost
FROM staff_shifts ss
JOIN staff s ON ss.staff_id = s.staff_id;

CREATE OR REPLACE VIEW vw_profitability AS
WITH sales AS (
    SELECT
        business_date,
        SUM(net_sales) AS net_sales,
        SUM(orders) AS orders
    FROM vw_daily_sales
    GROUP BY business_date
),
ingredient_cost AS (
    SELECT
        u.business_date,
        SUM(u.quantity_used * COALESCE(c.avg_unit_cost, 0)) AS ingredient_cost
    FROM vw_ingredient_usage u
    LEFT JOIN vw_ingredient_avg_cost c ON u.ingredient_id = c.ingredient_id
    GROUP BY u.business_date
),
labor AS (
    SELECT
        business_date,
        SUM(labor_cost) AS labor_cost
    FROM vw_staff_data
    GROUP BY business_date
)
SELECT
    s.business_date,
    s.orders,
    ROUND(s.net_sales, 2) AS net_sales,
    ROUND(COALESCE(ic.ingredient_cost, 0), 2) AS ingredient_cost,
    ROUND(COALESCE(l.labor_cost, 0), 2) AS labor_cost,
    ROUND(s.net_sales - COALESCE(ic.ingredient_cost, 0) - COALESCE(l.labor_cost, 0), 2) AS estimated_profit,
    ROUND(
        100.0 * (s.net_sales - COALESCE(ic.ingredient_cost, 0) - COALESCE(l.labor_cost, 0))
        / NULLIF(s.net_sales, 0),
        2
    ) AS estimated_margin_pct
FROM sales s
LEFT JOIN ingredient_cost ic ON s.business_date = ic.business_date
LEFT JOIN labor l ON s.business_date = l.business_date
ORDER BY s.business_date;

