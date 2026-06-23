-- Metabase card starters.
-- Use these in Metabase's SQL editor after connecting the DuckDB database.

-- 1. KPI: total net sales
SELECT ROUND(SUM(net_sales), 2) AS total_net_sales
FROM vw_daily_sales;

-- 2. KPI: completed orders
SELECT SUM(orders) AS completed_orders
FROM vw_daily_sales;

-- 3. KPI: estimated profit
SELECT ROUND(SUM(estimated_profit), 2) AS estimated_profit
FROM vw_profitability;

-- 4. Daily sales trend
SELECT business_date, net_sales, orders, avg_order_value
FROM vw_daily_sales
ORDER BY business_date;

-- 5. Hourly demand pattern
SELECT order_hour, SUM(orders) AS orders, ROUND(SUM(net_sales), 2) AS net_sales
FROM vw_hourly_orders
GROUP BY order_hour
ORDER BY order_hour;

-- 6. Sales by menu category
SELECT
    category_name,
    ROUND(SUM(gross_line_sales), 2) AS gross_sales,
    SUM(quantity) AS items_sold
FROM vw_sales_data
WHERE order_status = 'Completed'
GROUP BY category_name
ORDER BY gross_sales DESC;

-- 7. Top menu items
SELECT
    item_name,
    size_name,
    ROUND(SUM(gross_line_sales), 2) AS gross_sales,
    SUM(quantity) AS items_sold
FROM vw_sales_data
WHERE order_status = 'Completed'
GROUP BY item_name, size_name
ORDER BY gross_sales DESC;

-- 8. Low-stock inventory
SELECT
    ingredient_name,
    unit,
    current_stock_qty,
    reorder_level,
    stock_coverage_pct,
    stock_status
FROM vw_low_stock_alerts
ORDER BY stock_coverage_pct;

-- 9. Purchase cost by vendor
SELECT
    vendor_name,
    ROUND(SUM(purchase_cost), 2) AS purchase_cost
FROM vw_purchases_data
GROUP BY vendor_name
ORDER BY purchase_cost DESC;

-- 10. Staff labor cost by role
SELECT
    role,
    ROUND(SUM(hours_worked), 2) AS hours_worked,
    ROUND(SUM(labor_cost), 2) AS labor_cost
FROM vw_staff_data
GROUP BY role
ORDER BY labor_cost DESC;

-- 11. Profitability by day
SELECT
    business_date,
    net_sales,
    ingredient_cost,
    labor_cost,
    estimated_profit,
    estimated_margin_pct
FROM vw_profitability
ORDER BY business_date;

