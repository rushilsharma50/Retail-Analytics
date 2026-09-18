import pandas as pd
import psycopg2
from pathlib import Path
from io import StringIO


# ============================================================
# SETTINGS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "processed"

DB_NAME = "retail"
DB_USER = "postgres"
DB_PASSWORD = input("Enter PostgreSQL password: ")
DB_HOST = "localhost"
DB_PORT = "5432"


# ============================================================
# FILE → TABLE MAPPING
# ============================================================

files = {
    "products.csv": "products",
    "customers.csv": "customers",
    "stores.csv": "stores",
    "suppliers.csv": "suppliers",
    "employees.csv": "employees",
    "sales_clean.csv": "sales",
    "inventory.csv": "inventory",
    "purchases.csv": "purchases",
    "invoices.csv": "invoices"
}


# ============================================================
# CONNECT TO POSTGRESQL
# ============================================================

print("=" * 60)
print("CONNECTING TO POSTGRESQL")
print("=" * 60)

connection = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cursor = connection.cursor()

print("Connected successfully!")
print(f"Database: {DB_NAME}")


# ============================================================
# LOAD TABLES
# ============================================================

print("\n" + "=" * 60)
print("LOADING DATA")
print("=" * 60)


for filename, table_name in files.items():

    file_path = DATA_DIR / filename

    print(f"\nLoading {filename} → {table_name}")

    # --------------------------------------------------------
    # Read CSV
    # --------------------------------------------------------

    df = pd.read_csv(file_path)

    print(f"Rows found: {len(df):,}")

    # --------------------------------------------------------
    # Convert NaN to None
    # --------------------------------------------------------

    df = df.where(pd.notnull(df), None)

    # --------------------------------------------------------
    # Convert dataframe to CSV in memory
    # --------------------------------------------------------

    csv_buffer = StringIO()

    df.to_csv(
        csv_buffer,
        index=False,
        header=False
    )

    csv_buffer.seek(0)

    # --------------------------------------------------------
    # Get column names from dataframe
    # --------------------------------------------------------

    columns = list(df.columns)

    column_string = ", ".join(
        f'"{column}"'
        for column in columns
    )

    # --------------------------------------------------------
    # Clear existing data
    # --------------------------------------------------------

    cursor.execute(
        f'TRUNCATE TABLE "{table_name}" CASCADE;'
    )

    # --------------------------------------------------------
    # COPY data into PostgreSQL
    # --------------------------------------------------------

    copy_sql = f"""
        COPY "{table_name}" ({column_string})
        FROM STDIN
        WITH CSV
    """

    cursor.copy_expert(
        copy_sql,
        csv_buffer
    )

    connection.commit()

    print(
        f"Loaded successfully: "
        f"{len(df):,} rows"
    )


# ============================================================
# CLOSE CONNECTION
# ============================================================

cursor.close()
connection.close()


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("ALL DATA LOADED SUCCESSFULLY")
print("=" * 60)

print("PostgreSQL database:", DB_NAME)
print("Tables loaded:", len(files))