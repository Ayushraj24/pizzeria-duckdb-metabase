# Data Dictionary

## Core Tables

| Table | Grain | Purpose |
|---|---|---|
| `addresses` | One row per address | Customer location and city analysis |
| `customers` | One row per customer | Customer information |
| `orders` | One row per order | Order header, payment, order type, staff |
| `order_items` | One row per item in an order | Items sold and line-level sales |
| `menu_items` | One row per sellable item | Menu catalog and item price |
| `item_categories` | One row per category | Pizza, sides, drinks, dessert |
| `item_sizes` | One row per size | Regular, large, bottle, single |
| `ingredients` | One row per ingredient | Stock tracking and reorder level |
| `recipes` | One row per item and ingredient | Ingredient quantity used per menu item |
| `vendors` | One row per supplier | Supplier dimension |
| `purchases` | One row per ingredient purchase | Incoming stock and ingredient cost |
| `staff` | One row per staff member | Staff role and hourly rate |
| `staff_shifts` | One row per staff shift | Labor hours and cost |
| `inventory_adjustments` | One row per adjustment | Waste, spoilage, and corrections |

## Analytical Views

| View | Purpose |
|---|---|
| `vw_sales_data` | Detailed order-line sales view |
| `vw_daily_sales` | Daily order count, items sold, sales, average order value |
| `vw_hourly_orders` | Hourly demand pattern |
| `vw_ingredient_usage` | Ingredient consumption derived from recipes and sold items |
| `vw_inventory_in` | Purchased quantity and purchase cost by ingredient |
| `vw_inventory_out` | Used and adjusted quantity by ingredient |
| `vw_inventory_status` | Current stock, coverage percent, reorder status |
| `vw_low_stock_alerts` | Ingredients requiring attention |
| `vw_purchases_data` | Purchase-level vendor and ingredient detail |
| `vw_staff_data` | Staff hours and labor cost |
| `vw_profitability` | Daily net sales, ingredient cost, labor cost, estimated profit |

