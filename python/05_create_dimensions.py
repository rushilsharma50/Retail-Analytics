import pandas as pd
from pathlib import Path


# ============================================================
# RETAIL360 - CREATE DIMENSION TABLES
# ============================================================

input_file = Path("data/processed/sales_clean.csv")

products_file = Path("data/processed/products.csv")
customers_file = Path("data/processed/customers.csv")


print("=" * 60)
print("RETAIL360 - CREATE DIMENSION TABLES")
print("=" * 60)


# ============================================================
# 1. LOAD CLEAN SALES DATA
# ============================================================

df = pd.read_csv(input_file)

print(f"\nLoaded sales records: {len(df):,}")


# ============================================================
# 2. CREATE PRODUCT DIMENSION
# ============================================================

print("\nCreating products table...")

products = (
    df[
        [
            "product_id",
            "product_name",
            "category",
            "sub_category"
        ]
    ]
    .drop_duplicates(subset=["product_id"])
    .sort_values("product_id")
    .reset_index(drop=True)
)

products.to_csv(products_file, index=False)

print(f"Products: {len(products):,}")
print(f"Saved: {products_file}")


# ============================================================
# 3. CREATE CUSTOMER DIMENSION
# ============================================================

print("\nCreating customers table...")

customers = (
    df[
        [
            "customer_id",
            "customer_name",
            "segment",
            "city",
            "state",
            "postal_code",
            "region"
        ]
    ]
    .drop_duplicates(subset=["customer_id"])
    .sort_values("customer_id")
    .reset_index(drop=True)
)

customers.to_csv(customers_file, index=False)

print(f"Customers: {len(customers):,}")
print(f"Saved: {customers_file}")


# ============================================================
# 4. VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("DIMENSION VALIDATION")
print("=" * 60)

print(f"\nProduct duplicate IDs: {products['product_id'].duplicated().sum()}")
print(f"Customer duplicate IDs: {customers['customer_id'].duplicated().sum()}")

print(
    f"Product missing values: "
    f"{products.isnull().sum().sum()}"
)

print(
    f"Customer missing values: "
    f"{customers.isnull().sum().sum()}"
)


# ============================================================
# 5. PREVIEW
# ============================================================

print("\n" + "=" * 60)
print("PRODUCTS PREVIEW")
print("=" * 60)

print(products.head().to_string(index=False))


print("\n" + "=" * 60)
print("CUSTOMERS PREVIEW")
print("=" * 60)

print(customers.head().to_string(index=False))


print("\n" + "=" * 60)
print("DIMENSION CREATION COMPLETE")
print("=" * 60)