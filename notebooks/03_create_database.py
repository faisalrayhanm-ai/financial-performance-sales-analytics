import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text


# ============================================================
# 1. PATHS
# ============================================================

DATA_PATH = Path("data/sales_transactions.csv")

DATABASE_PATH = Path("data/sales_performance.db")


# ============================================================
# 2. LOAD CSV DATA
# ============================================================

print("=" * 70)
print("CREATING SALES PERFORMANCE SQL DATABASE")
print("=" * 70)

print("\nLoading sales transaction data...")

df = pd.read_csv(DATA_PATH)

df["order_date"] = pd.to_datetime(
    df["order_date"]
)

print(
    f"Rows loaded: {len(df):,}"
)

print(
    f"Columns loaded: {len(df.columns)}"
)


# ============================================================
# 3. CREATE SQLITE DATABASE
# ============================================================

print("\nCreating SQLite database...")

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# ============================================================
# 4. WRITE DATA TO SQL TABLE
# ============================================================

print("\nWriting data to SQL table...")

df.to_sql(
    "sales_transactions",
    con=engine,
    if_exists="replace",
    index=False
)

print(
    "Table created: sales_transactions"
)


# ============================================================
# 5. VERIFY TABLE
# ============================================================

print("\nVerifying database...")

with engine.connect() as connection:

    row_count = connection.execute(
        text(
            "SELECT COUNT(*) FROM sales_transactions"
        )
    ).scalar()

    column_count = len(df.columns)

print(
    f"Rows in SQL table: {row_count:,}"
)

print(
    f"Columns in SQL table: {column_count}"
)


# ============================================================
# 6. DISPLAY TABLE STRUCTURE
# ============================================================

print("\n" + "=" * 70)
print("TABLE STRUCTURE")
print("=" * 70)

with engine.connect() as connection:

    result = connection.execute(
        text(
            "PRAGMA table_info(sales_transactions)"
        )
    )

    columns = result.fetchall()

for column in columns:

    print(
        f"{column[1]:25} {column[2]}"
    )


# ============================================================
# 7. RUN BASIC SQL KPI QUERY
# ============================================================

print("\n" + "=" * 70)
print("BASIC SQL KPI CHECK")
print("=" * 70)

kpi_query = text(
    """
    SELECT
        COUNT(*) AS total_orders,
        COUNT(DISTINCT customer_id) AS unique_customers,
        SUM(quantity) AS total_quantity,
        SUM(sales) AS total_sales,
        SUM(cost) AS total_cost,
        SUM(profit) AS total_profit,
        AVG(sales) AS average_order_value,
        AVG(discount) AS average_discount,
        SUM(
            CASE
                WHEN profit < 0 THEN 1
                ELSE 0
            END
        ) AS loss_making_orders
    FROM sales_transactions
    """
)

with engine.connect() as connection:

    result = connection.execute(
        kpi_query
    ).fetchone()


print(
    f"\nTotal Orders: {result.total_orders:,}"
)

print(
    f"Unique Customers: {result.unique_customers:,}"
)

print(
    f"Total Quantity: {result.total_quantity:,}"
)

print(
    f"Total Sales: €{result.total_sales:,.2f}"
)

print(
    f"Total Cost: €{result.total_cost:,.2f}"
)

print(
    f"Total Profit: €{result.total_profit:,.2f}"
)

print(
    f"Average Order Value: €{result.average_order_value:,.2f}"
)

print(
    f"Average Discount: {result.average_discount:.2%}"
)

print(
    f"Loss-Making Orders: {result.loss_making_orders:,}"
)


# ============================================================
# 8. PROFIT MARGIN CALCULATION
# ============================================================

profit_margin = (
    result.total_profit /
    result.total_sales
)

print(
    f"Overall Profit Margin: {profit_margin:.2%}"
)


# ============================================================
# 9. TEST GROUP BY QUERY
# ============================================================

print("\n" + "=" * 70)
print("CATEGORY SQL TEST")
print("=" * 70)

category_query = text(
    """
    SELECT
        product_category,
        COUNT(*) AS orders,
        SUM(sales) AS sales,
        SUM(cost) AS cost,
        SUM(profit) AS profit,
        ROUND(
            SUM(profit) / SUM(sales) * 100,
            2
        ) AS profit_margin_percent
    FROM sales_transactions
    GROUP BY product_category
    ORDER BY profit DESC
    """
)

with engine.connect() as connection:

    category_results = connection.execute(
        category_query
    )

    for row in category_results:

        print(
            f"{row.product_category:20} "
            f"Orders: {row.orders:6,} | "
            f"Sales: €{row.sales:,.2f} | "
            f"Profit: €{row.profit:,.2f} | "
            f"Margin: {row.profit_margin_percent:.2f}%"
        )


# ============================================================
# 10. DATABASE FILE CHECK
# ============================================================

print("\n" + "=" * 70)
print("DATABASE CREATED SUCCESSFULLY")
print("=" * 70)

print(
    f"\nDatabase location:"
)

print(
    DATABASE_PATH
)

print(
    "\nTable:"
)

print(
    "sales_transactions"
)

print(
    f"\nRows stored: {row_count:,}"
)

print(
    f"Columns stored: {column_count}"
)

print(
    "\nSQL database is ready for analysis."
)