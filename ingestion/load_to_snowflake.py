
import os
import pandas as pd
import snowflake.connector

from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

# 1. Load credentials from .env
load_dotenv(override=True)

# 2. Connect to Snowflake
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE")
)

print("Connected to Snowflake successfully!")

# 3. Define our CSV files and destination tables
datasets = {
    "campaigns_dirty.csv": "RAW_CAMPAIGNS",
    "conversions_dirty.csv": "RAW_CONVERSIONS",
    "daily_performance_dirty.csv": "RAW_DAILY_PERFORMANCE"
}

try:
    for filename, table_name in datasets.items():

        file_path = os.path.join("data", "dirty", filename)

        # Read CSV using Pandas
        df = pd.read_csv(file_path, dtype=str)

        # Match Snowflake column names
        df.columns = df.columns.str.upper()

        print(f"\nLoading {filename}...")
        print("Records found:", len(df))

        # Clear previous data so rerunning doesn't duplicate records
        cursor = conn.cursor()
        cursor.execute(
            f"TRUNCATE TABLE {table_name}"
        )
        cursor.close()

        # Upload DataFrame to Snowflake
        success, nchunks, nrows, output = write_pandas(
            conn,
            df,
            table_name,
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema="RAW",
            quote_identifiers=False
        )

        if success:
            print(f"Successfully loaded {nrows} rows into {table_name}")
        else:
            raise RuntimeError(f"Loading failed for {table_name}: {output}")

    print("\nAll datasets loaded successfully!")

finally:
    conn.close()
    print("Snowflake connection closed.")
