import pandas as pd

file_path = "data/raw/Sample - Superstore.csv"

# Load dataset
df = pd.read_csv(file_path, encoding="cp1252")

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Calculate shipping duration
df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days


# ============================================================
# 1. OVERALL KPIs
# ============================================================

print("=" * 60)
print("OVERALL BUSINESS KPIs")
print("=" * 60)

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()
total_orders = df["Order ID"].nunique()

profit_margin = total_profit / total_sales * 100

print(f"Total Sales:      ${total_sales:,.2f}")
print(f"Total Profit:     ${total_profit:,.2f}")
print(f"Total Quantity:   {total_quantity:,}")
print(f"Total Orders:     {total_orders:,}")
print(f"Profit Margin:    {profit_margin:.2f}%")
print(f"Average Order:    ${total_sales / total_orders:,.2f}")


# ============================================================
# 2. CATEGORY PERFORMANCE
# ============================================================

print("\n" + "=" * 60)
print("CATEGORY PERFORMANCE")
print("=" * 60)

category_analysis = (
    df.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

category_analysis["Profit Margin %"] = (
    category_analysis["Profit"]
    / category_analysis["Sales"]
    * 100
)

print(
    category_analysis
    .sort_values("Sales", ascending=False)
    .to_string(index=False)
)


# ============================================================
# 3. SUB-CATEGORY PERFORMANCE
# ============================================================

print("\n" + "=" * 60)
print("SUB-CATEGORY PERFORMANCE")
print("=" * 60)

subcategory_analysis = (
    df.groupby("Sub-Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

subcategory_analysis["Profit Margin %"] = (
    subcategory_analysis["Profit"]
    / subcategory_analysis["Sales"]
    * 100
)

print(
    subcategory_analysis
    .sort_values("Profit", ascending=False)
    .to_string(index=False)
)


# ============================================================
# 4. REGIONAL PERFORMANCE
# ============================================================

print("\n" + "=" * 60)
print("REGIONAL PERFORMANCE")
print("=" * 60)

region_analysis = (
    df.groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

region_analysis["Profit Margin %"] = (
    region_analysis["Profit"]
    / region_analysis["Sales"]
    * 100
)

print(
    region_analysis
    .sort_values("Sales", ascending=False)
    .to_string(index=False)
)


# ============================================================
# 5. DISCOUNT ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("DISCOUNT ANALYSIS")
print("=" * 60)

discount_analysis = (
    df.groupby("Discount")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

discount_analysis["Profit Margin %"] = (
    discount_analysis["Profit"]
    / discount_analysis["Sales"]
    * 100
)

print(
    discount_analysis
    .sort_values("Discount")
    .to_string(index=False)
)


# ============================================================
# 6. TOP 10 PRODUCTS BY SALES
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 PRODUCTS BY SALES")
print("=" * 60)

top_products = (
    df.groupby(["Product ID", "Product Name"])
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Sales", ascending=False)
    .head(10)
)

print(top_products.to_string(index=False))


# ============================================================
# 7. TOP 10 PRODUCTS BY PROFIT
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 PRODUCTS BY PROFIT")
print("=" * 60)

top_profit_products = (
    df.groupby(["Product ID", "Product Name"])
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Profit", ascending=False)
    .head(10)
)

print(top_profit_products.to_string(index=False))


# ============================================================
# 8. TOP 10 LOSS-MAKING PRODUCTS
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 LOSS-MAKING PRODUCTS")
print("=" * 60)

loss_products = (
    df.groupby(["Product ID", "Product Name"])
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Profit", ascending=True)
    .head(10)
)

print(loss_products.to_string(index=False))


# ============================================================
# 9. YEARLY PERFORMANCE
# ============================================================

print("\n" + "=" * 60)
print("YEARLY PERFORMANCE")
print("=" * 60)

df["Year"] = df["Order Date"].dt.year

yearly_analysis = (
    df.groupby("Year")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

yearly_analysis["Profit Margin %"] = (
    yearly_analysis["Profit"]
    / yearly_analysis["Sales"]
    * 100
)

print(yearly_analysis.to_string(index=False))


# ============================================================
# 10. SHIPPING PERFORMANCE
# ============================================================

print("\n" + "=" * 60)
print("SHIPPING PERFORMANCE")
print("=" * 60)

shipping_analysis = (
    df.groupby("Shipping Days")
    .agg(
        Orders=("Order ID", "nunique"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

print(shipping_analysis.to_string(index=False))