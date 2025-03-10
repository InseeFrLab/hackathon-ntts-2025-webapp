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

# Construct full S3 path
path_name="projet-hackathon-ntts-2025/indicators/indic_predictions.parquet"

# Open the file using s3fs and read it with pandas
with fs.open(path_name, "rb") as f:
    df = pd.read_parquet(f)


# Sorting the DataFrame by NUTS3
df = df.sort_values(by="NUTS3")

buf_bytes = dataframe_to_parquet_bytes(df)

# Write the bytes to standard output
sys.stdout.buffer.write(buf_bytes)