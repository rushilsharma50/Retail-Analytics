import pandas as pd
import random
from pathlib import Path

# ============================================================
# SETTINGS
# ============================================================

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

products_file = BASE_DIR / "data" / "processed" / "products.csv"
output_file = BASE_DIR / "data" / "processed" / "suppliers.csv"


# ============================================================
# LOAD PRODUCTS
# ============================================================

products = pd.read_csv(products_file)

print("=" * 60)
print("CREATING SUPPLIERS")
print("=" * 60)

print(f"Products loaded: {len(products):,}")


# ============================================================
# SUPPLIER MASTER DATA
# ============================================================

supplier_names = [
    "TechSource Distributors",
    "Prime Office Supplies",
    "Global Retail Solutions",
    "Metro Wholesale",
    "Apex Business Products",
    "SmartTrade Suppliers",
    "NorthStar Distribution",
    "Reliable Retail Supply",
    "Vertex Wholesale",
    "United Business Supplies",
    "BlueLine Distributors",
    "Capital Office Products",
    "ProSource Trading",
    "Evergreen Supplies",
    "Pioneer Distribution"
]

cities = [
    ("New York", "New York"),
    ("Los Angeles", "California"),
    ("Chicago", "Illinois"),
    ("Houston", "Texas"),
    ("Phoenix", "Arizona"),
    ("Philadelphia", "Pennsylvania"),
    ("Dallas", "Texas"),
    ("San Jose", "California"),
    ("Austin", "Texas"),
    ("Seattle", "Washington"),
    ("Boston", "Massachusetts"),
    ("Denver", "Colorado"),
    ("Atlanta", "Georgia"),
    ("Miami", "Florida"),
    ("Detroit", "Michigan")
]

payment_terms = [
    "Net 15",
    "Net 30",
    "Net 45",
    "Net 60"
]


# ============================================================
# CREATE SUPPLIERS
# ============================================================

suppliers = []

categories = products["category"].dropna().unique().tolist()

for i, supplier_name in enumerate(supplier_names, start=1):

    city, state = cities[i - 1]

    # Assign suppliers to one or more product categories
    category = random.choice(categories)

    suppliers.append({
        "supplier_id": f"SUP{i:03d}",
        "supplier_name": supplier_name,
        "category": category,
        "city": city,
        "state": state,
        "payment_terms": random.choice(payment_terms)
    })


suppliers_df = pd.DataFrame(suppliers)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("VALIDATION")
print("=" * 60)

print(f"Suppliers created: {len(suppliers_df):,}")

print(
    f"Duplicate supplier IDs: "
    f"{suppliers_df['supplier_id'].duplicated().sum()}"
)

print(
    f"Missing values: "
    f"{suppliers_df.isnull().sum().sum()}"
)

print("\nCategory distribution:")
print(suppliers_df["category"].value_counts())


# ============================================================
# SAVE
# ============================================================

output_file.parent.mkdir(parents=True, exist_ok=True)

suppliers_df.to_csv(output_file, index=False)

print("\n" + "=" * 60)
print("SUPPLIERS SAVED")
print("=" * 60)

print(output_file)

print("\nPreview:")
print(suppliers_df.head())