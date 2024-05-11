import os
import defopt
import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, Column, String, Date, Float
from sqlalchemy.dialects.postgresql import MONEY

# Define the connection string
db_user = os.environ.get("POSTGRES_USER")
db_password = os.environ.get("POSTGRES_PASSWORD")
db_port = os.environ.get("PG_PORT")
db_host = os.environ.get("PG_HOST")
db_name = os.environ.get("POSTGRES_DB")

# db_string = f"postgresql://username:password@localhost:5432/mydatabase"
db_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def generate_sql_create_table(df, table_name):
    type_mapping = {
        'int64': 'INTEGER',
        'float64': 'REAL',
        'datetime64[ns]': 'TIMESTAMP',
        'object': 'TEXT',
    }

    fields = []
    for column, dtype in df.dtypes.items():
        sql_type = type_mapping.get(str(dtype), 'TEXT')
        fields.append(f"{column} {sql_type}")

    fields_str = ",\n".join(fields)
    sql_create_table = f"CREATE TABLE {table_name} (\n{fields_str}\n);"

    return sql_create_table

def execute(*, csv_file: str = None):
    
    # Create the database engine
    engine = create_engine(db_string)

    # Define the metadata
    metadata = MetaData()

    # Define the table
    transactions = Table('transactions', metadata,
        Column('Account', String),
        Column('Date', Date),
        Column('Description', String),
        Column('Note', String),
        Column('Check_Number', String),
        Column('Amount', MONEY),
        Column('Balance', MONEY),
    )

    # Create the table
    metadata.create_all(engine)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Write the data from the DataFrame to the table
    # df.to_sql('transactions', engine, if_exists='append', index=False)


if __name__ == '__main__':
    defopt.run(execute)