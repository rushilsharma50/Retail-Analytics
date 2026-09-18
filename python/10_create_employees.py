import pandas as pd
import random
from pathlib import Path


# ============================================================
# SETTINGS
# ============================================================

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

stores_file = BASE_DIR / "data" / "processed" / "stores.csv"
output_file = BASE_DIR / "data" / "processed" / "employees.csv"


# ============================================================
# LOAD STORES
# ============================================================

stores = pd.read_csv(stores_file)

print("=" * 60)
print("CREATING EMPLOYEE DATA")
print("=" * 60)

print(f"Stores loaded: {len(stores):,}")


# ============================================================
# EMPLOYEE SETTINGS
# ============================================================

first_names = [
    "Aarav",
    "Vihaan",
    "Aditya",
    "Arjun",
    "Rohan",
    "Rahul",
    "Karan",
    "Vivek",
    "Amit",
    "Raj",
    "Neha",
    "Priya",
    "Ananya",
    "Isha",
    "Kavya",
    "Sneha",
    "Pooja",
    "Riya",
    "Meera",
    "Aisha"
]

last_names = [
    "Shah",
    "Patel",
    "Mehta",
    "Desai",
    "Joshi",
    "Sharma",
    "Verma",
    "Gupta",
    "Kapoor",
    "Malhotra"
]

roles = [
    "Invoice Analyst",
    "Invoice Analyst",
    "Invoice Analyst",
    "Senior Invoice Analyst",
    "Operations Analyst"
]

departments = [
    "Finance Operations",
    "Finance Operations",
    "Accounts Payable",
    "Retail Operations"
]


# ============================================================
# CREATE EMPLOYEES
# ============================================================

employees = []

number_of_employees = 30

for i in range(1, number_of_employees + 1):

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    employee_name = f"{first_name} {last_name}"

    store_id = random.choice(
        stores["store_id"].tolist()
    )

    role = random.choice(roles)

    department = random.choice(departments)

    employees.append({
        "employee_id": f"EMP{i:03d}",
        "employee_name": employee_name,
        "role": role,
        "store_id": store_id,
        "department": department
    })


employees_df = pd.DataFrame(employees)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("VALIDATION")
print("=" * 60)

print(
    f"Employees created: "
    f"{len(employees_df):,}"
)

print(
    f"Duplicate employee IDs: "
    f"{employees_df['employee_id'].duplicated().sum()}"
)

print(
    f"Missing values: "
    f"{employees_df.isnull().sum().sum()}"
)

print("\nRole distribution:")

print(
    employees_df["role"]
    .value_counts()
)

print("\nDepartment distribution:")

print(
    employees_df["department"]
    .value_counts()
)


# ============================================================
# SAVE
# ============================================================

output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

employees_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("EMPLOYEE DATA SAVED")
print("=" * 60)

print(output_file)

print("\nPreview:")

print(
    employees_df.head(10)
    .to_string(index=False)
)