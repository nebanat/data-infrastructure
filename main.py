from time import time
import argparse
from os import system, getenv, path

import pandas as pd
from sqlalchemy import create_engine

DB_USER = getenv('POSTGRES_USER')
DB_PASSWORD = getenv('POSTGRES_PASSWORD')
DB_NAME = getenv('POSTGRES_DB')
DATA_URL = getenv('DATA_URL')
OUTPUT_FILE = getenv('OUTPUT_FILE')

def main():
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@pgdatabase:5432/{DB_NAME}')
    # download file from url if file does not exist
    if not path.exists(OUTPUT_FILE):
        print('Downloading data...')
        system(f"wget -O {OUTPUT_FILE} {DATA_URL}")
        print("done downloading file")

    df = pd.read_parquet(OUTPUT_FILE)

    # df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    print("inserting records ...")
    df.head(n=0).to_sql(DB_NAME, engine, if_exists='replace')
  
    df = df.iloc[0:20000]
    df.to_sql(DB_NAME, engine, if_exists='append')
    print("Done inserting records ..")
    # print(df.head())


if __name__ == "__main__":
    main()
