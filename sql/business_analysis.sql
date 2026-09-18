-- ============================================================
-- QUERY 1: OVERALL BUSINESS PERFORMANCE
-- ============================================================

SELECT
    COUNT(*) AS transactions,
    COUNT(DISTINCT order_id) AS orders,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    SUM(quantity) AS units_sold,
    ROUND(
        (SUM(profit) / SUM(sales)) * 100,
        2
    ) AS profit_margin_pct
FROM sales;


-- ============================================================
-- QUERY 2: MONTHLY SALES TREND
-- ============================================================

SELECT
    DATE_TRUNC('month', order_date)::DATE AS month,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    COUNT(DISTINCT order_id) AS orders
FROM sales
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;


-- ============================================================
-- QUERY 3: CATEGORY PERFORMANCE
-- ============================================================

SELECT
    category,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    SUM(quantity) AS units_sold,
    ROUND(
        (SUM(profit) / SUM(sales)) * 100,
        2
    ) AS profit_margin_pct
FROM sales
GROUP BY category
ORDER BY revenue DESC;


-- ============================================================
-- QUERY 4: TOP 10 PRODUCTS BY REVENUE
-- ============================================================

SELECT
    product_id,
    product_name,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    SUM(quantity) AS units_sold
FROM sales
GROUP BY
    product_id,
    product_name
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- QUERY 5: LOSS-MAKING PRODUCTS
-- ============================================================

SELECT
    product_id,
    product_name,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    SUM(quantity) AS units_sold
FROM sales
GROUP BY
    product_id,
    product_name
HAVING SUM(profit) < 0
ORDER BY profit ASC
LIMIT 10;


-- ============================================================
-- QUERY 6: INVENTORY OVERVIEW
-- ============================================================

SELECT
    stock_status,
    COUNT(*) AS inventory_records,
    SUM(closing_stock) AS total_closing_stock
FROM inventory
GROUP BY stock_status
ORDER BY inventory_records DESC;

-- ============================================================
-- QUERY 7: STOCK-OUT ANALYSIS
-- ============================================================

SELECT
    i.product_id,
    p.product_name,
    COUNT(*) AS stock_out_records
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
WHERE i.stock_out_flag = TRUE
GROUP BY
    i.product_id,
    p.product_name
ORDER BY stock_out_records DESC;

-- ============================================================
-- QUERY 8: SUPPLIER DELIVERY PERFORMANCE
-- ============================================================

SELECT
    s.supplier_id,
    s.supplier_name,
    COUNT(p.purchase_id) AS total_purchases,

    SUM(
        CASE
            WHEN p.delivery_status = 'Late'
            THEN 1
            ELSE 0
        END
    ) AS late_deliveries,

    ROUND(
        (
            SUM(
                CASE
                    WHEN p.delivery_status = 'Late'
                    THEN 1
                    ELSE 0
                END
            )::NUMERIC
            / COUNT(p.purchase_id)
        ) * 100,
        2
    ) AS late_delivery_pct

FROM purchases p

JOIN suppliers s
    ON p.supplier_id = s.supplier_id

GROUP BY
    s.supplier_id,
    s.supplier_name

ORDER BY late_delivery_pct DESC;


-- ============================================================
-- QUERY 9: PURCHASE SPENDING BY SUPPLIER
-- ============================================================

SELECT
    s.supplier_id,
    s.supplier_name,
    COUNT(p.purchase_id) AS purchase_orders,
    SUM(p.quantity) AS units_purchased,
    ROUND(SUM(p.purchase_value), 2) AS total_purchase_value
FROM purchases p
JOIN suppliers s
    ON p.supplier_id = s.supplier_id
GROUP BY
    s.supplier_id,
    s.supplier_name
ORDER BY total_purchase_value DESC;

-- ============================================================
-- QUERY 10: INVOICE STATUS
-- ============================================================

SELECT
    status,
    COUNT(*) AS invoice_count,
    ROUND(
        COUNT(*)::NUMERIC /
        SUM(COUNT(*)) OVER () * 100,
        2
    ) AS percentage
FROM invoices
GROUP BY status
ORDER BY invoice_count DESC;

-- ============================================================
-- QUERY 11: INVOICE PROCESSING TAT
-- ============================================================

SELECT
    ROUND(
        AVG(processing_tat_days),
        2
    ) AS average_tat_days,

    MIN(processing_tat_days) AS minimum_tat_days,

    MAX(processing_tat_days) AS maximum_tat_days
FROM invoices;

-- ============================================================
-- QUERY 12: SLA BREACH ANALYSIS
-- ============================================================

SELECT
    sla_breach,
    COUNT(*) AS invoice_count,
    ROUND(
        COUNT(*)::NUMERIC /
        SUM(COUNT(*)) OVER () * 100,
        2
    ) AS percentage
FROM invoices
GROUP BY sla_breach
ORDER BY sla_breach DESC;

-- ============================================================
-- QUERY 13: INVOICE DISCREPANCIES
-- ============================================================

SELECT
    COUNT(*) AS total_invoices,

    COUNT(
        CASE
            WHEN discrepancy_amount <> 0
            THEN 1
        END
    ) AS invoices_with_discrepancy,

    ROUND(
        SUM(absolute_discrepancy),
        2
    ) AS total_absolute_discrepancy

FROM invoices;

-- ============================================================
-- QUERY 14: SUPPLIER INVOICE PERFORMANCE
-- ============================================================

SELECT
    s.supplier_name,

    COUNT(i.invoice_id) AS total_invoices,

    ROUND(
        AVG(i.processing_tat_days),
        2
    ) AS avg_processing_tat,

    SUM(
        CASE
            WHEN i.sla_breach = TRUE
            THEN 1
            ELSE 0
        END
    ) AS sla_breaches,

    ROUND(
        SUM(
            CASE
                WHEN i.sla_breach = TRUE
                THEN 1
                ELSE 0
            END
        )::NUMERIC
        / COUNT(i.invoice_id) * 100,
        2
    ) AS sla_breach_pct

FROM invoices i

JOIN suppliers s
    ON i.supplier_id = s.supplier_id

GROUP BY
    s.supplier_id,
    s.supplier_name

ORDER BY sla_breach_pct DESC;


-- ============================================================
-- QUERY 15: EMPLOYEE PRODUCTIVITY
-- ============================================================

SELECT
    e.employee_id,
    e.employee_name,
    e.role,

    COUNT(i.invoice_id) AS invoices_processed,

    ROUND(
        AVG(i.processing_tat_days),
        2
    ) AS avg_processing_tat,

    SUM(
        CASE
            WHEN i.sla_breach = TRUE
            THEN 1
            ELSE 0
        END
    ) AS sla_breaches,

    ROUND(
        SUM(
            CASE
                WHEN i.sla_breach = TRUE
                THEN 1
                ELSE 0
            END
        )::NUMERIC
        / COUNT(i.invoice_id) * 100,
        2
    ) AS sla_breach_pct

FROM employees e

LEFT JOIN invoices i
    ON e.employee_id = i.assigned_employee

GROUP BY
    e.employee_id,
    e.employee_name,
    e.role

ORDER BY invoices_processed DESC;


-- ============================================================
-- QUERY 16: INVOICE AGING
-- ============================================================

SELECT
    CASE
        WHEN processing_tat_days <= 2
            THEN '0-2 Days'

        WHEN processing_tat_days <= 5
            THEN '3-5 Days'

        WHEN processing_tat_days <= 7
            THEN '6-7 Days'

        ELSE '8+ Days'
    END AS aging_bucket,

    COUNT(*) AS invoice_count

FROM invoices

GROUP BY
    CASE
        WHEN processing_tat_days <= 2
            THEN '0-2 Days'

        WHEN processing_tat_days <= 5
            THEN '3-5 Days'

        WHEN processing_tat_days <= 7
            THEN '6-7 Days'

        ELSE '8+ Days'
    END

ORDER BY
    MIN(processing_tat_days);