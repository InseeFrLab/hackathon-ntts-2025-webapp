import sys
from utils.wrappers import dataframe_to_parquet_bytes
import s3fs
import os
import pandas as pd

# Initialize S3 filesystem connection
fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": f"https://{os.environ['AWS_S3_ENDPOINT']}"},
    key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

# List to store DataFrames for each year

path="projet-hackathon-ntts-2025/indicators/indicateurs_departements.parquet"
data = pd.read_parquet(path, filesystem=fs)

# Sorting the DataFrame by NUTS3
data = data.sort_values(by="NUTS3")

buf_bytes = dataframe_to_parquet_bytes(data)

# Write the bytes to standard output
sys.stdout.buffer.write(buf_bytes)