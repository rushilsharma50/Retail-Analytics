# Retail Analytics — Business Insights

## 1. Executive Summary

Retail Analytics analyzes sales, profitability, inventory, purchasing, and invoice operations using Python, PostgreSQL, SQL, and Power BI.

The analysis covers 9,994 sales transactions, 5,009 orders, 37,873 units sold, and 7,680 invoices.

The overall business generated approximately $2.30M in revenue and $286.40K in profit, resulting in a 12.47% profit margin.

---

## 2. Sales & Profitability

### Overall Performance

| Metric | Value |
|---|---:|
| Revenue | $2.30M |
| Profit | $286.40K |
| Profit Margin | 12.47% |
| Orders | 5,009 |
| Units Sold | 37,873 |

### Category Performance

Technology generated approximately $836K in revenue with a 17.40% profit margin.

Office Supplies generated approximately $719K in revenue with a 17.04% profit margin.

Furniture generated approximately $742K in revenue but had a much lower profit margin of approximately 2.49%.

### Business Observation

Furniture generates substantial revenue but comparatively low profitability.

This suggests that revenue alone should not be used to evaluate category performance. Margin should also be monitored when evaluating product and category performance.

---

## 3. Product Profitability

The Canon imageCLASS 2200 Advanced Copier generated approximately $25.2K in profit and was the highest-profit product in the dataset.

Several products generated negative profit.

The analysis identified products such as:

- Cubify CubeX 3D Printer Double Head
- Lexmark MX611dhe
- Cubify CubeX Triple Head
- Chromcraft Bull-Nose Conference Tables
- Bush Advantage Conference Table

among the largest loss-making products.

### Business Observation

High-revenue products do not always generate high profit.

Products should therefore be evaluated using both revenue and profitability rather than sales volume alone.

---

## 4. Pricing & Discount Analysis

The Power BI analysis shows a strong negative association between higher discount levels and profit margin.

As discount levels increase, observed profit margins decline significantly in this dataset.

### Important Interpretation

This is an observed relationship, not proof that discounts directly caused the losses.

Further analysis would be required to control for product category, product type, and sales mix before making a causal conclusion.

---

## 5. Inventory Analysis

The inventory dataset contains 469,104 inventory records.

| Inventory Status | Records |
|---|---:|
| Healthy | 468,837 |
| Low Stock | 185 |
| Out of Stock | 82 |

Five products were identified with stock-out flags in the analyzed inventory records.

These exceptions included:

- Macally Suction Cup Mount
- Panasonic KP-4ABK Battery-Operated Pencil Sharpener
- Presstex Flexible Ring Binders
- Round Specialty Laser Printer Labels
- Wireless Extenders zBoost YX545 SOHO Signal Booster

### Business Observation

The dashboard provides an exception-oriented view of inventory so that stock issues can be investigated instead of relying only on total inventory levels.

---

## 6. Invoice Operations

A total of 7,680 invoices were analyzed.

| Metric | Value |
|---|---:|
| Total Invoices | 7,680 |
| Average Processing TAT | 3.46 days |
| Maximum TAT | 12 days |
| SLA Breach Rate | 34.61% |
| Invoices with Discrepancy | 795 |

### Invoice Status

- Processed: 5,022
- Processed Late: 1,938
- Pending / Delayed: 720

### Business Observation

Invoice processing represents an important operational monitoring area.

The SLA breach rate and processing-time distribution can be used to identify operational bottlenecks and prioritize delayed invoices.

---

## 7. Supplier Analysis

Supplier-level analysis evaluates:

- Purchase volume
- Purchase spending
- Delivery performance
- Invoice processing performance

Supplier delivery performance varied across the simulated supplier dataset.

The highest observed late-delivery rate was approximately 75%, while the lowest was approximately 69%.

### Important Interpretation

The supplier operational data is synthetically generated for this project.

Therefore, these percentages should be interpreted as demonstration data rather than real-world supplier benchmarks.

---

## 8. Invoice Discrepancies

The analysis identified:

- 795 invoices with discrepancies
- Approximately $16.08K in absolute discrepancy value

The discrepancy analysis can help identify invoices requiring reconciliation between expected and actual amounts.

---

## 9. Regional Performance

The dataset contains four regions:

- West
- East
- Central
- South

The West region generated the highest revenue at approximately $725K and approximately $108K in profit.

The Central region generated approximately $501K in revenue and approximately $39.7K in profit.

### Business Observation

Regional revenue and regional profitability should be monitored together because higher sales volume does not necessarily result in proportionally higher profit.

---

## 10. Key Business Questions Answered

Retail Analytics was designed to answer questions such as:

1. How much revenue and profit are being generated?
2. Which categories generate the highest margins?
3. Which products generate the most profit?
4. Which products generate losses?
5. How are discounts associated with profitability?
6. Which inventory records require attention?
7. How many invoices are delayed?
8. What percentage of invoices breach SLA?
9. Which suppliers have delivery-performance issues?
10. Which employees process the highest invoice volumes?
11. Where are invoice discrepancies occurring?
12. How does profitability vary across regions and categories?

---

## 11. Recommended Business Actions

### Profitability

Investigate consistently loss-making products and review their pricing, cost structure, and discount levels.

### Pricing

Review high-discount transactions and evaluate whether discount levels are sustainable for specific products or categories.

### Inventory

Monitor stock-out and low-stock exceptions and prioritize products with recurring demand.

### Invoice Operations

Investigate invoices with long processing TAT and SLA breaches.

### Supplier Management

Review supplier delivery performance and investigate suppliers with consistently high late-delivery rates.

### Reconciliation

Prioritize invoices with large absolute discrepancies for financial reconciliation.

---

## 12. Data Limitations

The sales dataset is based on a public Sample Superstore dataset.

The operational datasets for:

- Inventory
- Suppliers
- Purchases
- Employees
- Invoices

were synthetically generated to simulate retail operations.

Therefore, operational findings should be treated as analytical demonstrations rather than real company performance measurements.

The project focuses on demonstrating the analytical workflow and business analysis process.

---

## 13. Final Analytical Workflow

Raw Data
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
↓
Actionable Recommendations