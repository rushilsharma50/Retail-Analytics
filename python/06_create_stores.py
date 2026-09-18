import pandas as pd
from pathlib import Path


# ============================================================
# RETAIL360 - CREATE STORE DIMENSION
# ============================================================

input_file = Path("data/processed/sales_clean.csv")
output_file = Path("data/processed/stores.csv")


print("=" * 60)
print("RETAIL360 - CREATE STORE DIMENSION")
print("=" * 60)


# ============================================================
# 1. LOAD CLEAN SALES DATA
# ============================================================

df = pd.read_csv(input_file)

print(f"\nLoaded sales records: {len(df):,}")


# ============================================================
# 2. FIND UNIQUE LOCATIONS
# ============================================================

locations = (
    df[
        [
            "city",
            "state",
            "postal_code",
            "region"
        ]
    ]
    .drop_duplicates()
    .sort_values(["state", "city"])
    .reset_index(drop=True)
)


# ============================================================
# 3. CREATE STORE IDs
# ============================================================

locations.insert(
    0,
    "store_id",
    [
        f"ST{i:03d}"
        for i in range(1, len(locations) + 1)
    ]
)


# ============================================================
# 4. CREATE STORE NAMES
# ============================================================

locations["store_name"] = (
    locations["city"]
    + " "
    + locations["region"]
    + " Store "
    + locations["store_id"]
)


# ============================================================
# 5. ASSIGN STORE TYPE
# ============================================================

# Store type is simulated because the source dataset
# does not contain actual store types.

def assign_store_type(index):
    if index % 10 == 0:
        return "Flagship"
    elif index % 3 == 0:
        return "Large"
    else:
        return "Standard"


locations["store_type"] = [
    assign_store_type(i)
    for i in range(len(locations))
]


# ============================================================
# 6. CREATE OPENING DATE
# ============================================================

# Synthetic opening dates.
# We keep them before the sales period so all stores
# can participate in the simulated operational model.

locations["opening_date"] = pd.to_datetime("2013-01-01")


# ============================================================
# 7. REORDER COLUMNS
# ============================================================

stores = locations[
    [
        "store_id",
        "store_name",
        "city",
        "state",
        "postal_code",
        "region",
        "store_type",
        "opening_date"
    ]
]


# ============================================================
# 8. VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STORE VALIDATION")
print("=" * 60)

print(f"Stores created: {len(stores):,}")

print(
    f"Duplicate store IDs: "
    f"{stores['store_id'].duplicated().sum()}"
)

print(
    f"Duplicate city/state combinations: "
    f"{stores[['city', 'state', 'postal_code']].duplicated().sum()}"
)

print(
    f"Missing values: "
    f"{stores.isnull().sum().sum()}"
)


# ============================================================
# 9. REGION DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("STORES BY REGION")
print("=" * 60)

print(stores["region"].value_counts())


# ============================================================
# 10. SAVE
# ============================================================

output_file.parent.mkdir(parents=True, exist_ok=True)

stores.to_csv(output_file, index=False)

print(f"\nSaved to: {output_file}")


# ============================================================
# 11. PREVIEW
# ============================================================

print("\n" + "=" * 60)
print("STORE PREVIEW")
print("=" * 60)

print(stores.head(10).to_string(index=False))


print("\n" + "=" * 60)
print("STORE DIMENSION CREATION COMPLETE")
print("=" * 60)