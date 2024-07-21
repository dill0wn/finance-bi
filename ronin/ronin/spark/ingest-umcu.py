import os

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf


_NAME_ = 'ronin.spark.ingest-umcu'

SHARED_DATA_DIR = os.environ.get('SHARED_DATA_DIR')
SPARK_MASTER_HOST = os.environ.get('SPARK_MASTER_HOST')
SPARK_MASTER_PORT = os.environ.get('SPARK_MASTER_PORT')
SPARK_MASTER_URL = f'spark://{SPARK_MASTER_HOST}:{SPARK_MASTER_PORT}'

# SPARK_MASTER_URL = 'spark://172.18.0.2:7078'
SPARK_MASTER_URL = 'spark://spark_master.local:7078'

# Create a SparkConf object
conf = (SparkConf()
        .setAppName(_NAME_)
        # .setMaster(SPARK_MASTER_URL)
        # .set('spark.blockManager.port', '7068')
        )
ctx = SparkContext(conf=conf)

# Initialize Spark session
# spark = SparkSession.builder.config(conf=conf)
# spark = spark.getOrCreate()
spark = SparkSession(ctx)


# Read the CSV file
df = spark.read \
    .option("header", "true") \
    .csv(f"{SHARED_DATA_DIR}/transactions/TransactionHistory-05-10-2024-12-08-43.csv")

# Rename "description" to "raw description"
renamed_df = df.withColumnRenamed("Description", "Raw_Description")

# Remove "check number" and "balance"
reduced_df = renamed_df.drop("Check #", "Balance")

# Reorder columns, moving "note" to last
# Assuming "date", "raw description", "amount" are the columns you want first
reordered_df = reduced_df.select("Date", "Raw_Description", "Amount", "Note")

# Show the result for verification
reordered_df.show()
