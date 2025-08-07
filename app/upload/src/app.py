from datetime import datetime
import os
import pandas as pd
import psycopg2
import time
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine

from scraper import download_csv

# get directory of this file
DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables
load_dotenv()

def get_db_connection():
    '''Create database connection'''
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        port=os.getenv('POSTGRES_PORT', '5432'),
        database=os.getenv('POSTGRES_DB', 'currency_tracker'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'password')
    )

def get_db_engine():
    '''Create database engine'''
    usr = os.getenv('POSTGRES_USER', 'postgres')
    pwd = os.getenv('POSTGRES_PASSWORD', 'password')
    host = os.getenv('POSTGRES_HOST', 'postgres')
    port = os.getenv('POSTGRES_PORT', '5432')
    db = os.getenv('POSTGRES_DB', 'currency_tracker')
    return create_engine(
        f'postgresql://{usr}:{pwd}@{host}:{port}/{db}'
    )

def test_connection():
    '''Test PostgreSQL connection'''
    for _ in range(10):
        try:
            conn = get_db_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('SELECT version();')
                version = cur.fetchone()
                print(f'Connected to PostgreSQL: {version['version']}')
                
                # Test table access
                cur.execute('SELECT COUNT(*) FROM conversion_rates;')
                count = cur.fetchone()
                print(f'Found {count['count']} records in conversion_rates table')
                
            conn.close()
            return True
        except psycopg2.OperationalError as e:
            print("Database not ready, retrying...")
            time.sleep(3)
    print(f'Database connection failed: {e}')
    return False

def get_last_update_per_currency(query_file) -> pd.DataFrame:
    '''Get the latest dates for each currency'''
    with open(query_file, 'r') as f:
        query = f.read()
    # loads to a dataframe with currency code and latest date
    df = pd.read_sql_query(query, get_db_connection())
    df['latest_date'] = pd.to_datetime(df['latest_date'])
    return df

def get_latest_rates(csv_file) -> pd.DataFrame:
    '''Load the latest rates into the database

    Load the raw datafile downloaded from the ECB website. Original data is in
    wide format and contains all history since EUR was founded.

    Args:
        csv_file: path to the csv file

    Returns a dataframe with columns:
    - conversion_date: date of the conversion rate
    - currency_code: currency code
    - conversion_rate: conversion rate
    '''
    df = pd.read_csv(csv_file)
    df = df.rename(columns={'Date': 'conversion_date'})
    df_long = df.melt(id_vars=['conversion_date'], var_name='currency_code',
                      value_name='conversion_rate')
    df_long['conversion_date'] = pd.to_datetime(df_long['conversion_date'])
    # limit rate to 4 decimal places
    df_long['conversion_rate'] = df_long['conversion_rate']\
        .astype(float)\
        .round(4)
    # drop instances where conversion_rate is NaN
    df_long = df_long[~df_long['conversion_rate'].isna()]
    return df_long

def get_missing_dates(last_update_per_currency, latest_rates_df) -> pd.DataFrame:
    '''Get the missing dates for each currency'''
    # get earliest date in last_update_per_currency
    earliest_date = last_update_per_currency['latest_date'].min()
    # check if earliest_date is NaT
    if pd.isna(earliest_date):
        earliest_date = datetime.strptime('1970-01-01', '%Y-%m-%d')
    # limit latest_rates_df to dates after earliest_date
    # this avoids expensive join with entire conversion rate history
    latest_rates_df_lim = latest_rates_df[
        latest_rates_df['conversion_date'] > earliest_date]
    # merge the two dataframes on currency code and conversion date
    merged = pd.merge(
        last_update_per_currency, latest_rates_df_lim, on='currency_code',
        how='outer', suffixes=('_last_update', '_latest'))
    # fill in latest_date with past date in case of new currency code
    merged['latest_date'] = merged['latest_date']\
        .fillna(datetime.strptime('1970-01-01', '%Y-%m-%d'))
    # get entries where latest file date is after latest update date
    missing_dates = merged[merged['conversion_date'] > merged['latest_date']]
    # reformat columns
    missing_dates = missing_dates[
        ['conversion_date', 'currency_code', 'conversion_rate']]
    return missing_dates

def insert_missing_dates(missing_dates, eng):
    '''Insert the missing dates into the database'''
    # insert missing dates using pandas
    nrows = missing_dates.to_sql('conversion_rates', eng, if_exists='append', index=False)
    print(f'Inserted {nrows} rows')

def main():

    download_csv()
    last_update_per_currency = get_last_update_per_currency(
        os.path.join(DIR, 'last_update_per_currency.sql'))
    latest_rates = get_latest_rates(
        os.path.join(DIR, 'data', 'eurofxref-hist.csv'))
    missing_dates = get_missing_dates(last_update_per_currency, latest_rates)
    test_connection() 
    insert_missing_dates(missing_dates, get_db_engine())

if __name__ == '__main__':
    main()