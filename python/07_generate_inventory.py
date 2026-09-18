import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# RETAIL360 - SYNTHETIC INVENTORY GENERATION
# ============================================================

sales_file = Path("data/processed/sales_clean.csv")
stores_file = Path("data/processed/stores.csv")

output_file = Path("data/processed/inventory.csv")


print("=" * 60)
print("RETAIL360 - INVENTORY GENERATION")
print("=" * 60)


# ============================================================
# 1. LOAD DATA
# ============================================================

sales = pd.read_csv(sales_file)
stores = pd.read_csv(stores_file)

sales["order_date"] = pd.to_datetime(sales["order_date"])

print(f"\nSales records: {len(sales):,}")
print(f"Stores: {len(stores):,}")


# ============================================================
# 2. MAP SALES TO STORES
# ============================================================

print("\nMapping sales to stores...")

sales = sales.merge(
    stores[
        [
            "store_id",
            "city",
            "state",
            "postal_code"
        ]
    ],
    on=["city", "state", "postal_code"],
    how="left"
)

print(
    f"Sales without store mapping: "
    f"{sales['store_id'].isna().sum()}"
)


# ============================================================
# 3. CREATE MONTHLY DEMAND
# ============================================================

print("\nCalculating monthly demand...")

sales["inventory_month"] = (
    sales["order_date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

monthly_sales = (
    sales.groupby(
        [
            "inventory_month",
            "store_id",
            "product_id"
        ]
    )
    .agg(
        demand_quantity=("quantity", "sum")
    )
    .reset_index()
)


# ============================================================
# 4. MONTH RANGE
# ============================================================

start_date = sales["inventory_month"].min()
end_date = sales["inventory_month"].max()

months = pd.date_range(
    start=start_date,
    end=end_date,
    freq="MS"
)

print(
    f"Inventory period: "
    f"{start_date.date()} → {end_date.date()}"
)

print(f"Months: {len(months)}")


# ============================================================
# 5. ACTIVE STORE-PRODUCT COMBINATIONS
# ============================================================

active_pairs = (
    sales[
        [
            "store_id",
            "product_id"
        ]
    ]
    .drop_duplicates()
    .reset_index(drop=True)
)

print(
    f"Active store-product combinations: "
    f"{len(active_pairs):,}"
)


# ============================================================
# 6. CREATE DEMAND LOOKUP
# ============================================================

demand_lookup = {
    (
        row.store_id,
        row.product_id,
        row.inventory_month
    ): row.demand_quantity
    for row in monthly_sales.itertuples()
}


# ============================================================
# 7. AVERAGE DEMAND LOOKUP
# ============================================================

average_demand_lookup = (
    monthly_sales
    .groupby(
        [
            "store_id",
            "product_id"
        ]
    )["demand_quantity"]
    .mean()
    .to_dict()
)


# ============================================================
# 8. GENERATE INVENTORY
# ============================================================

print("\nGenerating inventory records...")

records = []

rng = np.random.default_rng(42)


for pair in active_pairs.itertuples(index=False):

    store_id = pair.store_id
    product_id = pair.product_id

    average_demand = average_demand_lookup.get(
        (store_id, product_id),
        0
    )

    # --------------------------------------------------------
    # Products with extremely low demand
    # --------------------------------------------------------

    if average_demand <= 0:

        opening_stock = 0

    else:

        # Keep initial stock around 1–2 months of demand
        opening_stock = max(
            1,
            int(
                average_demand
                * rng.uniform(0.8, 1.8)
            )
        )


    # ========================================================
    # MONTHLY INVENTORY
    # ========================================================

    for month in months:

        demand = demand_lookup.get(
            (
                store_id,
                product_id,
                month
            ),
            0
        )


        # ----------------------------------------------------
        # Target stock
        # ----------------------------------------------------

        if average_demand > 0:

            target_stock = max(
                2,
                int(
                    average_demand
                    * rng.uniform(1.0, 2.0)
                )
            )

        else:

            target_stock = 0


        # ----------------------------------------------------
        # Reorder only when stock is below target
        # ----------------------------------------------------

        required_replenishment = max(
            0,
            target_stock - opening_stock
        )


        # ----------------------------------------------------
        # Supplier/replenishment variation
        # ----------------------------------------------------

        if required_replenishment > 0:

            # 12% chance of partial replenishment
            if rng.random() < 0.12:

                received_quantity = int(
                    required_replenishment
                    * rng.uniform(0.20, 0.70)
                )

            else:

                received_quantity = required_replenishment

        else:

            received_quantity = 0


        # ----------------------------------------------------
        # Damaged stock
        # ----------------------------------------------------

        damaged_quantity = int(
            rng.binomial(
                received_quantity,
                0.01
            )
        )


        # ----------------------------------------------------
        # Available inventory
        # ----------------------------------------------------

        available_stock = (
            opening_stock
            + received_quantity
            - damaged_quantity
        )


        # ----------------------------------------------------
        # Fulfilled sales
        # ----------------------------------------------------

        sold_quantity = min(
            demand,
            available_stock
        )


        # ----------------------------------------------------
        # Closing inventory
        # ----------------------------------------------------

        closing_stock = (
            available_stock
            - sold_quantity
        )


        # ----------------------------------------------------
        # Stock-out event
        # ----------------------------------------------------

        stock_out_flag = (
            demand > available_stock
        )


        # ----------------------------------------------------
        # Record
        # ----------------------------------------------------

        records.append(
            {
                "inventory_date": month,
                "store_id": store_id,
                "product_id": product_id,
                "opening_stock": opening_stock,
                "received_quantity": received_quantity,
                "sold_quantity": sold_quantity,
                "demand_quantity": demand,
                "damaged_quantity": damaged_quantity,
                "closing_stock": closing_stock,
                "stock_out_flag": stock_out_flag
            }
        )


        # Next month's opening stock
        opening_stock = closing_stock


# ============================================================
# 9. CREATE DATAFRAME
# ============================================================

inventory = pd.DataFrame(records)


# ============================================================
# 10. CALCULATE STOCK STATUS
# ============================================================

def determine_status(row):

    average_demand = average_demand_lookup.get(
        (
            row["store_id"],
            row["product_id"]
        ),
        0
    )

    closing_stock = row["closing_stock"]

    # No meaningful demand
    if average_demand == 0:

        return "No Demand"

    # Stock completely unavailable
    if closing_stock == 0:

        return "Out of Stock"

    # Less than half a month's typical demand
    if closing_stock < average_demand * 0.5:

        return "Low Stock"

    # More than 3 months of typical demand
    if closing_stock > average_demand * 3:

        return "Overstock"

    return "Healthy"


inventory["stock_status"] = inventory.apply(
    determine_status,
    axis=1
)


# ============================================================
# 11. VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("INVENTORY VALIDATION")
print("=" * 60)

print(
    f"Inventory rows: "
    f"{len(inventory):,}"
)

print(
    f"Duplicate records: "
    f"{inventory.duplicated(
        subset=[
            "inventory_date",
            "store_id",
            "product_id"
        ]
    ).sum()}"
)

print(
    f"Missing values: "
    f"{inventory.isnull().sum().sum()}"
)

print(
    f"Negative closing stock: "
    f"{(inventory['closing_stock'] < 0).sum()}"
)


# ============================================================
# 12. STOCK STATUS
# ============================================================

print("\n" + "=" * 60)
print("STOCK STATUS")
print("=" * 60)

print(
    inventory["stock_status"]
    .value_counts()
)


# ============================================================
# 13. STOCK-OUT EVENTS
# ============================================================

print("\n" + "=" * 60)
print("STOCK-OUT ANALYSIS")
print("=" * 60)

print(
    inventory["stock_out_flag"]
    .value_counts()
)

stock_out_rate = (
    inventory["stock_out_flag"].mean()
    * 100
)

print(
    f"\nStock-out rate: "
    f"{stock_out_rate:.2f}%"
)


# ============================================================
# 14. INVENTORY SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("INVENTORY SUMMARY")
print("=" * 60)

print(
    f"Average closing stock: "
    f"{inventory['closing_stock'].mean():.2f}"
)

print(
    f"Total units received: "
    f"{inventory['received_quantity'].sum():,}"
)

print(
    f"Total units sold: "
    f"{inventory['sold_quantity'].sum():,}"
)

print(
    f"Total damaged units: "
    f"{inventory['damaged_quantity'].sum():,}"
)


# ============================================================
# 15. SAVE
# ============================================================

output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

inventory.to_csv(
    output_file,
    index=False
)

print(
    f"\nSaved to: {output_file}"
)


# ============================================================
# 16. PREVIEW
# ============================================================

print("\n" + "=" * 60)
print("INVENTORY PREVIEW")
print("=" * 60)

print(
    inventory.head(10)
    .to_string(index=False)
)


print("\n" + "=" * 60)
print("INVENTORY GENERATION COMPLETE")
print("=" * 60)