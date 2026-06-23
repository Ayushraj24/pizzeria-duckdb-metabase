from __future__ import annotations

from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "warehouse" / "pizzeria.duckdb"


CHECKS = [
    (
        "orders_have_items",
        """
        SELECT COUNT(*)
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE oi.order_id IS NULL
        """,
        0,
    ),
    (
        "no_negative_prices",
        """
        SELECT COUNT(*)
        FROM order_items
        WHERE item_price < 0 OR quantity <= 0
        """,
        0,
    ),
    (
        "completed_orders_exist",
        """
        SELECT COUNT(*)
        FROM orders
        WHERE order_status = 'Completed'
        """,
        "positive",
    ),
    (
        "inventory_status_exists",
        """
        SELECT COUNT(*)
        FROM vw_inventory_status
        """,
        "positive",
    ),
    (
        "no_negative_inventory",
        """
        SELECT COUNT(*)
        FROM vw_inventory_status
        WHERE current_stock_qty < 0
        """,
        0,
    ),
    (
        "profitability_exists",
        """
        SELECT COUNT(*)
        FROM vw_profitability
        """,
        "positive",
    ),
    (
        "no_null_profit_dates",
        """
        SELECT COUNT(*)
        FROM vw_profitability
        WHERE business_date IS NULL
        """,
        0,
    ),
]


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit(f"DuckDB database not found: {DB_PATH}. Run scripts/build_warehouse.py first.")

    con = duckdb.connect(str(DB_PATH), read_only=True)
    failures = []
    try:
        print("Warehouse summary")
        for table_name in ["orders", "order_items", "purchases", "staff_shifts"]:
            count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            print(f"  {table_name}: {count}")

        print("\nData quality checks")
        for name, query, expected in CHECKS:
            value = con.execute(query).fetchone()[0]
            passed = value > 0 if expected == "positive" else value == expected
            status = "PASS" if passed else "FAIL"
            print(f"  {status} {name}: {value}")
            if not passed:
                failures.append(name)

        print("\nSample daily sales")
        rows = con.execute(
            """
            SELECT business_date, orders, items_sold, net_sales, avg_order_value
            FROM vw_daily_sales
            ORDER BY business_date
            LIMIT 5
            """
        ).fetchall()
        for row in rows:
            print(f"  {row}")

        print("\nSample low-stock alerts")
        rows = con.execute(
            """
            SELECT ingredient_name, current_stock_qty, reorder_level, stock_status
            FROM vw_low_stock_alerts
            ORDER BY stock_coverage_pct
            LIMIT 5
            """
        ).fetchall()
        for row in rows:
            print(f"  {row}")
    finally:
        con.close()

    if failures:
        raise SystemExit(f"Validation failed: {', '.join(failures)}")
    print("\nValidation passed")


if __name__ == "__main__":
    main()
