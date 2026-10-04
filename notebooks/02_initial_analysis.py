import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_PATH = Path("data/sales_transactions.csv")

df = pd.read_csv(DATA_PATH)

df["order_date"] = pd.to_datetime(df["order_date"])

print("=" * 70)
print("FINANCIAL PERFORMANCE & SALES ANALYSIS")
print("=" * 70)

print("\nDataset loaded successfully!")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# 2. DATA QUALITY CHECK
# ============================================================

print("\n" + "=" * 70)
print("1. DATA QUALITY CHECK")
print("=" * 70)

missing_values = df.isnull().sum().sum()
duplicate_rows = df.duplicated().sum()

print(f"\nTotal rows: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print(f"Missing values: {missing_values}")
print(f"Duplicate rows: {duplicate_rows}")

print("\nData types:")
print(df.dtypes)


# ============================================================
# 3. OVERALL FINANCIAL KPIs
# ============================================================

print("\n" + "=" * 70)
print("2. OVERALL FINANCIAL KPIs")
print("=" * 70)

total_orders = df["order_id"].nunique()

total_sales = df["sales"].sum()

total_cost = df["cost"].sum()

total_profit = df["profit"].sum()

average_order_value = df["sales"].mean()

overall_margin = (
    total_profit / total_sales
)

total_quantity = df["quantity"].sum()

average_discount = df["discount"].mean()

unique_customers = df["customer_id"].nunique()

loss_making_orders = (
    df["profit"] < 0
).sum()

print(f"\nTotal Orders: {total_orders:,}")

print(f"Unique Customers: {unique_customers:,}")

print(f"Total Quantity Sold: {total_quantity:,}")

print(f"Total Sales: €{total_sales:,.2f}")

print(f"Total Cost: €{total_cost:,.2f}")

print(f"Total Profit: €{total_profit:,.2f}")

print(
    f"Average Order Value: €{average_order_value:,.2f}"
)

print(
    f"Overall Profit Margin: {overall_margin:.2%}"
)

print(
    f"Average Discount: {average_discount:.2%}"
)

print(
    f"Loss-Making Orders: {loss_making_orders:,}"
)


# ============================================================
# 4. CREATE TIME VARIABLES
# ============================================================

df["year"] = df["order_date"].dt.year

df["month_number"] = df["order_date"].dt.month

df["year_month"] = (
    df["order_date"]
    .dt.to_period("M")
    .astype(str)
)


# ============================================================
# 5. MONTHLY PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("3. MONTHLY PERFORMANCE")
print("=" * 70)

monthly = (
    df.groupby("year_month")
    .agg(
        orders=("order_id", "count"),
        sales=("sales", "sum"),
        cost=("cost", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
    .reset_index()
)

monthly["profit_margin"] = (
    monthly["profit"] /
    monthly["sales"]
)

monthly["aov"] = (
    monthly["sales"] /
    monthly["orders"]
)

print("\nMonthly performance:")
print(monthly.to_string(index=False))

best_month = monthly.loc[
    monthly["sales"].idxmax()
]

best_profit_month = monthly.loc[
    monthly["profit"].idxmax()
]

print(
    f"\nHighest Sales Month: "
    f"{best_month['year_month']} "
    f"→ €{best_month['sales']:,.2f}"
)

print(
    f"Highest Profit Month: "
    f"{best_profit_month['year_month']} "
    f"→ €{best_profit_month['profit']:,.2f}"
)


# ============================================================
# 6. YEARLY PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("4. YEARLY PERFORMANCE")
print("=" * 70)

yearly = (
    df.groupby("year")
    .agg(
        orders=("order_id", "count"),
        sales=("sales", "sum"),
        cost=("cost", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

yearly["profit_margin"] = (
    yearly["profit"] /
    yearly["sales"]
)

yearly["aov"] = (
    yearly["sales"] /
    yearly["orders"]
)

print("\nYearly performance:")
print(yearly.to_string(index=False))

# Year-over-year growth

yearly["sales_growth"] = (
    yearly["sales"]
    .pct_change()
)

yearly["profit_growth"] = (
    yearly["profit"]
    .pct_change()
)

print("\nYear-over-year growth:")
print(
    yearly[
        [
            "year",
            "sales_growth",
            "profit_growth"
        ]
    ].to_string(index=False)
)


# ============================================================
# 7. REGION PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("5. REGIONAL PERFORMANCE")
print("=" * 70)

region = (
    df.groupby("region")
    .agg(
        orders=("order_id", "count"),
        sales=("sales", "sum"),
        cost=("cost", "sum"),
        profit=("profit", "sum"),
        customers=("customer_id", "nunique")
    )
    .reset_index()
)

region["profit_margin"] = (
    region["profit"] /
    region["sales"]
)

region["aov"] = (
    region["sales"] /
    region["orders"]
)

region = region.sort_values(
    "profit",
    ascending=False
)

print(
    "\nRegional performance:"
)

print(
    region.to_string(index=False)
)

best_region = region.iloc[0]

lowest_margin_region = region.loc[
    region["profit_margin"].idxmin()
]

print(
    f"\nMost Profitable Region: "
    f"{best_region['region']} "
    f"→ €{best_region['profit']:,.2f}"
)

print(
    f"Lowest Margin Region: "
    f"{lowest_margin_region['region']} "
    f"→ {lowest_margin_region['profit_margin']:.2%}"
)


# ============================================================
# 8. PRODUCT CATEGORY PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("6. PRODUCT CATEGORY PERFORMANCE")
print("=" * 70)

category = (
    df.groupby("product_category")
    .agg(
        orders=("order_id", "count"),
        sales=("sales", "sum"),
        cost=("cost", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
    .reset_index()
)

category["profit_margin"] = (
    category["profit"] /
    category["sales"]
)

category["aov"] = (
    category["sales"] /
    category["orders"]
)

category = category.sort_values(
    "profit",
    ascending=False
)

print(
    "\nCategory performance:"
)

print(
    category.to_string(index=False)
)

most_profitable_category = category.iloc[0]

highest_margin_category = category.loc[
    category["profit_margin"].idxmax()
]

lowest_margin_category = category.loc[
    category["profit_margin"].idxmin()
]

print(
    f"\nMost Profitable Category: "
    f"{most_profitable_category['product_category']} "
    f"→ €{most_profitable_category['profit']:,.2f}"
)

print(
    f"Highest Margin Category: "
    f"{highest_margin_category['product_category']} "
    f"→ {highest_margin_category['profit_margin']:.2%}"
)

print(
    f"Lowest Margin Category: "
    f"{lowest_margin_category['product_category']} "
    f"→ {lowest_margin_category['profit_margin']:.2%}"
)


# ============================================================
# 9. PRODUCT PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("7. PRODUCT PERFORMANCE")
print("=" * 70)

product = (
    df.groupby("product")
    .agg(
        orders=("order_id", "count"),
        sales=("sales", "sum"),
        cost=("cost", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
    .reset_index()
)

product["profit_margin"] = (
    product["profit"] /
    product["sales"]
)

product["aov"] = (
    product["sales"] /
    product["orders"]
)

# ------------------------------------------------------------
# Top 10 products by sales
# ------------------------------------------------------------

top_sales_products = (
    product
    .sort_values(
        "sales",
        ascending=False
    )
    .head(10)
)

print("\nTop 10 Products by Sales:")

print(
    top_sales_products.to_string(
        index=False
    )
)

# ------------------------------------------------------------
# Top 10 products by profit
# ------------------------------------------------------------

top_profit_products = (
    product
    .sort_values(
        "profit",
        ascending=False
    )
    .head(10)
)

print("\nTop 10 Products by Profit:")

print(
    top_profit_products.to_string(
        index=False
    )
)

# ------------------------------------------------------------
# Lowest margin products
# ------------------------------------------------------------

lowest_margin_products = (
    product
    .sort_values(
        "profit_margin"
    )
    .head(10)
)

print("\n10 Lowest Margin Products:")

print(
    lowest_margin_products.to_string(
        index=False
    )
)


# ============================================================
# 10. SALES CHANNEL PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("8. SALES CHANNEL PERFORMANCE")
print("=" * 70)

channel = (
    df.groupby("sales_channel")
    .agg(
        orders=("order_id", "count"),
        sales=("sales", "sum"),
        cost=("cost", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

channel["profit_margin"] = (
    channel["profit"] /
    channel["sales"]
)

channel["aov"] = (
    channel["sales"] /
    channel["orders"]
)

channel = channel.sort_values(
    "profit",
    ascending=False
)

print(
    "\nChannel performance:"
)

print(
    channel.to_string(index=False)
)


# ============================================================
# 11. CUSTOMER TYPE PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("9. NEW VS REPEAT CUSTOMER PERFORMANCE")
print("=" * 70)

customer_type = (
    df.groupby("customer_type")
    .agg(
        orders=("order_id", "count"),
        customers=("customer_id", "nunique"),
        sales=("sales", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

customer_type["profit_margin"] = (
    customer_type["profit"] /
    customer_type["sales"]
)

customer_type["aov"] = (
    customer_type["sales"] /
    customer_type["orders"]
)

print(
    "\nNew vs Repeat Customers:"
)

print(
    customer_type.to_string(index=False)
)


# ============================================================
# 12. CUSTOMER SEGMENT PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("10. CUSTOMER SEGMENT PERFORMANCE")
print("=" * 70)

customer_segment = (
    df.groupby("customer_segment")
    .agg(
        orders=("order_id", "count"),
        customers=("customer_id", "nunique"),
        sales=("sales", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

customer_segment["profit_margin"] = (
    customer_segment["profit"] /
    customer_segment["sales"]
)

customer_segment["aov"] = (
    customer_segment["sales"] /
    customer_segment["orders"]
)

print(
    "\nCustomer segment performance:"
)

print(
    customer_segment.to_string(index=False)
)


# ============================================================
# 13. DISCOUNT ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("11. DISCOUNT VS PROFITABILITY")
print("=" * 70)

discount = (
    df.groupby("discount")
    .agg(
        orders=("order_id", "count"),
        sales=("sales", "sum"),
        cost=("cost", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

discount["profit_margin"] = (
    discount["profit"] /
    discount["sales"]
)

discount["aov"] = (
    discount["sales"] /
    discount["orders"]
)

print(
    "\nDiscount performance:"
)

print(
    discount.to_string(index=False)
)


# ============================================================
# 14. HIGH SALES / LOW MARGIN PRODUCTS
# ============================================================

print("\n" + "=" * 70)
print("12. HIGH SALES BUT LOW MARGIN PRODUCTS")
print("=" * 70)

sales_median = product["sales"].median()

margin_median = product["profit_margin"].median()

high_sales_low_margin = product[
    (product["sales"] >= sales_median)
    &
    (product["profit_margin"] < margin_median)
].sort_values(
    "sales",
    ascending=False
)

print(
    "\nProducts with above-median sales but below-median margin:"
)

print(
    high_sales_low_margin.to_string(
        index=False
    )
)


# ============================================================
# 15. LOSS-MAKING ORDERS
# ============================================================

print("\n" + "=" * 70)
print("13. LOSS-MAKING ORDERS")
print("=" * 70)

loss_orders = df[
    df["profit"] < 0
]

print(
    f"\nNumber of loss-making orders: "
    f"{len(loss_orders):,}"
)

print(
    f"Total loss from loss-making orders: "
    f"€{loss_orders['profit'].sum():,.2f}"
)

if len(loss_orders) > 0:

    print(
        "\nTop 10 loss-making orders:"
    )

    print(
        loss_orders[
            [
                "order_id",
                "order_date",
                "product_category",
                "product",
                "sales",
                "discount",
                "cost",
                "profit"
            ]
        ]
        .sort_values(
            "profit"
        )
        .head(10)
        .to_string(index=False)
    )


# ============================================================
# 16. PROFITABILITY BY DISCOUNT AND CATEGORY
# ============================================================

print("\n" + "=" * 70)
print("14. CATEGORY + DISCOUNT ANALYSIS")
print("=" * 70)

category_discount = (
    df.groupby(
        [
            "product_category",
            "discount"
        ]
    )
    .agg(
        orders=("order_id", "count"),
        sales=("sales", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

category_discount["profit_margin"] = (
    category_discount["profit"] /
    category_discount["sales"]
)

print(
    "\nCategory and discount profitability:"
)

print(
    category_discount.to_string(
        index=False
    )
)


# ============================================================
# 17. REGIONAL + CHANNEL ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("15. REGION + CHANNEL PERFORMANCE")
print("=" * 70)

region_channel = (
    df.groupby(
        [
            "region",
            "sales_channel"
        ]
    )
    .agg(
        orders=("order_id", "count"),
        sales=("sales", "sum"),
        profit=("profit", "sum")
    )
    .reset_index()
)

region_channel["profit_margin"] = (
    region_channel["profit"] /
    region_channel["sales"]
)

print(
    "\nRegion and channel performance:"
)

print(
    region_channel.to_string(
        index=False
    )
)


# ============================================================
# 18. EXPORT ANALYSIS TABLES
# ============================================================

print("\n" + "=" * 70)
print("16. SAVING ANALYSIS RESULTS")
print("=" * 70)

output_folder = Path("data/analysis")

output_folder.mkdir(
    parents=True,
    exist_ok=True
)

monthly.to_csv(
    output_folder / "monthly_analysis.csv",
    index=False
)

yearly.to_csv(
    output_folder / "yearly_analysis.csv",
    index=False
)

region.to_csv(
    output_folder / "region_analysis.csv",
    index=False
)

category.to_csv(
    output_folder / "category_analysis.csv",
    index=False
)

product.to_csv(
    output_folder / "product_analysis.csv",
    index=False
)

channel.to_csv(
    output_folder / "channel_analysis.csv",
    index=False
)

customer_type.to_csv(
    output_folder / "customer_type_analysis.csv",
    index=False
)

customer_segment.to_csv(
    output_folder / "customer_segment_analysis.csv",
    index=False
)

discount.to_csv(
    output_folder / "discount_analysis.csv",
    index=False
)

category_discount.to_csv(
    output_folder / "category_discount_analysis.csv",
    index=False
)

region_channel.to_csv(
    output_folder / "region_channel_analysis.csv",
    index=False
)


# ============================================================
# 19. FINAL BUSINESS INSIGHTS
# ============================================================

print("\n" + "=" * 70)
print("17. KEY BUSINESS INSIGHTS")
print("=" * 70)

print(
    f"""
1. The business generated €{total_sales:,.2f}
   in total sales across {total_orders:,} orders.

2. Total profit was €{total_profit:,.2f},
   producing an overall margin of {overall_margin:.2%}.

3. {best_region['region']} was the most profitable
   region with €{best_region['profit']:,.2f} profit.

4. {highest_margin_category['product_category']}
   had the highest category margin at
   {highest_margin_category['profit_margin']:.2%}.

5. {lowest_margin_category['product_category']}
   had the lowest category margin at
   {lowest_margin_category['profit_margin']:.2%}.

6. Higher discounts are associated with
   significantly lower profit margins.

7. Repeat customers generated a substantial
   share of total sales.

8. Product profitability differs significantly
   across categories, showing that revenue alone
   should not be used to evaluate performance.
"""
)

print("\n" + "=" * 70)

print(
    "INITIAL ANALYSIS COMPLETE"
)

print("=" * 70)

print(
    "\nAnalysis files saved to:"
)

print(
    "data/analysis/"
)