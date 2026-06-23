# Metabase Dashboard Specification

Create one dashboard named `Pizzeria Operations`.

## Tab 1: Operations Overview

| Card | Source | Visualization |
|---|---|---|
| Net sales | `vw_daily_sales` | Number |
| Orders | `vw_daily_sales` | Number |
| Average order value | `vw_daily_sales` | Number |
| Estimated profit | `vw_profitability` | Number |
| Net sales by day | `vw_daily_sales` | Line chart |
| Orders by hour | `vw_hourly_orders` | Bar chart |

## Tab 2: Sales

| Card | Source | Visualization |
|---|---|---|
| Sales by category | `vw_sales_data` | Bar chart |
| Sales by item | `vw_sales_data` | Bar chart |
| Orders by city | `vw_sales_data` | Bar chart or map |
| Pickup vs delivery | `vw_sales_data` | Pie or bar chart |
| Payment method split | `vw_sales_data` | Bar chart |

Useful SQL:

```sql
SELECT
    category_name,
    ROUND(SUM(gross_line_sales), 2) AS sales
FROM vw_sales_data
WHERE order_status = 'Completed'
GROUP BY category_name
ORDER BY sales DESC;
```

## Tab 3: Inventory

| Card | Source | Visualization |
|---|---|---|
| Current stock by ingredient | `vw_inventory_status` | Table |
| Low stock alerts | `vw_low_stock_alerts` | Table |
| Purchased vs used quantity | `vw_inventory_status` | Combo chart |
| Ingredient usage over time | `vw_ingredient_usage` | Line chart |

Use conditional formatting:

- `Reorder now`: red
- `Watch`: yellow
- `Healthy`: green

## Tab 4: Purchasing

| Card | Source | Visualization |
|---|---|---|
| Purchase cost by vendor | `vw_purchases_data` | Bar chart |
| Ingredient unit cost trend | `vw_purchases_data` | Line chart |
| Purchases by ingredient | `vw_purchases_data` | Table |

## Tab 5: Staff

| Card | Source | Visualization |
|---|---|---|
| Labor cost by day | `vw_staff_data` | Line chart |
| Hours by staff | `vw_staff_data` | Bar chart |
| Labor cost by role | `vw_staff_data` | Bar chart |
| Shift log | `vw_staff_data` | Table |

## Tab 6: Profitability

| Card | Source | Visualization |
|---|---|---|
| Net sales vs estimated profit | `vw_profitability` | Combo chart |
| Ingredient cost by day | `vw_profitability` | Line chart |
| Labor cost by day | `vw_profitability` | Line chart |
| Estimated margin percent | `vw_profitability` | Line chart |

