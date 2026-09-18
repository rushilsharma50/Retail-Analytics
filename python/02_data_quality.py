import pandas as pd

file_path = "data/raw/Sample - Superstore.csv"

# Load dataset
df = pd.read_csv(file_path, encoding="cp1252")

print("=" * 60)
print("DATA QUALITY CHECK")
print("=" * 60)

# --------------------------------------------------
# 1. Duplicate rows
# --------------------------------------------------

print("\n" + "=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)

duplicates = df.duplicated().sum()

print(f"Duplicate rows: {duplicates}")


# --------------------------------------------------
# 2. Unique values
# --------------------------------------------------

print("\n" + "=" * 60)
print("UNIQUE VALUES")
print("=" * 60)

columns_to_check = [
    "Order ID",
    "Customer ID",
    "Product ID",
    "Category",
    "Sub-Category",
    "Region",
    "Ship Mode",
    "Segment"
]

for column in columns_to_check:
    print(f"{column}: {df[column].nunique()} unique values")


# --------------------------------------------------
# 3. Date conversion
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATE RANGE")
print("=" * 60)

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

print(f"Order date: {df['Order Date'].min()} → {df['Order Date'].max()}")
print(f"Ship date:  {df['Ship Date'].min()} → {df['Ship Date'].max()}")


# --------------------------------------------------
# 4. Negative / zero values
# --------------------------------------------------

print("\n" + "=" * 60)
print("VALUE VALIDATION")
print("=" * 60)

print(f"Sales <= 0: {(df['Sales'] <= 0).sum()}")
print(f"Quantity <= 0: {(df['Quantity'] <= 0).sum()}")
print(f"Discount < 0: {(df['Discount'] < 0).sum()}")
print(f"Discount > 1: {(df['Discount'] > 1).sum()}")


# --------------------------------------------------
# 5. Shipping delay
# --------------------------------------------------

print("\n" + "=" * 60)
print("SHIPPING ANALYSIS")
print("=" * 60)

df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print(f"Minimum shipping days: {df['Shipping Days'].min()}")
print(f"Maximum shipping days: {df['Shipping Days'].max()}")
print(f"Average shipping days: {df['Shipping Days'].mean():.2f}")


# --------------------------------------------------
# 6. Category distribution
# --------------------------------------------------

print("\n" + "=" * 60)
print("CATEGORY DISTRIBUTION")
print("=" * 60)

print(df["Category"].value_counts())


# --------------------------------------------------
# 7. Region distribution
# --------------------------------------------------

print("\n" + "=" * 60)
print("REGION DISTRIBUTION")
print("=" * 60)

print(df["Region"].value_counts())


# --------------------------------------------------
# 8. Profitability
# --------------------------------------------------

print("\n" + "=" * 60)
print("PROFITABILITY")
print("=" * 60)

print(f"Total Sales:  ${df['Sales'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")

negative_profit = (df["Profit"] < 0).sum()

print(f"Loss-making transactions: {negative_profit}")