import os

import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


df = pd.read_csv(os.getenv("WEATHER_DATA_FILE", "raw_weather_data.csv"))
df.columns = [col.upper() for col in df.columns]

connection_config = {
    "user": required_env("SNOWFLAKE_USER"),
    "account": required_env("SNOWFLAKE_ACCOUNT"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    "database": os.getenv("SNOWFLAKE_DATABASE", "MY_FIRST_PIPELINE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA", "RAW"),
}
connection_config["password"] = required_env("SNOWFLAKE_PASSWORD")
conn = snowflake.connector.connect(**connection_config)

try:
    print("Uploading data to Snowflake...")
    success, _, nrows, _ = write_pandas(conn, df, "RAW_WEATHER")
    if not success:
        raise RuntimeError("Snowflake upload failed.")
    print(f"Success! Loaded {nrows} rows into Snowflake.")
finally:
    conn.close()
