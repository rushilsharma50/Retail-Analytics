import pandas as pd
from pathlib import Path


# ============================================================
# 1. FILE PATHS
# ============================================================

input_file = Path("data/raw/Sample - Superstore.csv")
output_file = Path("data/processed/sales_clean.csv")


# ============================================================
# 2. LOAD RAW DATA
# ============================================================

print("=" * 60)
print("RETAIL360 - SALES DATA CLEANING")
print("=" * 60)

print("\nLoading raw dataset...")

df = pd.read_csv(input_file, encoding="cp1252")

print(f"Raw rows: {len(df):,}")
print(f"Raw columns: {len(df.columns)}")


# ============================================================
# 3. RENAME COLUMNS
# ============================================================

print("\nRenaming columns...")

column_mapping = {
    "Row ID": "row_id",
    "Order ID": "order_id",
    "Order Date": "order_date",
    "Ship Date": "ship_date",
    "Ship Mode": "ship_mode",
    "Customer ID": "customer_id",
    "Customer Name": "customer_name",
    "Segment": "segment",
    "Country": "country",
    "City": "city",
    "State": "state",
    "Postal Code": "postal_code",
    "Region": "region",
    "Product ID": "product_id",
    "Category": "category",
    "Sub-Category": "sub_category",
    "Product Name": "product_name",
    "Sales": "sales",
    "Quantity": "quantity",
    "Discount": "discount",
    "Profit": "profit"
}

df = df.rename(columns=column_mapping)


# ============================================================
# 4. CONVERT DATA TYPES
# ============================================================

print("Converting data types...")

df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])

df["row_id"] = df["row_id"].astype(int)
df["postal_code"] = df["postal_code"].astype(int)

df["sales"] = df["sales"].astype(float)
df["quantity"] = df["quantity"].astype(int)
df["discount"] = df["discount"].astype(float)
df["profit"] = df["profit"].astype(float)


# ============================================================
# 5. CREATE DERIVED COLUMNS
# ============================================================

print("Creating derived columns...")

# Number of days between order and shipment
df["shipping_days"] = (
    df["ship_date"] - df["order_date"]
).dt.days

# Year
df["year"] = df["order_date"].dt.year

# Month number
df["month"] = df["order_date"].dt.month

# Month name
df["month_name"] = df["order_date"].dt.month_name()

# Quarter
df["quarter"] = "Q" + df["order_date"].dt.quarter.astype(str)


# ============================================================
# 6. REMOVE UNNECESSARY COLUMN
# ============================================================

print("Removing unnecessary columns...")

# Country contains only one value in this dataset.
# It does not provide useful analytical variation.
df = df.drop(columns=["country"])


# ============================================================
# 7. REORDER COLUMNS
# ============================================================

column_order = [
    "row_id",
    "order_id",
    "order_date",
    "ship_date",
    "shipping_days",
    "ship_mode",

    "customer_id",
    "customer_name",
    "segment",

    "city",
    "state",
    "postal_code",
    "region",

    "product_id",
    "category",
    "sub_category",
    "product_name",

    "sales",
    "quantity",
    "discount",
    "profit",

    "year",
    "month",
    "month_name",
    "quarter"
]

df = df[column_order]


# ============================================================
# 8. DATA QUALITY VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL DATA VALIDATION")
print("=" * 60)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print(f"Duplicate rows: {df.duplicated().sum()}")
print(f"Missing values: {df.isnull().sum().sum()}")

print(
    f"Invalid shipping days: "
    f"{(df['shipping_days'] < 0).sum()}"
)

print(
    f"Invalid quantity: "
    f"{(df['quantity'] <= 0).sum()}"
)

print(
    f"Invalid discount: "
    f"{((df['discount'] < 0) | (df['discount'] > 1)).sum()}"
)


# ============================================================
# 9. SAVE CLEAN DATA
# ============================================================

print("\nSaving cleaned dataset...")

output_file.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_file, index=False)

print(f"Saved to: {output_file}")


# ============================================================
# 10. PREVIEW
# ============================================================

print("\n" + "=" * 60)
print("CLEAN DATA PREVIEW")
print("=" * 60)

print(df.head().to_string(index=False))

print("\n" + "=" * 60)
print("CLEANING COMPLETE")
print("=" * 60)