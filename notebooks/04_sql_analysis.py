import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text


# ============================================================
# 1. PATHS
# ============================================================

DATABASE_PATH = Path("data/sales_performance.db")
OUTPUT_PATH = Path("data/sql_analysis")

OUTPUT_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. DATABASE CONNECTION
# ============================================================

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


print("=" * 75)
print("FINANCIAL PERFORMANCE & SALES - SQL ANALYSIS")
print("=" * 75)


# ============================================================
# 3. HELPER FUNCTION
# ============================================================

def run_query(query, output_file=None):
    """
    Run SQL query and optionally save the result as CSV.
    """

    with engine.connect() as connection:

        df = pd.read_sql(
            text(query),
            connection
        )

    if output_file:
        df.to_csv(
            OUTPUT_PATH / output_file,
            index=False
        )

    return df


# ============================================================
# 4. OVERALL FINANCIAL KPIs
# ============================================================

print("\n" + "=" * 75)
print("1. OVERALL FINANCIAL KPIs")
print("=" * 75)

query = """
SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(cost), 2) AS total_cost,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(sales), 2) AS average_order_value,
    ROUND(AVG(discount) * 100, 2) AS average_discount_percent,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent,
    SUM(
        CASE
            WHEN profit < 0 THEN 1
            ELSE 0
        END
    ) AS loss_making_orders
FROM sales_transactions;
"""

df = run_query(
    query,
    "sql_kpi_summary.csv"
)

print(df.to_string(index=False))


# ============================================================
# 5. MONTHLY PERFORMANCE
# ============================================================

print("\n" + "=" * 75)
print("2. MONTHLY SALES & PROFIT PERFORMANCE")
print("=" * 75)

query = """
SELECT
    year_month,
    COUNT(*) AS orders,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(cost), 2) AS cost,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent,
    ROUND(AVG(sales), 2) AS average_order_value
FROM sales_transactions
GROUP BY year_month
ORDER BY year_month;
"""

df = run_query(
    query,
    "sql_monthly_performance.csv"
)

print(df.to_string(index=False))


# ============================================================
# 6. YEARLY PERFORMANCE
# ============================================================

print("\n" + "=" * 75)
print("3. YEARLY PERFORMANCE")
print("=" * 75)

query = """
WITH yearly AS (
    SELECT
        year,
        SUM(sales) AS sales,
        SUM(cost) AS cost,
        SUM(profit) AS profit,
        COUNT(*) AS orders
    FROM sales_transactions
    GROUP BY year
)

SELECT
    year,
    orders,
    ROUND(sales, 2) AS sales,
    ROUND(cost, 2) AS cost,
    ROUND(profit, 2) AS profit,
    ROUND(
        profit / sales * 100,
        2
    ) AS profit_margin_percent
FROM yearly
ORDER BY year;
"""

df = run_query(
    query,
    "sql_yearly_performance.csv"
)

print(df.to_string(index=False))


# ============================================================
# 7. REGIONAL PERFORMANCE
# ============================================================

print("\n" + "=" * 75)
print("4. REGIONAL PERFORMANCE")
print("=" * 75)

query = """
SELECT
    region,
    COUNT(*) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(cost), 2) AS cost,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent,
    ROUND(AVG(sales), 2) AS average_order_value
FROM sales_transactions
GROUP BY region
ORDER BY profit DESC;
"""

df = run_query(
    query,
    "sql_region_performance.csv"
)

print(df.to_string(index=False))


# ============================================================
# 8. PRODUCT CATEGORY PERFORMANCE
# ============================================================

print("\n" + "=" * 75)
print("5. PRODUCT CATEGORY PERFORMANCE")
print("=" * 75)

query = """
SELECT
    product_category,
    COUNT(*) AS orders,
    SUM(quantity) AS quantity,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(cost), 2) AS cost,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent,
    ROUND(AVG(sales), 2) AS average_order_value
FROM sales_transactions
GROUP BY product_category
ORDER BY profit DESC;
"""

df = run_query(
    query,
    "sql_category_performance.csv"
)

print(df.to_string(index=False))


# ============================================================
# 9. TOP 10 PRODUCTS BY PROFIT
# ============================================================

print("\n" + "=" * 75)
print("6. TOP 10 PRODUCTS BY PROFIT")
print("=" * 75)

query = """
SELECT
    product,
    COUNT(*) AS orders,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent
FROM sales_transactions
GROUP BY product
ORDER BY profit DESC
LIMIT 10;
"""

df = run_query(
    query,
    "sql_top_products_by_profit.csv"
)

print(df.to_string(index=False))


# ============================================================
# 10. SALES CHANNEL PERFORMANCE
# ============================================================

print("\n" + "=" * 75)
print("7. SALES CHANNEL PERFORMANCE")
print("=" * 75)

query = """
SELECT
    sales_channel,
    COUNT(*) AS orders,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(cost), 2) AS cost,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent
FROM sales_transactions
GROUP BY sales_channel
ORDER BY profit DESC;
"""

df = run_query(
    query,
    "sql_channel_performance.csv"
)

print(df.to_string(index=False))


# ============================================================
# 11. NEW VS REPEAT CUSTOMERS
# ============================================================

print("\n" + "=" * 75)
print("8. NEW VS REPEAT CUSTOMER PERFORMANCE")
print("=" * 75)

query = """
SELECT
    customer_type,
    COUNT(*) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent,
    ROUND(AVG(sales), 2) AS average_order_value
FROM sales_transactions
GROUP BY customer_type
ORDER BY sales DESC;
"""

df = run_query(
    query,
    "sql_customer_type.csv"
)

print(df.to_string(index=False))


# ============================================================
# 12. CUSTOMER SEGMENT PERFORMANCE
# ============================================================

print("\n" + "=" * 75)
print("9. CUSTOMER SEGMENT PERFORMANCE")
print("=" * 75)

query = """
SELECT
    customer_segment,
    COUNT(*) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent,
    ROUND(AVG(sales), 2) AS average_order_value
FROM sales_transactions
GROUP BY customer_segment
ORDER BY profit DESC;
"""

df = run_query(
    query,
    "sql_customer_segments.csv"
)

print(df.to_string(index=False))


# ============================================================
# 13. DISCOUNT VS PROFITABILITY
# ============================================================

print("\n" + "=" * 75)
print("10. DISCOUNT VS PROFITABILITY")
print("=" * 75)

query = """
SELECT
    discount,
    COUNT(*) AS orders,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent
FROM sales_transactions
GROUP BY discount
ORDER BY discount;
"""

df = run_query(
    query,
    "sql_discount_analysis.csv"
)

print(df.to_string(index=False))


# ============================================================
# 14. LOSS-MAKING ORDERS
# ============================================================

print("\n" + "=" * 75)
print("11. LOSS-MAKING ORDERS")
print("=" * 75)

query = """
SELECT
    order_id,
    order_date,
    region,
    sales_channel,
    product_category,
    product,
    discount,
    ROUND(sales, 2) AS sales,
    ROUND(cost, 2) AS cost,
    ROUND(profit, 2) AS profit
FROM sales_transactions
WHERE profit < 0
ORDER BY profit ASC
LIMIT 20;
"""

df = run_query(
    query,
    "sql_loss_making_orders.csv"
)

print(df.to_string(index=False))


# ============================================================
# 15. REGION + CHANNEL ANALYSIS
# ============================================================

print("\n" + "=" * 75)
print("12. REGION + CHANNEL PERFORMANCE")
print("=" * 75)

query = """
SELECT
    region,
    sales_channel,
    COUNT(*) AS orders,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent
FROM sales_transactions
GROUP BY
    region,
    sales_channel
ORDER BY
    region,
    profit DESC;
"""

df = run_query(
    query,
    "sql_region_channel.csv"
)

print(df.to_string(index=False))


# ============================================================
# 16. CATEGORY + DISCOUNT ANALYSIS
# ============================================================

print("\n" + "=" * 75)
print("13. CATEGORY + DISCOUNT PROFITABILITY")
print("=" * 75)

query = """
SELECT
    product_category,
    discount,
    COUNT(*) AS orders,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent
FROM sales_transactions
GROUP BY
    product_category,
    discount
ORDER BY
    product_category,
    discount;
"""

df = run_query(
    query,
    "sql_category_discount.csv"
)

print(df.to_string(index=False))


# ============================================================
# 17. HIGH SALES + LOW MARGIN PRODUCTS
# ============================================================

print("\n" + "=" * 75)
print("14. HIGH SALES + LOW MARGIN PRODUCTS")
print("=" * 75)

query = """
WITH product_metrics AS (

    SELECT
        product,
        SUM(sales) AS sales,
        SUM(profit) AS profit,
        SUM(profit) / SUM(sales) AS margin

    FROM sales_transactions

    GROUP BY product
),

thresholds AS (

    SELECT
        AVG(sales) AS average_sales,
        AVG(margin) AS average_margin

    FROM product_metrics
)

SELECT
    p.product,
    ROUND(p.sales, 2) AS sales,
    ROUND(p.profit, 2) AS profit,
    ROUND(p.margin * 100, 2) AS profit_margin_percent

FROM product_metrics p

CROSS JOIN thresholds t

WHERE
    p.sales > t.average_sales
    AND p.margin < t.average_margin

ORDER BY
    p.sales DESC;
"""

df = run_query(
    query,
    "sql_high_sales_low_margin.csv"
)

print(df.to_string(index=False))


# ============================================================
# 18. EXECUTIVE BUSINESS SUMMARY
# ============================================================

print("\n" + "=" * 75)
print("15. EXECUTIVE SQL SUMMARY")
print("=" * 75)

query = """
SELECT
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        SUM(profit) / SUM(sales) * 100,
        2
    ) AS profit_margin_percent,

    (
        SELECT region
        FROM sales_transactions
        GROUP BY region
        ORDER BY SUM(profit) DESC
        LIMIT 1
    ) AS most_profitable_region,

    (
        SELECT product_category
        FROM sales_transactions
        GROUP BY product_category
        ORDER BY SUM(profit) / SUM(sales) DESC
        LIMIT 1
    ) AS highest_margin_category,

    (
        SELECT product_category
        FROM sales_transactions
        GROUP BY product_category
        ORDER BY SUM(profit) / SUM(sales) ASC
        LIMIT 1
    ) AS lowest_margin_category

FROM sales_transactions;
"""

df = run_query(
    query,
    "sql_executive_summary.csv"
)

print(df.to_string(index=False))


# ============================================================
# 19. COMPLETION
# ============================================================

print("\n" + "=" * 75)
print("SQL ANALYSIS COMPLETE")
print("=" * 75)

print("\nSQL analysis files saved to:")

print(
    OUTPUT_PATH
)

print("\nThe project now contains:")

print("✓ Python data generation")
print("✓ Python financial analysis")
print("✓ SQLite database")
print("✓ SQL business analysis")
print("✓ SQL aggregation")
print("✓ GROUP BY analysis")
print("✓ CTE analysis")
print("✓ CASE analysis")
print("✓ Customer analysis")
print("✓ Product analysis")
print("✓ Regional analysis")
print("✓ Discount profitability analysis")