import pandas as pd

file_path = "data/raw/Sample - Superstore.csv"

# Load dataset
df = pd.read_csv(file_path, encoding="cp1252")

print("=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\n" + "=" * 60)
print("COLUMN NAMES")
print("=" * 60)

for column in df.columns:
    print(f"- {column}")

print("\n" + "=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)

print(df.head().to_string(index=False))

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)

print(df.dtypes)

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

print(df.isnull().sum())