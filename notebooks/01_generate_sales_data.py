import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# 1. SETTINGS
# ============================================================

np.random.seed(42)

N = 75000

# ============================================================
# 2. MASTER DATA
# ============================================================

regions = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

channels = [
    "Online",
    "Retail Store",
    "Wholesale"
]

categories = [
    "Electronics",
    "Home & Furniture",
    "Clothing",
    "Office Supplies",
    "Sports & Outdoors"
]

products = {
    "Electronics": [
        "Laptop",
        "Smartphone",
        "Tablet",
        "Monitor",
        "Headphones"
    ],

    "Home & Furniture": [
        "Office Chair",
        "Desk",
        "Sofa",
        "Dining Table",
        "Bookshelf"
    ],

    "Clothing": [
        "Jacket",
        "Shoes",
        "T-Shirt",
        "Jeans",
        "Sportswear"
    ],

    "Office Supplies": [
        "Printer",
        "Notebook",
        "Paper Pack",
        "Pen Set",
        "Desk Organizer"
    ],

    "Sports & Outdoors": [
        "Running Shoes",
        "Bicycle",
        "Yoga Mat",
        "Dumbbells",
        "Fitness Tracker"
    ]
}

customer_segments = [
    "Consumer",
    "Small Business",
    "Corporate"
]

payment_methods = [
    "Credit Card",
    "Debit Card",
    "Bank Transfer",
    "PayPal"
]

# ============================================================
# 3. DATE AND CUSTOMER GENERATION
# ============================================================

dates = pd.date_range(
    start="2023-01-01",
    end="2025-12-31",
    freq="D"
)

order_dates = np.random.choice(
    dates,
    size=N
)

customer_ids = [
    f"C{num:05d}"
    for num in np.random.randint(
        1,
        15001,
        size=N
    )
]

order_ids = [
    f"O{num:06d}"
    for num in range(1, N + 1)
]

# ============================================================
# 4. DIMENSION VARIABLES
# ============================================================

region = np.random.choice(
    regions,
    size=N,
    p=[0.20, 0.18, 0.22, 0.20, 0.20]
)

channel = np.random.choice(
    channels,
    size=N,
    p=[0.50, 0.35, 0.15]
)

category = np.random.choice(
    categories,
    size=N,
    p=[0.24, 0.21, 0.22, 0.17, 0.16]
)

customer_segment = np.random.choice(
    customer_segments,
    size=N,
    p=[0.60, 0.25, 0.15]
)

payment_method = np.random.choice(
    payment_methods,
    size=N,
    p=[0.40, 0.25, 0.20, 0.15]
)

# ============================================================
# 5. PRODUCT GENERATION
# ============================================================

product = []

for cat in category:

    product.append(
        np.random.choice(
            products[cat]
        )
    )

# ============================================================
# 6. QUANTITY
# ============================================================

quantity = np.random.choice(
    [1, 2, 3, 4, 5, 6, 8, 10],
    size=N,
    p=[
        0.30,
        0.25,
        0.17,
        0.10,
        0.07,
        0.05,
        0.04,
        0.02
    ]
)

# ============================================================
# 7. PRODUCT PRICE RANGES
# ============================================================

price_ranges = {

    "Electronics": (
        80,
        1800
    ),

    "Home & Furniture": (
        40,
        1200
    ),

    "Clothing": (
        15,
        300
    ),

    "Office Supplies": (
        5,
        500
    ),

    "Sports & Outdoors": (
        20,
        900
    )
}

unit_price = np.array([

    np.random.uniform(
        *price_ranges[cat]
    )

    for cat in category

])

# ============================================================
# 8. DISCOUNTS
# ============================================================

discount = np.random.choice(

    [
        0.00,
        0.05,
        0.10,
        0.15,
        0.20,
        0.25
    ],

    size=N,

    p=[
        0.30,
        0.25,
        0.20,
        0.12,
        0.08,
        0.05
    ]
)

# ============================================================
# 9. SALES CALCULATION
# ============================================================

gross_sales = (
    unit_price *
    quantity
)

discount_amount = (
    gross_sales *
    discount
)

sales = (
    gross_sales -
    discount_amount
)

# ============================================================
# 10. SEASONAL SALES EFFECT
# ============================================================

# Certain months have stronger sales activity.
# This creates a more realistic monthly trend.

seasonal_factor_map = {

    1: 0.92,
    2: 0.90,
    3: 0.96,
    4: 1.00,
    5: 1.02,
    6: 1.00,
    7: 0.97,
    8: 1.01,
    9: 1.05,
    10: 1.08,
    11: 1.18,
    12: 1.30
}

order_month = pd.DatetimeIndex(
    order_dates
).month

seasonal_factor = np.array([

    seasonal_factor_map[month]

    for month in order_month

])

sales = sales * seasonal_factor

gross_sales = gross_sales * seasonal_factor

discount_amount = (
    gross_sales *
    discount
)

# Recalculate sales after seasonal adjustment
sales = (
    gross_sales -
    discount_amount
)

# ============================================================
# 11. PRODUCT COST
# ============================================================

# Different product categories have different typical margins.

category_cost_rate = {

    "Electronics": 0.72,

    "Home & Furniture": 0.63,

    "Clothing": 0.52,

    "Office Supplies": 0.58,

    "Sports & Outdoors": 0.60

}

base_cost_rate = np.array([

    category_cost_rate[cat]

    for cat in category

])

# Add realistic variation around the category average.

cost_rate = np.clip(

    base_cost_rate
    + np.random.normal(
        0,
        0.04,
        N
    ),

    0.40,
    0.80
)

# Product cost is based on original gross sales.
# This means discounts can reduce profit margins.

product_cost = (
    gross_sales *
    cost_rate
)

# ============================================================
# 12. CHANNEL OPERATING COST
# ============================================================

channel_operating_rate = {

    "Online": 0.025,

    "Retail Store": 0.055,

    "Wholesale": 0.040

}

channel_rate = np.array([

    channel_operating_rate[ch]

    for ch in channel

])

# ============================================================
# 13. REGIONAL OPERATING COST
# ============================================================

region_operating_rate = {

    "North": 0.015,

    "South": 0.025,

    "East": 0.020,

    "West": 0.030,

    "Central": 0.018

}

region_rate = np.array([

    region_operating_rate[r]

    for r in region

])

# ============================================================
# 14. OPERATING COST
# ============================================================

operating_cost = (

    sales *
    (
        channel_rate
        + region_rate
    )

)

# ============================================================
# 15. TOTAL COST
# ============================================================

cost = (

    product_cost
    + operating_cost

)

# ============================================================
# 16. PROFIT
# ============================================================

profit = (

    sales -
    cost

)

# ============================================================
# 17. PROFIT MARGIN
# ============================================================

profit_margin = np.where(

    sales != 0,

    profit / sales,

    0

)

# ============================================================
# 18. CREATE DATAFRAME
# ============================================================

df = pd.DataFrame({

    "order_id": order_ids,

    "order_date": order_dates,

    "customer_id": customer_ids,

    "region": region,

    "sales_channel": channel,

    "customer_segment": customer_segment,

    "product_category": category,

    "product": product,

    "quantity": quantity,

    "unit_price": unit_price,

    "discount": discount,

    "gross_sales": gross_sales,

    "discount_amount": discount_amount,

    "sales": sales,

    "product_cost": product_cost,

    "operating_cost": operating_cost,

    "cost": cost,

    "profit": profit,

    "profit_margin": profit_margin,

    "payment_method": payment_method

})

# ============================================================
# 19. CUSTOMER NEW / REPEAT ANALYSIS
# ============================================================

# Sort by customer and date so we can identify
# each customer's first order.

df = df.sort_values(

    [
        "customer_id",
        "order_date",
        "order_id"
    ]

)

# Number each customer's orders.

df["customer_order_number"] = (

    df.groupby(
        "customer_id"
    ).cumcount() + 1

)

# First order = New Customer
# Later orders = Repeat Customer

df["customer_type"] = np.where(

    df["customer_order_number"] == 1,

    "New Customer",

    "Repeat Customer"

)

# Restore order ID sequence.

df = df.sort_values(
    "order_id"
)

# ============================================================
# 20. YEAR / MONTH INFORMATION
# ============================================================

df["year"] = (

    df["order_date"]
    .dt.year

)

df["month"] = (

    df["order_date"]
    .dt.month

)

df["year_month"] = (

    df["order_date"]
    .dt.to_period("M")
    .astype(str)

)

# ============================================================
# 21. ROUND NUMERIC VALUES
# ============================================================

numeric_columns = [

    "unit_price",

    "gross_sales",

    "discount_amount",

    "sales",

    "product_cost",

    "operating_cost",

    "cost",

    "profit",

    "profit_margin"

]

df[numeric_columns] = (

    df[numeric_columns]
    .round(2)

)

# ============================================================
# 22. SAVE DATASET
# ============================================================

output_path = Path(
    "data/sales_transactions.csv"
)

df.to_csv(

    output_path,

    index=False

)

# ============================================================
# 23. DATASET SUMMARY
# ============================================================

print(
    "\n=============================================="
)

print(
    "FINANCIAL PERFORMANCE & SALES DATASET"
)

print(
    "=============================================="
)

print(
    "\nDataset created successfully!"
)

print(
    f"Rows: {len(df):,}"
)

print(
    f"Columns: {len(df.columns)}"
)

print(
    "\nDataset shape:"
)

print(
    df.shape
)

# ============================================================
# 24. FIRST FIVE ROWS
# ============================================================

print(
    "\nFirst 5 rows:"
)

print(
    df.head()
)

# ============================================================
# 25. DATA QUALITY
# ============================================================

print(
    "\n=============================================="
)

print(
    "DATA QUALITY"
)

print(
    "=============================================="
)

print(
    "\nMissing values:"
)

print(
    df.isnull().sum()
)

print(
    "\nDuplicate rows:"
)

print(
    df.duplicated().sum()
)

# ============================================================
# 26. FINANCIAL KPIs
# ============================================================

total_sales = df["sales"].sum()

total_cost = df["cost"].sum()

total_profit = df["profit"].sum()

average_order_value = df["sales"].mean()

overall_margin = (

    total_profit /
    total_sales

)

print(
    "\n=============================================="
)

print(
    "FINANCIAL KPIs"
)

print(
    "=============================================="
)

print(
    f"\nTotal Orders: {len(df):,}"
)

print(
    f"Total Sales: €{total_sales:,.2f}"
)

print(
    f"Total Cost: €{total_cost:,.2f}"
)

print(
    f"Total Profit: €{total_profit:,.2f}"
)

print(
    f"Average Order Value: €{average_order_value:,.2f}"
)

print(
    f"Overall Profit Margin: {overall_margin:.2%}"
)

# ============================================================
# 27. CUSTOMER ANALYSIS
# ============================================================

print(
    "\n=============================================="
)

print(
    "CUSTOMER TYPE"
)

print(
    "=============================================="
)

customer_type_summary = (

    df.groupby(
        "customer_type"
    )

    .agg(

        orders=(
            "order_id",
            "count"
        ),

        sales=(
            "sales",
            "sum"
        ),

        profit=(
            "profit",
            "sum"
        )

    )

    .sort_values(
        "sales",
        ascending=False
    )

)

customer_type_summary["profit_margin"] = (

    customer_type_summary["profit"]
    /
    customer_type_summary["sales"]

)

print(
    customer_type_summary
)

# ============================================================
# 28. REGION ANALYSIS
# ============================================================

print(
    "\n=============================================="
)

print(
    "REGION PERFORMANCE"
)

print(
    "=============================================="
)

region_summary = (

    df.groupby(
        "region"
    )

    .agg(

        orders=(
            "order_id",
            "count"
        ),

        sales=(
            "sales",
            "sum"
        ),

        cost=(
            "cost",
            "sum"
        ),

        profit=(
            "profit",
            "sum"
        )

    )

)

region_summary["profit_margin"] = (

    region_summary["profit"]
    /
    region_summary["sales"]

)

region_summary = region_summary.sort_values(

    "sales",
    ascending=False

)

print(
    region_summary
)

# ============================================================
# 29. CATEGORY ANALYSIS
# ============================================================

print(
    "\n=============================================="
)

print(
    "PRODUCT CATEGORY PERFORMANCE"
)

print(
    "=============================================="
)

category_summary = (

    df.groupby(
        "product_category"
    )

    .agg(

        orders=(
            "order_id",
            "count"
        ),

        sales=(
            "sales",
            "sum"
        ),

        cost=(
            "cost",
            "sum"
        ),

        profit=(
            "profit",
            "sum"
        )

    )

)

category_summary["profit_margin"] = (

    category_summary["profit"]
    /
    category_summary["sales"]

)

category_summary = category_summary.sort_values(

    "profit",
    ascending=False

)

print(
    category_summary
)

# ============================================================
# 30. CHANNEL ANALYSIS
# ============================================================

print(
    "\n=============================================="
)

print(
    "SALES CHANNEL PERFORMANCE"
)

print(
    "=============================================="
)

channel_summary = (

    df.groupby(
        "sales_channel"
    )

    .agg(

        orders=(
            "order_id",
            "count"
        ),

        sales=(
            "sales",
            "sum"
        ),

        cost=(
            "cost",
            "sum"
        ),

        profit=(
            "profit",
            "sum"
        )

    )

)

channel_summary["profit_margin"] = (

    channel_summary["profit"]
    /
    channel_summary["sales"]

)

channel_summary = channel_summary.sort_values(

    "profit",
    ascending=False

)

print(
    channel_summary
)

# ============================================================
# 31. TOP PRODUCTS
# ============================================================

print(
    "\n=============================================="
)

print(
    "TOP 10 PRODUCTS BY PROFIT"
)

print(
    "=============================================="
)

product_summary = (

    df.groupby(
        "product"
    )

    .agg(

        orders=(
            "order_id",
            "count"
        ),

        sales=(
            "sales",
            "sum"
        ),

        profit=(
            "profit",
            "sum"
        )

    )

)

product_summary["profit_margin"] = (

    product_summary["profit"]
    /
    product_summary["sales"]

)

top_products = (

    product_summary
    .sort_values(
        "profit",
        ascending=False
    )
    .head(10)

)

print(
    top_products
)

# ============================================================
# 32. DISCOUNT ANALYSIS
# ============================================================

print(
    "\n=============================================="
)

print(
    "DISCOUNT ANALYSIS"
)

print(
    "=============================================="
)

discount_summary = (

    df.groupby(
        "discount"
    )

    .agg(

        orders=(
            "order_id",
            "count"
        ),

        sales=(
            "sales",
            "sum"
        ),

        profit=(
            "profit",
            "sum"
        )

    )

)

discount_summary["profit_margin"] = (

    discount_summary["profit"]
    /
    discount_summary["sales"]

)

print(
    discount_summary
)

# ============================================================
# 33. MONTHLY PERFORMANCE
# ============================================================

print(
    "\n=============================================="
)

print(
    "MONTHLY PERFORMANCE"
)

print(
    "=============================================="
)

monthly_summary = (

    df.groupby(
        "year_month"
    )

    .agg(

        orders=(
            "order_id",
            "count"
        ),

        sales=(
            "sales",
            "sum"
        ),

        profit=(
            "profit",
            "sum"
        )

    )

)

monthly_summary["profit_margin"] = (

    monthly_summary["profit"]
    /
    monthly_summary["sales"]

)

print(
    monthly_summary
)

# ============================================================
# 34. SAVE SUMMARY FILES
# ============================================================

# Save useful analysis tables for later Excel / Power BI work.

region_summary.to_csv(
    "data/region_summary.csv"
)

category_summary.to_csv(
    "data/category_summary.csv"
)

channel_summary.to_csv(
    "data/channel_summary.csv"
)

customer_type_summary.to_csv(
    "data/customer_type_summary.csv"
)

product_summary.to_csv(
    "data/product_summary.csv"
)

discount_summary.to_csv(
    "data/discount_summary.csv"
)

monthly_summary.to_csv(
    "data/monthly_summary.csv"
)

# ============================================================
# 35. FINAL MESSAGE
# ============================================================

print(
    "\n=============================================="
)

print(
    "DATA GENERATION COMPLETE"
)

print(
    "=============================================="
)

print(
    "\nMain dataset:"
)

print(
    "data/sales_transactions.csv"
)

print(
    "\nAdditional summary files created:"
)

print(
    "- region_summary.csv"
)

print(
    "- category_summary.csv"
)

print(
    "- channel_summary.csv"
)

print(
    "- customer_type_summary.csv"
)

print(
    "- product_summary.csv"
)

print(
    "- discount_summary.csv"
)

print(
    "- monthly_summary.csv"
)

print(
    "\nProject 3 dataset is ready for analysis."
)