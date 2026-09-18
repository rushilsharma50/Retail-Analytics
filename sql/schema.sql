-- ============================================================
-- RETAIL DATABASE SCHEMA
-- ============================================================


-- ============================================================
-- 1. PRODUCTS
-- ============================================================

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name TEXT NOT NULL,
    category VARCHAR(100),
    sub_category VARCHAR(100)
);


-- ============================================================
-- 2. CUSTOMERS
-- ============================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name TEXT NOT NULL,
    segment VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code INTEGER,
    region VARCHAR(50)
);


-- ============================================================
-- 3. STORES
-- ============================================================

CREATE TABLE IF NOT EXISTS stores (
    store_id VARCHAR(20) PRIMARY KEY,
    store_name TEXT NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code INTEGER,
    region VARCHAR(50),
    store_type VARCHAR(50),
    opening_date DATE
);


-- ============================================================
-- 4. SUPPLIERS
-- ============================================================

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id VARCHAR(20) PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    category VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    payment_terms VARCHAR(50)
);


-- ============================================================
-- 5. EMPLOYEES
-- ============================================================

CREATE TABLE IF NOT EXISTS employees (
    employee_id VARCHAR(20) PRIMARY KEY,
    employee_name TEXT NOT NULL,
    role VARCHAR(100),
    store_id VARCHAR(20),
    department VARCHAR(100),

    CONSTRAINT fk_employee_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
);


-- ============================================================
-- 6. SALES
-- ============================================================

CREATE TABLE IF NOT EXISTS sales (
    row_id INTEGER PRIMARY KEY,
    order_id VARCHAR(50),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(50),
    customer_id VARCHAR(50),
    customer_name TEXT,
    segment VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code INTEGER,
    region VARCHAR(50),
    product_id VARCHAR(50),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    product_name TEXT,
    sales NUMERIC(12,2),
    quantity INTEGER,
    discount NUMERIC(5,2),
    profit NUMERIC(12,2),
    shipping_days INTEGER,
    year INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    quarter VARCHAR(10),

    CONSTRAINT fk_sales_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_sales_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- ============================================================
-- 7. INVENTORY
-- ============================================================

CREATE TABLE IF NOT EXISTS inventory (
    inventory_date DATE,
    store_id VARCHAR(20),
    product_id VARCHAR(50),
    opening_stock INTEGER,
    received_quantity INTEGER,
    sold_quantity INTEGER,
    damaged_quantity INTEGER,
    closing_stock INTEGER,
    stock_out_flag BOOLEAN,
    stock_status VARCHAR(50),

    PRIMARY KEY (
        inventory_date,
        store_id,
        product_id
    ),

    CONSTRAINT fk_inventory_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id),

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);


-- ============================================================
-- 8. PURCHASES
-- ============================================================

CREATE TABLE IF NOT EXISTS purchases (
    purchase_id VARCHAR(30) PRIMARY KEY,
    purchase_date DATE,
    store_id VARCHAR(20),
    supplier_id VARCHAR(20),
    product_id VARCHAR(50),
    quantity INTEGER,
    unit_cost NUMERIC(12,2),
    expected_delivery DATE,
    actual_delivery DATE,
    delivery_status VARCHAR(30),
    purchase_value NUMERIC(14,2),

    CONSTRAINT fk_purchase_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id),

    CONSTRAINT fk_purchase_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id),

    CONSTRAINT fk_purchase_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);


-- ============================================================
-- 9. INVOICES
-- ============================================================

CREATE TABLE IF NOT EXISTS invoices (
    invoice_id VARCHAR(30) PRIMARY KEY,
    supplier_id VARCHAR(20),
    store_id VARCHAR(20),
    invoice_date DATE,
    received_date DATE,
    processed_date DATE,
    invoice_amount NUMERIC(14,2),
    expected_amount NUMERIC(14,2),
    status VARCHAR(50),
    assigned_employee VARCHAR(20),
    processing_tat_days INTEGER,
    discrepancy_amount NUMERIC(14,2),
    absolute_discrepancy NUMERIC(14,2),
    sla_breach BOOLEAN,

    CONSTRAINT fk_invoice_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id),

    CONSTRAINT fk_invoice_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id),

    CONSTRAINT fk_invoice_employee
        FOREIGN KEY (assigned_employee)
        REFERENCES employees(employee_id)
);