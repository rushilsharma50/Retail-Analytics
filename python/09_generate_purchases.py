import pandas as pd
import numpy as np
import random
from pathlib import Path
from datetime import timedelta


# ============================================================
# SETTINGS
# ============================================================

random.seed(42)
np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

sales_file = BASE_DIR / "data" / "processed" / "sales_clean.csv"
products_file = BASE_DIR / "data" / "processed" / "products.csv"
stores_file = BASE_DIR / "data" / "processed" / "stores.csv"
suppliers_file = BASE_DIR / "data" / "processed" / "suppliers.csv"

output_file = BASE_DIR / "data" / "processed" / "purchases.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("GENERATING PURCHASE DATA")
print("=" * 60)

sales = pd.read_csv(sales_file)
products = pd.read_csv(products_file)
stores = pd.read_csv(stores_file)
suppliers = pd.read_csv(suppliers_file)

sales["order_date"] = pd.to_datetime(sales["order_date"])

print(f"Sales records:     {len(sales):,}")
print(f"Products:          {len(products):,}")
print(f"Stores:            {len(stores):,}")
print(f"Suppliers:         {len(suppliers):,}")


# ============================================================
# ESTIMATE PRODUCT COST
# ============================================================

print("\nCalculating estimated product costs...")

# Original Superstore does not provide a direct cost column.
# We estimate cost as:
#
# Cost = Sales - Profit

sales["estimated_cost"] = sales["sales"] - sales["profit"]

product_cost = (
    sales.groupby("product_id")
    .agg(
        total_cost=("estimated_cost", "sum"),
        total_quantity=("quantity", "sum")
    )
    .reset_index()
)

product_cost["unit_cost"] = (
    product_cost["total_cost"] /
    product_cost["total_quantity"]
)

# Prevent invalid zero/negative purchase costs
product_cost["unit_cost"] = product_cost["unit_cost"].clip(lower=0.01)

print(f"Product costs calculated: {len(product_cost):,}")


# ============================================================
# PRODUCT DEMAND
# ============================================================

product_demand = (
    sales.groupby("product_id")["quantity"]
    .sum()
    .reset_index(name="total_sold")
)

# Products with higher historical sales get a higher
# probability of appearing in purchase records.

product_demand["purchase_probability"] = (
    product_demand["total_sold"] /
    product_demand["total_sold"].sum()
)


# ============================================================
# SUPPLIERS
# ============================================================

supplier_ids = suppliers["supplier_id"].tolist()

store_ids = stores["store_id"].tolist()


# ============================================================
# GENERATE PURCHASES
# ============================================================

purchases = []

purchase_id = 1

start_date = sales["order_date"].min()
end_date = sales["order_date"].max()

current_date = start_date


while current_date <= end_date:

    # Create purchase activity twice every month
    if current_date.day in [5, 20]:

        # Select up to 80 products
        selected_products = product_demand.sample(
            n=min(80, len(product_demand)),
            weights="purchase_probability",
            random_state=purchase_id
        )

        for _, product_row in selected_products.iterrows():

            product_id = product_row["product_id"]

            # Find estimated product cost
            cost_row = product_cost[
                product_cost["product_id"] == product_id
            ]

            if cost_row.empty:
                continue

            unit_cost = float(
                cost_row["unit_cost"].iloc[0]
            )

            # Purchase quantity
            quantity = random.randint(2, 20)

            # Introduce realistic supplier price variation
            unit_cost = unit_cost * random.uniform(0.90, 1.10)

            # Assign supplier
            supplier_id = random.choice(supplier_ids)

            # Assign store
            store_id = random.choice(store_ids)

            # Expected delivery
            expected_delivery = (
                current_date +
                timedelta(days=random.randint(3, 7))
            )

            # Actual delivery
            delivery_delay = random.randint(-1, 5)

            actual_delivery = (
                expected_delivery +
                timedelta(days=delivery_delay)
            )

            # Delivery status
            if actual_delivery < expected_delivery:
                delivery_status = "Early"

            elif actual_delivery == expected_delivery:
                delivery_status = "On Time"

            else:
                delivery_status = "Late"

            purchases.append({
                "purchase_id": f"PUR{purchase_id:06d}",
                "purchase_date": current_date,
                "store_id": store_id,
                "supplier_id": supplier_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_cost": round(unit_cost, 2),
                "expected_delivery": expected_delivery,
                "actual_delivery": actual_delivery,
                "delivery_status": delivery_status
            })

            purchase_id += 1

    current_date += timedelta(days=1)


# ============================================================
# CREATE DATAFRAME
# ============================================================

purchases_df = pd.DataFrame(purchases)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("PURCHASE DATA VALIDATION")
print("=" * 60)

print(f"Purchase records: {len(purchases_df):,}")

print(
    f"Duplicate purchase IDs: "
    f"{purchases_df['purchase_id'].duplicated().sum()}"
)

print(
    f"Missing values: "
    f"{purchases_df.isnull().sum().sum()}"
)

print(
    f"Negative quantities: "
    f"{(purchases_df['quantity'] <= 0).sum()}"
)

print(
    f"Negative unit costs: "
    f"{(purchases_df['unit_cost'] < 0).sum()}"
)


# ============================================================
# DELIVERY ANALYSIS
# ============================================================

print("\nDelivery status:")
print(
    purchases_df["delivery_status"]
    .value_counts()
)


# ============================================================
# DATE RANGE
# ============================================================

print("\nPurchase date range:")

print(
    purchases_df["purchase_date"].min(),
    "→",
    purchases_df["purchase_date"].max()
)


# ============================================================
# PURCHASE VALUE
# ============================================================

purchases_df["purchase_value"] = (
    purchases_df["quantity"] *
    purchases_df["unit_cost"]
)

print(
    f"\nTotal purchase value: "
    f"${purchases_df['purchase_value'].sum():,.2f}"
)


# ============================================================
# SAVE
# ============================================================

output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

purchases_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("PURCHASE DATA SAVED")
print("=" * 60)

print(output_file)

print("\nPreview:")

print(
    purchases_df.head(10).to_string(index=False)
)