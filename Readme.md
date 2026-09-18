# Retail Analytics

## 📊 Project Overview

Retail Analytics is an end-to-end retail data analytics project designed to analyze sales, inventory, purchasing, invoice processing, pricing, profitability, and operational performance.

The project demonstrates a complete analytics workflow:

Raw Data → Python → PostgreSQL → SQL → Power BI → Business Insights

---

## 🎯 Business Problem

Retail businesses generate large volumes of sales, inventory, purchasing, and operational data.

When this information is fragmented, it becomes difficult to identify:

- Revenue and profit trends
- Low-margin categories and products
- Inventory risks
- Stock-out situations
- Supplier delivery performance
- Invoice processing delays
- SLA breaches
- Invoice discrepancies
- Pricing and discount impact

Retail Analytics consolidates these areas into a structured analytical system and Power BI dashboard.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- PostgreSQL
- SQL
- Power BI
- Excel / CSV
- Git / GitHub

---

## 🏗️ Architecture

Raw Retail Data
        ↓
Python Data Cleaning & Validation
        ↓
PostgreSQL Database
        ↓
SQL Business Analysis
        ↓
Power BI Dashboard
        ↓
Business Insights

---

## 📂 Data Model

The PostgreSQL database contains:

- Customers
- Products
- Stores
- Suppliers
- Employees
- Sales
- Inventory
- Purchases
- Invoices

---

## 📊 Power BI Dashboard

### 1. Executive Overview

Provides a high-level view of:

- Total Revenue
- Total Profit
- Profit Margin
- Total Orders
- Monthly Revenue and Profit
- Category Performance
- Regional Performance

### 2. Inventory Intelligence

Analyzes:

- Total Closing Stock
- Out-of-Stock Products
- Low-Stock Products
- Stock-Out Rate
- Inventory Status
- Inventory by Category
- Stock-Out Exceptions

### 3. Invoice & Operations

Analyzes:

- Total Invoices
- Average Processing TAT
- SLA Breach %
- Invoice Discrepancies
- Invoice Processing Status
- TAT Aging
- Supplier SLA Performance
- Employee Invoice Productivity

### 4. Margin & Pricing

Analyzes:

- Revenue
- Profit
- Profit Margin
- Average Discount
- Category Margin
- Top Profitable Products
- Loss-Making Products
- Revenue vs Profit by Sub-Category
- Margin by Discount Level

---

## 📈 Key Business Metrics

| Metric | Value |
|---|---:|
| Total Revenue | $2.30M |
| Total Profit | $286.40K |
| Profit Margin | 12.47% |
| Total Orders | 5.01K |
| Transactions | 9,994 |
| Total Units Sold | 37,873 |
| Total Invoices | 7.68K |
| Average Invoice TAT | 3.46 days |
| SLA Breach Rate | 34.61% |
| Invoice Discrepancies | 795 |

---

## 🔎 Key Findings

### Sales & Profitability

Technology generated approximately $836K in revenue with a 17.40% profit margin.

Office Supplies generated approximately $719K in revenue with a 17.04% profit margin.

Furniture generated approximately $742K in revenue but had a significantly lower profit margin of approximately 2.49%.

### Product Profitability

The Canon imageCLASS 2200 Advanced Copier was the highest-profit product in the dataset, generating approximately $25.2K in profit.

Several products generated negative profit and require further investigation.

### Pricing

The analysis shows a strong association between higher discount levels and lower profit margins.

This should be treated as an observed relationship in the dataset rather than proof that discounts directly caused the losses.

### Inventory

Most inventory records were classified as Healthy, while a small number of products were identified as Low Stock or Out of Stock.

### Invoice Operations

7,680 invoices were analyzed.

The average processing TAT was 3.46 days and 34.61% of invoices were classified as SLA breaches.

795 invoices contained a discrepancy.

---

## 🧪 Data Generation Note

The sales dataset is based on a public Sample Superstore retail dataset.

The operational datasets including:

- Inventory
- Suppliers
- Purchases
- Employees
- Invoices

were synthetically generated to simulate a realistic retail operations environment.

They are not real company or MostEdge data.

---

## 💡 Skills Demonstrated

- Data cleaning
- Data validation
- Exploratory data analysis
- Business KPI development
- Relational database design
- PostgreSQL
- SQL joins
- Aggregations
- CTEs
- Window functions
- Inventory analytics
- Supplier analysis
- Invoice operations analysis
- Power BI dashboard development
- Business storytelling