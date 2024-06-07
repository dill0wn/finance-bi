import os
from typing import Iterable

from sqlalchemy import bindparam, create_engine, text, Column, Integer, MetaData, String, Date, Numeric, Engine, literal, literal_column
from sqlalchemy.types import SchemaType
from sqlalchemy.orm import declarative_base, sessionmaker, Session, scoped_session
import sqlalchemy.exc

import psycopg2

from ronin.utils.logging import getLogger


log = getLogger('ronin.model.db')


maker = sessionmaker(autoflush=True, autocommit=False)
DBSession: Session | scoped_session = scoped_session(maker)

ModelBase = declarative_base()

metadata: MetaData = ModelBase.metadata

# Define the connection string
db_user = os.environ.get("POSTGRES_USER")
db_password = os.environ.get("POSTGRES_PASSWORD")
db_port = int(os.environ.get("POSTGRES_PORT"))
db_host = os.environ.get("POSTGRES_HOST")
db_name = os.environ.get("POSTGRES_DB")

# db_string = f"postgresql://username:password@localhost:5432/mydatabase"
db_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def init_databases(**engine_kwargs) -> Engine:

    recreate = engine_kwargs.pop('recreate', False)

    engine = create_engine(db_string, **engine_kwargs)

    init_metabase(engine)
    init_models(engine, recreate=recreate)

    return engine


def ignore_sql_errors(*orig_types: Iterable[Exception]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except sqlalchemy.exc.StatementError as e:
                if not type(e.orig) in orig_types:
                    raise
        return wrapper
    return decorator


def init_metabase(engine: Engine):

    metabase_db = os.environ.get("METABASE_DB_DBNAME")
    metabase_user = os.environ.get("METABASE_DB_USER")
    metabase_pass = os.environ.get("METABASE_DB_PASS")
    
    @ignore_sql_errors(psycopg2.errors.DuplicateDatabase)
    def create_db():
        with engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            conn.execute(text(f"CREATE DATABASE {metabase_db}"))

    @ignore_sql_errors(psycopg2.errors.DuplicateObject)
    def create_user():
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text(f"CREATE USER {metabase_user} WITH PASSWORD :db_pass"), parameters=dict(db_pass=metabase_pass))

    def grant_user():
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text(f"GRANT ALL PRIVILEGES ON DATABASE {metabase_db} TO {metabase_user}"))
                conn.execute(text(f"ALTER DATABASE {metabase_db} OWNER TO {metabase_user}"))
    
    create_db()
    create_user()
    grant_user()
        
    log.info("Metabase database created")


def init_models(engine: Engine, recreate: bool = False):

    DBSession.remove()
    DBSession.configure(bind=engine)
    metadata.bind = engine

    if recreate:
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text("DROP TABLE IF EXISTS raw_transactions CASCADE"))

    ModelBase.metadata.create_all(engine, checkfirst=True)


class RawTransactions(ModelBase):
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


"""
from sqlalchemy.orm import synonym, relation, scoped_session, sessionmaker

# Global session manager: DBSession() returns the Thread-local
# session object appropriate for the current web request.
maker = sessionmaker(autoflush=True, autocommit=False)
DBSession: sqlalchemy.orm.session.Session | sqlalchemy.orm.scoping.scoped_session = scoped_session(maker)
zope_register(DBSession)

# Base class for all of our model classes: By default, the data model is
# defined with SQLAlchemy's declarative extension, but if you need more
# control, you can switch to the traditional method.
DeclarativeBase = declarative_base()

# There are two convenient ways for you to spare some typing.
# You can have a query property on all your model classes by doing this:
DeclarativeBase.query = DBSession.query_property()
# Or you can use a session-aware mapper as it was used in TurboGears 1:
# DeclarativeBase = declarative_base(mapper=DBSession.mapper)

# Global metadata.
# The default metadata is the one from the declarative base.
metadata = DeclarativeBase.metadata

# If you have multiple databases with overlapping table names, you'll need a
# metadata for each database. Feel free to rename 'metadata2'.
# metadata2 = MetaData()

def init_model(engine: Engine):
    '''Call me before using any of the tables or classes in the model.'''
    event.listen(engine, 'connect', on_db_connect_set_encoding)
    DBSession.remove()
    DBSession.configure(bind=engine)
    metadata.bind = engine

    
class User(DeclarativeBase, ModelMixin):

    '''
    User mapped to alexandria sql tables, for account registration
    '''
    __tablename__ = 'users'

    # { Columns

    user_id = Column(Integer, Sequence('users_pk_seq'), primary_key=True)
    user_name = Column(Text, unique=True, default='')
    _email = Column('email', Text, default='',
                    info={'rum': {'field': 'Email'}})
    _password = Column('user_pw', String(32), nullable=False,
                       info={'rum': {'field': 'Password'}})
    status = Column(String(1), default='A')
    _unix_password = Column('unix_pw', String(40), nullable=False)
    mail_siteupdates = Column(Integer, default=0)    
    
"""