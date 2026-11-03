
import pandas as pd
from pathlib import Path

# Project data directories
RAW_DIR = Path("data/raw")
DIRTY_DIR = Path("data/dirty")
MARKETING_DIR = RAW_DIR / "marketing_campaigns1"


def inspect_file(file_path):
    print("\n" + "=" * 65)
    print(f"FILE: {file_path.name}")
    print("=" * 65)

    # Read according to file format
    if file_path.suffix.lower() == ".parquet":
        df = pd.read_parquet(file_path)
    elif file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path)
    else:
        print("Unsupported file format.")
        return

    # Basic information
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Column names: {list(df.columns)}")

    # Data types
    print("\nDATA TYPES:")
    print(df.dtypes)

    # Missing values
    print("\nMISSING VALUES:")
    print(df.isnull().sum())

    # Duplicate rows
    print(f"\nDuplicate rows: {df.duplicated().sum():,}")

    # Sample records
    print("\nFIRST 5 RECORDS:")
    print(df.head())


# Existing CSV datasets
csv_files = [
    RAW_DIR / "campaigns.csv",
    RAW_DIR / "conversions.csv",
    RAW_DIR / "daily_performance.csv",
    DIRTY_DIR / "campaigns_dirty.csv",
    DIRTY_DIR / "conversions_dirty.csv",
    DIRTY_DIR / "daily_performance_dirty.csv",
]

# New Parquet datasets
parquet_files = list(MARKETING_DIR.glob("*.parquet"))

# Inspect existing CSV files
for file in csv_files:
    if file.exists():
        inspect_file(file)
    else:
        print(f"\nFile not found: {file}")

# Inspect new Parquet files
for file in parquet_files:
    inspect_file(file)
