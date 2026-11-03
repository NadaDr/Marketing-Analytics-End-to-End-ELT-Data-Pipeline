
import os
from pathlib import Path

import pandas as pd
import snowflake.connector

from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data" / "raw" / "marketing_campaigns1"

load_dotenv(PROJECT_DIR / ".env", override=True)

DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SCHEMA = "RAW"


# --------------------------------------------------
# 2. DATASET CONFIGURATION
# --------------------------------------------------

TABLE_NAME = "RAW_MC_CONVERSIONS"
FILENAME = "conversions.parquet"

COLUMNS = """
    CONVERSION_ID NUMBER(10,0),
    AD_GROUP_ID NUMBER(10,0),
    FIRST_TOUCH_CHANNEL_ID NUMBER(10,0),
    LAST_TOUCH_CHANNEL_ID NUMBER(10,0),
    CONVERTED_AT TIMESTAMP_NTZ(6),
    REVENUE NUMBER(12,2),
    TOUCH_COUNT NUMBER(10,0),
    DEVICE VARCHAR
"""


# --------------------------------------------------
# 3. CHECK SOURCE FILE
# --------------------------------------------------

file_path = DATA_DIR / FILENAME

if not file_path.exists():
    raise FileNotFoundError(f"Dataset not found: {file_path}")


# --------------------------------------------------
# 4. READ AND PREPARE DATA
# --------------------------------------------------

print(f"Reading {FILENAME}...")

df = pd.read_parquet(file_path)

# Standardize column names
df.columns = df.columns.str.upper()

# Convert timestamp to a formatted string
# This avoids incorrect microsecond timestamp interpretation
df["CONVERTED_AT"] = (
    pd.to_datetime(df["CONVERTED_AT"])
    .dt.strftime("%Y-%m-%d %H:%M:%S.%f")
)

print(f"Records found: {len(df):,}")

print("\nTimestamp sample:")
print(df["CONVERTED_AT"].head())


# --------------------------------------------------
# 5. CONNECT TO SNOWFLAKE
# --------------------------------------------------

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=DATABASE,
    schema=SCHEMA,
    role=os.getenv("SNOWFLAKE_ROLE")
)

print("\nConnected to Snowflake successfully!")


# --------------------------------------------------
# 6. CREATE TABLE AND RELOAD CONVERSIONS
# --------------------------------------------------

try:
    cursor = conn.cursor()

    # Create table if it does not exist
    create_sql = f"""
        CREATE TABLE IF NOT EXISTS
        {DATABASE}.{SCHEMA}.{TABLE_NAME}
        ({COLUMNS})
    """

    cursor.execute(create_sql)

    # Remove previous incorrect records
    print("\nTruncating old conversion records...")

    cursor.execute(
        f"TRUNCATE TABLE {DATABASE}.{SCHEMA}.{TABLE_NAME}"
    )

    # Upload corrected data
    print("\nUploading corrected conversion data...")

    success, nchunks, nrows, output = write_pandas(
        conn,
        df,
        TABLE_NAME,
        database=DATABASE,
        schema=SCHEMA,
        quote_identifiers=False
    )

    if not success:
        raise RuntimeError(
            f"Loading failed for {TABLE_NAME}: {output}"
        )

    print(f"\nSuccessfully loaded {nrows:,} rows!")
    print(f"Number of chunks: {nchunks}")

    # Verify timestamps directly in Snowflake
    cursor.execute(f"""
        SELECT
            MIN(CONVERTED_AT),
            MAX(CONVERTED_AT),
            COUNT(*)
        FROM {DATABASE}.{SCHEMA}.{TABLE_NAME}
    """)

    result = cursor.fetchone()

    print("\nSNOWFLAKE VERIFICATION:")
    print(f"Minimum timestamp: {result[0]}")
    print(f"Maximum timestamp: {result[1]}")
    print(f"Total rows: {result[2]:,}")

finally:
    conn.close()
    print("\nSnowflake connection closed.")
