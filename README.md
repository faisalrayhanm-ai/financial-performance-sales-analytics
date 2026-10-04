# Financial Performance & Sales Analytics

## Project Overview

This project analyses a synthetic sales transaction dataset to evaluate financial performance, profitability, customer behaviour, product performance, regional performance, sales channels, and discount effectiveness.

The project demonstrates an end-to-end data analytics workflow using Python, SQL, Excel, and Power BI.

> **Note:** The dataset is synthetic and does not represent real company financial data.

---

## Business Objectives

The analysis answers questions such as:

- How much revenue and profit does the business generate?
- What is the overall profit margin?
- Which products and categories generate the most profit?
- Which regions perform best?
- Which sales channels are most profitable?
- How do discounts affect profitability?
- How do new and repeat customers contribute to sales?
- Which orders are loss-making?
- Are there products with high sales but relatively low margins?

---

## Dataset

The dataset contains **75,000 synthetic sales transactions** covering 2023–2025.

### Main fields

- Order ID
- Order Date
- Customer ID
- Region
- Sales Channel
- Customer Segment
- Product Category
- Product
- Quantity
- Unit Price
- Discount
- Gross Sales
- Discount Amount
- Sales
- Product Cost
- Operating Cost
- Total Cost
- Profit
- Profit Margin
- Payment Method
- Customer Order Number
- Customer Type
- Year
- Month
- Year-Month

---

## Key KPIs

| KPI | Result |
|---|---:|
| Total Orders | 75,000 |
| Unique Customers | 14,899 |
| Total Quantity | 215,287 |
| Total Sales | €104.11M |
| Total Cost | €80.05M |
| Total Profit | €24.06M |
| Average Order Value | €1,388.08 |
| Average Discount | 7.88% |
| Overall Profit Margin | 23.11% |
| Loss-Making Orders | 942 |

---

## Tools & Technologies

### Python

- Python
- Pandas
- NumPy
- Data cleaning
- Data validation
- Aggregation
- KPI analysis
- Business analysis
- CSV generation

### SQL

SQLite was used to create and analyse the sales database.

SQL techniques include:

- SELECT
- WHERE
- GROUP BY
- ORDER BY
- COUNT
- SUM
- AVG
- CASE
- CTEs
- Aggregations
- Multi-dimensional analysis

### Excel

Created an Excel financial performance dashboard containing:

- Executive KPIs
- Monthly performance
- Regional performance
- Category performance
- Product performance
- Channel performance
- Customer analysis
- Customer segments
- Discount analysis
- Region & channel analysis
- Category & discount analysis

### Power BI

Created an interactive three-page dashboard:

1. Executive Financial Overview
2. Product & Customer Analysis
3. Regional & Channel Performance

Power BI features include:

- KPI cards
- DAX measures
- Line charts
- Bar charts
- Column charts
- Donut charts
- Scatter plot
- Matrix
- Slicers
- Conditional formatting
- Top-N analysis

---

## Analysis Performed

### Financial Performance

Analysed:

- Total sales
- Total cost
- Total profit
- Profit margin
- Average order value
- Monthly performance
- Yearly performance

### Product Analysis

Compared products based on:

- Sales
- Profit
- Profit margin
- Order volume

### Category Analysis

Compared product categories based on:

- Revenue
- Profit
- Margin
- Order volume

### Regional Analysis

Evaluated:

- Sales by region
- Profit by region
- Profit margin by region
- Region and channel combinations

### Channel Analysis

Compared:

- Online
- Retail Store
- Wholesale

based on sales, profit, and margin.

### Customer Analysis

Analysed:

- New vs repeat customers
- Customer segments
- Sales contribution
- Profit contribution
- Customer order behaviour

### Discount Analysis

Analysed the relationship between discount levels and observed profit margins.

Higher discount levels were associated with lower observed margins in this synthetic dataset.

### Loss-Making Orders

Identified orders where:

```text
Profit < 0