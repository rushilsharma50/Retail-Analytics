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

purchases_file = BASE_DIR / "data" / "processed" / "purchases.csv"
employees_file = BASE_DIR / "data" / "processed" / "employees.csv"

output_file = BASE_DIR / "data" / "processed" / "invoices.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("GENERATING INVOICE DATA")
print("=" * 60)

purchases = pd.read_csv(purchases_file)
employees = pd.read_csv(employees_file)

purchases["purchase_date"] = pd.to_datetime(
    purchases["purchase_date"]
)

print(f"Purchases loaded:  {len(purchases):,}")
print(f"Employees loaded:  {len(employees):,}")


# ============================================================
# CREATE INVOICES FROM PURCHASES
# ============================================================

invoices = []

for i, purchase in purchases.iterrows():

    purchase_date = purchase["purchase_date"]

    purchase_value = (
        purchase["quantity"] *
        purchase["unit_cost"]
    )

    # --------------------------------------------------------
    # RECEIVED DATE
    # --------------------------------------------------------

    received_date = (
        purchase_date +
        timedelta(days=random.randint(3, 8))
    )

    # --------------------------------------------------------
    # EXPECTED AMOUNT
    # --------------------------------------------------------

    expected_amount = purchase_value

    # --------------------------------------------------------
    # INVOICE AMOUNT
    # --------------------------------------------------------
    # Most invoices match the expected purchase value.
    # Some contain small discrepancies.

    discrepancy_probability = random.random()

    if discrepancy_probability < 0.10:

        # 10% invoices have discrepancies
        discrepancy_percentage = random.uniform(
            -0.08,
            0.08
        )

        invoice_amount = (
            expected_amount *
            (1 + discrepancy_percentage)
        )

    else:

        invoice_amount = expected_amount

    invoice_amount = round(invoice_amount, 2)

    # --------------------------------------------------------
    # PROCESSING TIME
    # --------------------------------------------------------

    processing_probability = random.random()

    if processing_probability < 0.65:

        # Normal processing: 1–3 days
        processing_days = random.randint(1, 3)

    elif processing_probability < 0.90:

        # Slightly delayed: 4–6 days
        processing_days = random.randint(4, 6)

    else:

        # Significant delay: 7–12 days
        processing_days = random.randint(7, 12)

    processed_date = (
        received_date +
        timedelta(days=processing_days)
    )

    # --------------------------------------------------------
    # INVOICE STATUS
    # --------------------------------------------------------

    if processing_days >= 7:

        status = "Pending / Delayed"

    elif processing_days >= 4:

        status = "Processed Late"

    else:

        status = "Processed"

    # --------------------------------------------------------
    # ASSIGN EMPLOYEE
    # --------------------------------------------------------

    employee = employees.sample(
        n=1,
        random_state=i
    ).iloc[0]

    employee_id = employee["employee_id"]

    # --------------------------------------------------------
    # INVOICE RECORD
    # --------------------------------------------------------

    invoices.append({

        "invoice_id":
            f"INV{i + 1:06d}",

        "supplier_id":
            purchase["supplier_id"],

        "store_id":
            purchase["store_id"],

        "invoice_date":
            purchase_date,

        "received_date":
            received_date,

        "processed_date":
            processed_date,

        "invoice_amount":
            invoice_amount,

        "expected_amount":
            round(expected_amount, 2),

        "status":
            status,

        "assigned_employee":
            employee_id
    })


# ============================================================
# CREATE DATAFRAME
# ============================================================

invoices_df = pd.DataFrame(invoices)


# ============================================================
# CALCULATED FIELDS
# ============================================================

invoices_df["invoice_date"] = pd.to_datetime(
    invoices_df["invoice_date"]
)

invoices_df["received_date"] = pd.to_datetime(
    invoices_df["received_date"]
)

invoices_df["processed_date"] = pd.to_datetime(
    invoices_df["processed_date"]
)

# Processing TAT
invoices_df["processing_tat_days"] = (
    invoices_df["processed_date"] -
    invoices_df["received_date"]
).dt.days

# Invoice discrepancy
invoices_df["discrepancy_amount"] = (
    invoices_df["invoice_amount"] -
    invoices_df["expected_amount"]
).round(2)

# Absolute discrepancy
invoices_df["absolute_discrepancy"] = (
    invoices_df["discrepancy_amount"]
    .abs()
    .round(2)
)

# SLA breach
invoices_df["sla_breach"] = (
    invoices_df["processing_tat_days"] > 3
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("INVOICE DATA VALIDATION")
print("=" * 60)

print(
    f"Invoices created: "
    f"{len(invoices_df):,}"
)

print(
    f"Duplicate invoice IDs: "
    f"{invoices_df['invoice_id'].duplicated().sum()}"
)

print(
    f"Missing values: "
    f"{invoices_df.isnull().sum().sum()}"
)

print(
    f"Invalid TAT values: "
    f"{(invoices_df['processing_tat_days'] < 0).sum()}"
)


# ============================================================
# STATUS ANALYSIS
# ============================================================

print("\nInvoice status:")

print(
    invoices_df["status"]
    .value_counts()
)


# ============================================================
# SLA ANALYSIS
# ============================================================

print("\nSLA analysis:")

print(
    f"SLA breaches: "
    f"{invoices_df['sla_breach'].sum():,}"
)

sla_rate = (
    invoices_df["sla_breach"].mean() * 100
)

print(
    f"SLA breach rate: "
    f"{sla_rate:.2f}%"
)


# ============================================================
# TAT ANALYSIS
# ============================================================

print("\nProcessing TAT:")

print(
    f"Average TAT: "
    f"{invoices_df['processing_tat_days'].mean():.2f} days"
)

print(
    f"Maximum TAT: "
    f"{invoices_df['processing_tat_days'].max()} days"
)


# ============================================================
# DISCREPANCY ANALYSIS
# ============================================================

print("\nInvoice discrepancies:")

discrepancy_count = (
    (invoices_df["discrepancy_amount"] != 0)
    .sum()
)

print(
    f"Invoices with discrepancy: "
    f"{discrepancy_count:,}"
)

print(
    f"Total discrepancy amount: "
    f"${invoices_df['discrepancy_amount'].sum():,.2f}"
)

print(
    f"Absolute discrepancy amount: "
    f"${invoices_df['absolute_discrepancy'].sum():,.2f}"
)


# ============================================================
# DATE RANGE
# ============================================================

print("\nInvoice date range:")

print(
    invoices_df["invoice_date"].min(),
    "→",
    invoices_df["invoice_date"].max()
)


# ============================================================
# SAVE
# ============================================================

output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

invoices_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("INVOICE DATA SAVED")
print("=" * 60)

print(output_file)

print("\nPreview:")

print(
    invoices_df.head(10)
    .to_string(index=False)
)