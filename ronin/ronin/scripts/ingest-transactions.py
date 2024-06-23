import os
import re

import defopt
import pandas as pd
from psycopg2 import OperationalError
from sqlalchemy.dialects.postgresql import MONEY

from ronin.model.db import init_databases
from ronin.lib.logging import getLogger

log = getLogger('ronin.scripts.ingest_transactions')


CURRENCY_RE = re.compile('[^0-9\.-]')
def currency_converter(value):
    amount = float(CURRENCY_RE.sub('', value))
    if amount is not None and value.startswith('('):
        return -amount
    return amount


def build_converters():
    return {
        'Account': str,                 # "VISA PLATINUM CASH REWARDS, $93.00 pmt due 05/27/24",
        'Date': pd.to_datetime,         # 5/9/2024,
        'Description': str,             # "Purchase RYLEE'S ACE HARDWARE GRAND RAPIDS MI Date 05/08/24 24431064130091903001276 5251 %% Card 52 #6301 MEMO Balance Change -$12.71",
        'Note': str,                    # "",
        'Check #': str,                 # "",
        'Amount': currency_converter,   # ($12.71),
        'Balance': currency_converter,  # "$5,295.00",
    }


def read_csv(csv_file: str) -> pd.DataFrame:

    df_csv_params = dict(
        na_filter=False,
        thousands=',',
        parse_dates=True,
        date_format='%m/%d/%Y',
        converters=build_converters(),
    )

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file, **df_csv_params)
    df = df.rename({'Check #': 'Check_Number'}, axis="columns")
    df = df.rename(str.lower, axis="columns")

    return df


def execute(*,
            csv_file: str,
            csv_source: str,
            recreate: bool = True,
            verbose: bool = False):

    df = read_csv(csv_file)

    df['source'] = csv_source
    
    # Create the database engine
    engine_kwargs = dict(
        recreate=recreate,
    )
    if verbose:
        engine_kwargs['echo'] = 'debug'

    engine = init_databases(**engine_kwargs)

    # Write the data from the DataFrame to the table
    df.to_sql('raw_transactions', engine, if_exists='append', index=False)


if __name__ == '__main__':
    log.info("Starting...")
    defopt.run(execute)