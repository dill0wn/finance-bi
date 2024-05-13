from sqlalchemy import Column, Integer, MetaData, String, Date, Numeric, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import MONEY

Base = declarative_base()

class RawTransactions(Base):
    __tablename__ = 'raw_transactions'

    id = Column(Integer, index=True, primary_key=True)
    source = Column(String)
    account = Column(String)
    date = Column(Date)
    description = Column(String)
    note = Column(String)
    check_number = Column(String)
    amount = Column(Numeric)  # Assuming MONEY is a numeric type
    balance = Column(Numeric)  # Assuming MONEY is a numeric type


def build_tables_orm(engine):
    Base.metadata.create_all(engine, checkfirst=False)


class TablesHolder:
    # from configure_alexandria_tables()
    RawTransactions: Table

tables = TablesHolder()


def build_tables_core(engine):
    metadata = MetaData()

    # Define the table
    tables.RawTransactions = Table('raw_transactions', metadata,
        Column('id', Integer, index=True, primary_key=True),
        Column('source', String),
        Column('account', String),
        Column('date', Date),
        Column('description', String),
        Column('note', String),
        Column('check_number', String),
        Column('amount', MONEY),
        Column('balance', MONEY),
    )

    # Create the table
    metadata.create_all(engine, checkfirst=False)



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