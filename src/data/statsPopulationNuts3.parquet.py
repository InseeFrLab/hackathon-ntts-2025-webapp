import pandas as pd
import s3fs
import os
import sys
from utils.wrappers import dataframe_to_parquet_bytes


# Initialize S3 filesystem connection
fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": f"https://{os.environ['AWS_S3_ENDPOINT']}"},
    key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

file_path = "s3://projet-hackathon-ntts-2025/indicators/estat_demo_r_pjanaggr3.tsv.gz"

with fs.open(file_path, 'rb') as f:
    df = pd.read_csv(f, sep="\t", compression="gzip", dtype=str)

df[['freq', 'unit', 'sex', 'age', 'geo']] = df.iloc[:, 0].str.split(",", expand=True)
df = df.drop(columns=df.columns[0])
cols = ['freq', 'unit', 'sex', 'age', 'geo'] + list(df.columns[:-5])  # Les années en dernier
df = df[cols]

df.replace(': ', 0, inplace=True)

df = df[(df['sex'] == 'T') & (df['age'] == 'TOTAL')]
df = df.drop(columns=['freq', 'unit', 'sex', 'age', '1990 ', '1991 ', '1992 ', '1993 ',
       '1994 ', '1995 ', '1996 ', '1997 ', '1998 ', '1999 ', '2000 ', '2001 ',
       '2002 ', '2003 ', '2004 ', '2005 ', '2006 ', '2007 ', '2008 ', '2009 ',
       '2010 ', '2011 ', '2012 ', '2013 ', '2014 ', '2015 ', '2016 ', '2017 '])


def extract_number(value):
    if isinstance(value, str):
        num = "".join(c for c in value if c.isdigit())
        return int(num) if num else None
    return value


years = ['2018 ', '2019 ', '2020 ', '2021 ', '2022 ', '2023 ', '2024 ']
for year in years:
    df[year] = df[year].apply(extract_number)
    df[year].astype("Int64")

new_columns = ['nuts_id', 'population_2018', 'population_2019', 'population_2020', 'population_2021', 'population_2022', 'population_2023', 'population_2024']
df.columns = new_columns

df_nuts3 = df[df['nuts_id'].str.len() == 5]

# Sélectionner uniquement les colonnes 'nuts_id' et 'population_2021'
df = df_nuts3[['nuts_id', 'population_2021']].copy()

# Renommer la colonne 'nuts_id' en 'NUTS3'
df.rename(columns={'nuts_id': 'NUTS3'}, inplace=True)



# Construct full S3 path
path_name="projet-hackathon-ntts-2025/indicators/indic_predictions.parquet"

# Open the file using s3fs and read it with pandas
with fs.open(path_name, "rb") as f:
    df_prop = pd.read_parquet(f)


# Sorting the DataFrame by NUTS3
df_prop = df_prop.sort_values(by="NUTS3")

df = df_prop.merge(df, on="NUTS3", how="left")

buf_bytes = dataframe_to_parquet_bytes(df)
sys.stdout.buffer.write(buf_bytes)
