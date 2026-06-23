from __future__ import annotations

from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
WAREHOUSE_DIR = ROOT / "data" / "warehouse"
DB_PATH = WAREHOUSE_DIR / "pizzeria.duckdb"
SCHEMA_SQL = ROOT / "sql" / "01_schema.sql"
VIEWS_SQL = ROOT / "sql" / "03_views.sql"


LOAD_ORDER = [
    "addresses",
    "customers",
    "item_categories",
    "item_sizes",
    "menu_items",
    "ingredients",
    "recipes",
    "vendors",
    "purchases",
    "staff",
    "staff_shifts",
    "orders",
    "order_items",
    "inventory_adjustments",
]


def require_raw_files() -> None:
    missing = [name for name in LOAD_ORDER if not (RAW_DIR / f"{name}.csv").exists()]
    if missing:
        missing_str = ", ".join(missing)
        raise SystemExit(f"Missing raw CSV files: {missing_str}. Run scripts/generate_data.py first.")


def execute_sql_file(con: duckdb.DuckDBPyConnection, path: Path) -> None:
    con.execute(path.read_text(encoding="utf-8"))


def load_table(con: duckdb.DuckDBPyConnection, table_name: str) -> int:
    csv_path = (RAW_DIR / f"{table_name}.csv").as_posix()
    con.execute(
        f"""
        COPY {table_name}
        FROM '{csv_path}'
        (HEADER, DELIMITER ',', QUOTE '"', ESCAPE '"');
        """
    )
    return con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]


def main() -> None:
    require_raw_files()
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    con = duckdb.connect(str(DB_PATH))
    try:
        execute_sql_file(con, SCHEMA_SQL)
        print(f"Created schema in {DB_PATH}")
        for table_name in LOAD_ORDER:
            count = load_table(con, table_name)
            print(f"Loaded {table_name}: {count} rows")
        execute_sql_file(con, VIEWS_SQL)
        print("Created analytical views")
        con.execute("CHECKPOINT")
    finally:
        con.close()


if __name__ == "__main__":
    main()

