import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule


# ============================================================
# FINANCIAL PERFORMANCE & SALES ANALYTICS
# STEP 5 - CREATE EXCEL DASHBOARD
# ============================================================

print("=" * 75)
print("CREATING EXCEL FINANCIAL PERFORMANCE DASHBOARD")
print("=" * 75)


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DASHBOARD_DIR = BASE_DIR / "dashboard"

DASHBOARD_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DASHBOARD_DIR / "Financial_Performance_Sales_Analytics.xlsx"


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("\nLoading data...")

sales_file = DATA_DIR / "sales_transactions.csv"

df = pd.read_csv(sales_file)

df["order_date"] = pd.to_datetime(df["order_date"])

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")


# ------------------------------------------------------------
# CREATE SUMMARY DATASETS
# ------------------------------------------------------------

df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
df["year"] = df["order_date"].dt.year


# Monthly
monthly = (
    df.groupby("year_month")
    .agg(
        Orders=("order_id", "count"),
        Sales=("sales", "sum"),
        Cost=("cost", "sum"),
        Profit=("profit", "sum"),
    )
    .reset_index()
)

monthly["Profit Margin"] = monthly["Profit"] / monthly["Sales"]
monthly["AOV"] = monthly["Sales"] / monthly["Orders"]


# Regional
regional = (
    df.groupby("region")
    .agg(
        Orders=("order_id", "count"),
        Customers=("customer_id", "nunique"),
        Sales=("sales", "sum"),
        Cost=("cost", "sum"),
        Profit=("profit", "sum"),
    )
    .reset_index()
)

regional["Profit Margin"] = regional["Profit"] / regional["Sales"]
regional["AOV"] = regional["Sales"] / regional["Orders"]


# Category
category = (
    df.groupby("product_category")
    .agg(
        Orders=("order_id", "count"),
        Quantity=("quantity", "sum"),
        Sales=("sales", "sum"),
        Cost=("cost", "sum"),
        Profit=("profit", "sum"),
    )
    .reset_index()
)

category["Profit Margin"] = category["Profit"] / category["Sales"]
category["AOV"] = category["Sales"] / category["Orders"]


# Product
product = (
    df.groupby("product")
    .agg(
        Orders=("order_id", "count"),
        Sales=("sales", "sum"),
        Cost=("cost", "sum"),
        Profit=("profit", "sum"),
        Quantity=("quantity", "sum"),
    )
    .reset_index()
)

product["Profit Margin"] = product["Profit"] / product["Sales"]
product["AOV"] = product["Sales"] / product["Orders"]

product = product.sort_values("Profit", ascending=False)


# Channel
channel = (
    df.groupby("sales_channel")
    .agg(
        Orders=("order_id", "count"),
        Sales=("sales", "sum"),
        Cost=("cost", "sum"),
        Profit=("profit", "sum"),
    )
    .reset_index()
)

channel["Profit Margin"] = channel["Profit"] / channel["Sales"]
channel["AOV"] = channel["Sales"] / channel["Orders"]


# Customer type
customer_type = (
    df.groupby("customer_type")
    .agg(
        Orders=("order_id", "count"),
        Customers=("customer_id", "nunique"),
        Sales=("sales", "sum"),
        Profit=("profit", "sum"),
    )
    .reset_index()
)

customer_type["Profit Margin"] = (
    customer_type["Profit"] / customer_type["Sales"]
)

customer_type["AOV"] = (
    customer_type["Sales"] / customer_type["Orders"]
)


# Customer segment
customer_segment = (
    df.groupby("customer_segment")
    .agg(
        Orders=("order_id", "count"),
        Customers=("customer_id", "nunique"),
        Sales=("sales", "sum"),
        Profit=("profit", "sum"),
    )
    .reset_index()
)

customer_segment["Profit Margin"] = (
    customer_segment["Profit"] / customer_segment["Sales"]
)

customer_segment["AOV"] = (
    customer_segment["Sales"] / customer_segment["Orders"]
)


# Discount
discount = (
    df.groupby("discount")
    .agg(
        Orders=("order_id", "count"),
        Sales=("sales", "sum"),
        Cost=("cost", "sum"),
        Profit=("profit", "sum"),
    )
    .reset_index()
)

discount["Profit Margin"] = discount["Profit"] / discount["Sales"]
discount["AOV"] = discount["Sales"] / discount["Orders"]


# Region + Channel
region_channel = (
    df.groupby(["region", "sales_channel"])
    .agg(
        Orders=("order_id", "count"),
        Sales=("sales", "sum"),
        Profit=("profit", "sum"),
    )
    .reset_index()
)

region_channel["Profit Margin"] = (
    region_channel["Profit"] / region_channel["Sales"]
)


# Category + Discount
category_discount = (
    df.groupby(["product_category", "discount"])
    .agg(
        Orders=("order_id", "count"),
        Sales=("sales", "sum"),
        Profit=("profit", "sum"),
    )
    .reset_index()
)

category_discount["Profit Margin"] = (
    category_discount["Profit"] / category_discount["Sales"]
)


# ------------------------------------------------------------
# KPI CALCULATIONS
# ------------------------------------------------------------

total_orders = len(df)
total_customers = df["customer_id"].nunique()
total_sales = df["sales"].sum()
total_cost = df["cost"].sum()
total_profit = df["profit"].sum()
average_order_value = total_sales / total_orders
profit_margin = total_profit / total_sales
average_discount = df["discount"].mean()
loss_making_orders = (df["profit"] < 0).sum()


# ------------------------------------------------------------
# CREATE WORKBOOK
# ------------------------------------------------------------

print("\nCreating Excel workbook...")

wb = Workbook()

# Remove default sheet
default_sheet = wb.active
wb.remove(default_sheet)


# ------------------------------------------------------------
# COLORS / STYLES
# ------------------------------------------------------------

dark_fill = PatternFill(
    "solid",
    fgColor="17365D"
)

blue_fill = PatternFill(
    "solid",
    fgColor="1F4E78"
)

light_blue_fill = PatternFill(
    "solid",
    fgColor="D9EAF7"
)

green_fill = PatternFill(
    "solid",
    fgColor="E2F0D9"
)

orange_fill = PatternFill(
    "solid",
    fgColor="FCE4D6"
)

grey_fill = PatternFill(
    "solid",
    fgColor="E7E6E6"
)

white_font = Font(
    color="FFFFFF",
    bold=True
)

header_font = Font(
    bold=True,
    color="FFFFFF"
)

title_font = Font(
    size=18,
    bold=True,
    color="FFFFFF"
)

subtitle_font = Font(
    size=11,
    italic=True
)

kpi_value_font = Font(
    size=16,
    bold=True,
    color="17365D"
)

thin_border = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9")
)


# ------------------------------------------------------------
# HELPER FUNCTION
# ------------------------------------------------------------

def write_dataframe(ws, dataframe, start_row=1, start_col=1):

    for col_index, column in enumerate(
        dataframe.columns,
        start_col
    ):
        cell = ws.cell(
            row=start_row,
            column=col_index,
            value=column
        )

        cell.fill = blue_fill
        cell.font = header_font
        cell.alignment = Alignment(
            horizontal="center"
        )
        cell.border = thin_border

    for row_index, row in enumerate(
        dataframe.itertuples(index=False),
        start_row + 1
    ):

        for col_index, value in enumerate(
            row,
            start_col
        ):

            cell = ws.cell(
                row=row_index,
                column=col_index,
                value=value
            )

            cell.border = thin_border

            if isinstance(value, float):
                cell.number_format = '#,##0.00'


def autofit_columns(ws):

    for column_cells in ws.columns:

        max_length = 0

        column_letter = get_column_letter(
            column_cells[0].column
        )

        for cell in column_cells:

            try:
                length = len(str(cell.value))

                if length > max_length:
                    max_length = length

            except:
                pass

        ws.column_dimensions[
            column_letter
        ].width = min(max_length + 2, 28)


# ------------------------------------------------------------
# EXECUTIVE DASHBOARD
# ------------------------------------------------------------

ws = wb.create_sheet("Dashboard")

ws.sheet_view.showGridLines = False


# Title
ws.merge_cells("A1:L2")

title = ws["A1"]

title.value = "FINANCIAL PERFORMANCE & SALES ANALYTICS"

title.fill = dark_fill
title.font = title_font
title.alignment = Alignment(
    horizontal="center",
    vertical="center"
)


ws.merge_cells("A3:L3")

ws["A3"] = (
    "Executive Financial Dashboard | "
    "Synthetic Dataset | 2023–2025"
)

ws["A3"].font = subtitle_font
ws["A3"].alignment = Alignment(
    horizontal="center"
)


# KPI helper
def create_kpi(
    cell_range,
    title,
    value,
    fill
):

    ws.merge_cells(cell_range)

    start_cell = cell_range.split(":")[0]

    cell = ws[start_cell]

    cell.value = f"{title}\n{value}"

    cell.fill = fill
    cell.font = kpi_value_font

    cell.alignment = Alignment(
        horizontal="center",
        vertical="center",
        wrap_text=True
    )

    cell.border = thin_border


create_kpi(
    "A5:B7",
    "TOTAL SALES",
    f"€{total_sales:,.2f}",
    light_blue_fill
)

create_kpi(
    "C5:D7",
    "TOTAL COST",
    f"€{total_cost:,.2f}",
    grey_fill
)

create_kpi(
    "E5:F7",
    "TOTAL PROFIT",
    f"€{total_profit:,.2f}",
    green_fill
)

create_kpi(
    "G5:H7",
    "PROFIT MARGIN",
    f"{profit_margin:.2%}",
    green_fill
)

create_kpi(
    "I5:J7",
    "TOTAL ORDERS",
    f"{total_orders:,}",
    light_blue_fill
)

create_kpi(
    "K5:L7",
    "AVERAGE ORDER VALUE",
    f"€{average_order_value:,.2f}",
    orange_fill
)


# Additional KPIs
create_kpi(
    "A9:C11",
    "UNIQUE CUSTOMERS",
    f"{total_customers:,}",
    light_blue_fill
)

create_kpi(
    "D9:F11",
    "AVERAGE DISCOUNT",
    f"{average_discount:.2%}",
    grey_fill
)

create_kpi(
    "G9:I11",
    "LOSS-MAKING ORDERS",
    f"{loss_making_orders:,}",
    orange_fill
)

create_kpi(
    "J9:L11",
    "BEST REGION",
    regional.loc[
        regional["Profit"].idxmax(),
        "region"
    ],
    green_fill
)


# ------------------------------------------------------------
# DASHBOARD DATA
# ------------------------------------------------------------

# Monthly data
start_row = 14

ws["A14"] = "MONTHLY SALES & PROFIT"

ws["A14"].font = Font(
    bold=True,
    size=12
)

monthly_chart_data = monthly[
    [
        "year_month",
        "Sales",
        "Profit"
    ]
]

write_dataframe(
    ws,
    monthly_chart_data,
    start_row=15,
    start_col=1
)


# ------------------------------------------------------------
# MONTHLY CHART
# ------------------------------------------------------------

line_chart = LineChart()

line_chart.title = "Monthly Sales vs Profit"

line_chart.y_axis.title = "Amount (€)"

line_chart.x_axis.title = "Month"

line_chart.height = 8

line_chart.width = 15

data = Reference(
    ws,
    min_col=2,
    max_col=3,
    min_row=15,
    max_row=15 + len(monthly)
)

categories = Reference(
    ws,
    min_col=1,
    min_row=16,
    max_row=15 + len(monthly)
)

line_chart.add_data(
    data,
    titles_from_data=True
)

line_chart.set_categories(categories)

ws.add_chart(
    line_chart,
    "E14"
)


# ------------------------------------------------------------
# REGIONAL CHART DATA
# ------------------------------------------------------------

region_start = 14

ws["A51"] = "REGIONAL PERFORMANCE"

ws["A51"].font = Font(
    bold=True,
    size=12
)

regional_chart_data = regional[
    [
        "region",
        "Sales",
        "Profit",
        "Profit Margin"
    ]
]

write_dataframe(
    ws,
    regional_chart_data,
    start_row=52,
    start_col=1
)


# Regional chart
bar_chart = BarChart()

bar_chart.type = "col"

bar_chart.style = 10

bar_chart.title = "Profit by Region"

bar_chart.y_axis.title = "Profit (€)"

bar_chart.x_axis.title = "Region"

bar_chart.height = 8

bar_chart.width = 15

data = Reference(
    ws,
    min_col=3,
    min_row=52,
    max_row=52 + len(regional)
)

categories = Reference(
    ws,
    min_col=1,
    min_row=53,
    max_row=52 + len(regional)
)

bar_chart.add_data(
    data,
    titles_from_data=True
)

bar_chart.set_categories(categories)

ws.add_chart(
    bar_chart,
    "E51"
)


# ------------------------------------------------------------
# CATEGORY CHART
# ------------------------------------------------------------

ws["A61"] = "CATEGORY PERFORMANCE"

ws["A61"].font = Font(
    bold=True,
    size=12
)

category_chart_data = category[
    [
        "product_category",
        "Sales",
        "Profit",
        "Profit Margin"
    ]
]

write_dataframe(
    ws,
    category_chart_data,
    start_row=62,
    start_col=1
)


category_chart = BarChart()

category_chart.type = "bar"

category_chart.style = 11

category_chart.title = "Profit by Product Category"

category_chart.x_axis.title = "Profit (€)"

category_chart.height = 8

category_chart.width = 15

data = Reference(
    ws,
    min_col=3,
    min_row=62,
    max_row=62 + len(category)
)

categories_ref = Reference(
    ws,
    min_col=1,
    min_row=63,
    max_row=62 + len(category)
)

category_chart.add_data(
    data,
    titles_from_data=True
)

category_chart.set_categories(
    categories_ref
)

ws.add_chart(
    category_chart,
    "E61"
)


# ------------------------------------------------------------
# FREEZE / COLUMN WIDTHS
# ------------------------------------------------------------

ws.freeze_panes = "A14"

for column in range(1, 13):

    ws.column_dimensions[
        get_column_letter(column)
    ].width = 18


# ------------------------------------------------------------
# DETAIL SHEETS
# ------------------------------------------------------------

detail_sheets = {
    "Monthly Performance": monthly,
    "Regional Performance": regional,
    "Category Performance": category,
    "Product Performance": product,
    "Channel Performance": channel,
    "Customer Analysis": customer_type,
    "Customer Segments": customer_segment,
    "Discount Analysis": discount,
    "Region & Channel": region_channel,
    "Category & Discount": category_discount,
}


for sheet_name, dataframe in detail_sheets.items():

    ws_detail = wb.create_sheet(sheet_name)

    ws_detail.sheet_view.showGridLines = False

    ws_detail["A1"] = sheet_name

    ws_detail["A1"].font = Font(
        size=16,
        bold=True
    )

    ws_detail["A2"] = (
        "Financial Performance & Sales Analytics"
    )

    write_dataframe(
        ws_detail,
        dataframe,
        start_row=4,
        start_col=1
    )

    ws_detail.freeze_panes = "A5"

    autofit_columns(ws_detail)


# ------------------------------------------------------------
# RAW DATA SHEET
# ------------------------------------------------------------

print("\nAdding raw data sheet...")

raw_ws = wb.create_sheet("Raw Data")

raw_ws.sheet_view.showGridLines = False

# Write only the first 75,000 rows.
write_dataframe(
    raw_ws,
    df,
    start_row=1,
    start_col=1
)

raw_ws.freeze_panes = "A2"

autofit_columns(raw_ws)


# ------------------------------------------------------------
# PROJECT NOTES
# ------------------------------------------------------------

notes_ws = wb.create_sheet("Project Notes")

notes_ws.sheet_view.showGridLines = False

notes_ws["A1"] = "PROJECT NOTES"

notes_ws["A1"].font = Font(
    size=18,
    bold=True
)

notes = [
    "Project: Financial Performance & Sales Analytics",
    "Dataset: Synthetic sales transaction data",
    "Time period: 2023–2025",
    "Number of transactions: 75,000",
    "Unique customers: 14,899",
    "Total sales: €104,105,772.51",
    "Total cost: €80,045,417.19",
    "Total profit: €24,060,355.76",
    "Overall profit margin: 23.11%",
    "Average order value: €1,388.08",
    "Average discount: 7.88%",
    "Loss-making orders: 942",
    "",
    "Important:",
    "All financial values are simulated for portfolio analysis.",
    "The dataset does not represent a real company.",
    "Business relationships shown in the analysis are analytical associations, not causal conclusions.",
    "",
    "Main business questions:",
    "• Where are we generating the most profit?",
    "• Which products have strong sales but weak margins?",
    "• Which regions perform best?",
    "• Which sales channels are most profitable?",
    "• How do discounts affect simulated profitability?",
    "• How do new and repeat customers contribute to sales?",
]

for row_number, note in enumerate(notes, start=3):

    notes_ws.cell(
        row=row_number,
        column=1,
        value=note
    )

notes_ws.column_dimensions["A"].width = 100


# ------------------------------------------------------------
# FORMATTING NUMBERS
# ------------------------------------------------------------

for ws_sheet in wb.worksheets:

    for row in ws_sheet.iter_rows():

        for cell in row:

            if isinstance(cell.value, float):

                # Percentage columns
                if (
                    "Margin" in str(
                        ws_sheet.cell(
                            row=cell.row,
                            column=cell.column
                        ).value
                    )
                ):
                    pass


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

print("\nSaving workbook...")

wb.save(OUTPUT_FILE)

print("\n" + "=" * 75)
print("EXCEL DASHBOARD CREATED SUCCESSFULLY")
print("=" * 75)

print(f"\nFile:")
print(OUTPUT_FILE)

print("\nSheets created:")

for sheet in wb.sheetnames:
    print(f"✓ {sheet}")

print("\nNext step: Power BI dashboard")