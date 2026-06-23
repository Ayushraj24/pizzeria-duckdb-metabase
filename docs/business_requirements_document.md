# Business Requirements Document

## Project Name

Pizzeria Operations Analytics Dashboard

## Business Objective

Build a local analytics solution that helps a small pizzeria understand sales performance, ordering behavior, inventory status, staff labor cost, ingredient cost, and estimated profitability using a free technical stack.

The dashboard should help answer:

- Is the pizzeria profitable?
- Which menu items and categories drive revenue?
- When do customers place the most orders?
- Which ingredients need restocking?
- How much are labor and ingredient costs affecting margin?
- Which payment and fulfillment channels are most used?

## Background

The pizzeria has operational data across orders, order items, menu items, recipes, ingredients, vendors, purchases, inventory adjustments, staff, and staff shifts. Without a central analytics model, it is difficult to connect sales activity with inventory usage and profitability.

This project creates a DuckDB analytical warehouse and a Metabase dashboard to give decision-makers a single view of business performance.

## Stakeholders

| Stakeholder | Role | Needs |
|---|---|---|
| Owner / Manager | Business decision-maker | Sales, margin, demand, and inventory visibility |
| Operations Manager | Daily operations | Low-stock alerts, usage trends, purchasing needs |
| Finance Analyst | Profitability analysis | Revenue, ingredient cost, labor cost, estimated margin |
| Store Staff Lead | Staffing decisions | Shift hours, labor cost, busy periods |
| Data Analyst / Engineer | Solution builder | Reliable schema, SQL views, reproducible pipeline |

## Scope

### In Scope

- Generate synthetic pizzeria operations data.
- Build normalized DuckDB tables.
- Create analytical SQL views for dashboarding.
- Track sales, orders, inventory, purchasing, staff, and profitability.
- Create a Metabase dashboard with executive, sales, inventory, and profitability views.
- Document ERD, data dictionary, pipeline, dashboard design, and business requirements.

### Out of Scope

- Real payment gateway integration.
- Live point-of-sale ingestion.
- User authentication beyond Metabase local setup.
- Cloud hosting.
- Real-time streaming updates.
- Production-grade accounting or tax reporting.

## Business KPIs

| KPI | Definition | Current Dashboard Value |
|---|---|---:|
| Total net sales | Sales after discounts plus delivery fees | `134,707.43` |
| Completed orders | Orders with completed status | `4,321` |
| Estimated profit | Net sales minus ingredient and labor cost | `-53,994.99` |
| Profit margin % | Estimated profit divided by net sales | `-40.08%` |
| Average order value | Net sales divided by completed orders | Derived from `vw_daily_sales` |
| Low-stock ingredients | Ingredients in `Watch` or `Reorder now` status | Dough, Mozzarella |
| Top menu items | Items ranked by gross sales | Meat Lovers, Pepperoni, Margherita |

## Dashboard Requirements

| Requirement ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| BRD-001 | Show executive KPIs | High | Dashboard displays net sales, orders, estimated profit, and margin |
| BRD-002 | Track daily sales trend | High | User can view net sales, orders, and average order value by date |
| BRD-003 | Analyze profitability | High | User can compare net sales, ingredient cost, labor cost, and profit by day |
| BRD-004 | Monitor inventory status | High | User can see current stock, used quantity, purchased quantity, reorder level, and stock status |
| BRD-005 | Identify low-stock ingredients | High | Dashboard highlights ingredients in `Watch` or `Reorder now` status |
| BRD-006 | Analyze product performance | Medium | Dashboard ranks menu items and categories by sales |
| BRD-007 | Understand customer ordering behavior | Medium | Dashboard shows orders by hour, payment split, and pickup vs delivery |
| BRD-008 | Analyze labor cost | Medium | Dashboard shows hours worked and labor cost by role |
| BRD-009 | Support reproducibility | High | Pipeline can rebuild the database using `python scripts/run_pipeline.py` |

## Functional Requirements

1. The data generator must create repeatable synthetic data using a fixed random seed.
2. The warehouse build must recreate the DuckDB database from raw CSV files.
3. The schema must enforce primary-key and foreign-key relationships where supported.
4. SQL views must provide dashboard-ready metrics.
5. The validation script must check for missing order items, invalid prices, missing profitability dates, and negative inventory.
6. Metabase must connect to the DuckDB database file through Docker.
7. Dashboard queries must be documented for easy recreation.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Cost | Must run locally with free/open-source tooling |
| Portability | Must run on a local laptop with Python and Docker |
| Maintainability | SQL, Python, and docs must be organized by purpose |
| Reproducibility | Pipeline must be executable from a clean checkout |
| Performance | Dashboard queries should be based on prebuilt analytical views |
| Usability | Dashboard should separate executive KPIs, sales behavior, inventory, and profitability |

## Data Requirements

| Data Domain | Tables |
|---|---|
| Customers | `customers`, `addresses` |
| Sales | `orders`, `order_items`, `menu_items`, `item_categories`, `item_sizes` |
| Inventory | `ingredients`, `recipes`, `inventory_adjustments` |
| Purchasing | `vendors`, `purchases` |
| Staff | `staff`, `staff_shifts` |

## Analytical Views

| View | Business Purpose |
|---|---|
| `vw_daily_sales` | Daily orders, net sales, average order value |
| `vw_hourly_orders` | Demand by hour |
| `vw_sales_data` | Detailed line-level sales analysis |
| `vw_inventory_status` | Current stock and reorder status |
| `vw_low_stock_alerts` | Ingredients needing attention |
| `vw_purchases_data` | Vendor and ingredient purchasing |
| `vw_staff_data` | Staff hours and labor cost |
| `vw_profitability` | Net sales, costs, estimated profit, and margin |

## Analysis Summary

The dashboard shows strong sales volume but poor estimated profitability. Total net sales are `134,707.43`, while estimated profit is `-53,994.99`. This indicates the generated business is operationally active but cost-heavy.

The main business issue is cost control. Labor cost and ingredient cost are consuming more than revenue can support. The pizzeria should analyze staffing schedules, vendor pricing, menu pricing, and recipe cost per item.

Inventory analysis shows Dough and Mozzarella in `Watch` status. These are core pizza ingredients, so low stock could disrupt the highest-performing category. Purchasing cadence should prioritize these ingredients.

Sales analysis shows Pizza dominates the revenue mix, and Meat Lovers, Pepperoni, and Margherita pizzas are the highest-performing items. This supports business actions such as menu optimization, bundle offers, price testing, and ingredient purchase planning around top sellers.

## Risks and Assumptions

| Risk / Assumption | Impact | Mitigation |
|---|---|---|
| Data is synthetic | Results are not real business outcomes | Clearly document that data is generated for portfolio/demo use |
| Profit is estimated | Does not include rent, utilities, tax, delivery partner fees, or waste beyond adjustments | Label all profit metrics as estimated |
| DuckDB is local | Not designed for many concurrent writers | Use DuckDB as an analytical warehouse, not as a transactional app database |
| Metabase driver is community-developed | Driver behavior can change | Pin and document setup instructions |

## Success Criteria

- A user can rebuild the warehouse locally.
- A user can connect Metabase to the DuckDB file.
- Dashboard screenshots are included in the README.
- ERD and data dictionary explain the data model.
- BRD explains the business purpose, KPIs, requirements, and findings.
- The project is suitable as a portfolio artifact for data analytics/data engineering.

