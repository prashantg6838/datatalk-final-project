#Import libraries
from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql.functions import regexp_replace
from pyspark.sql.functions import col
from pyspark.sql.functions import col, mean, when
import argparse


#Define parameters to pass for the main script
#Initiate parser
parser = argparse.ArgumentParser(description='Parameters for main script')

#Define arguments
parser.add_argument('--GcsBucket_name', type=str, help='GCS bucket name that will be used to store raw data/as a staging area.', required=True)
parser.add_argument('--dataset_url', type=str, help='Dataset path.', required=True)
parser.add_argument('--bq_dataset_name', type=str, help='Dataset in BQ to store table.', required=True)
parser.add_argument('--bq_table_name', type=str, help='Table name to store output from Spark.', required=True)

#Capture arguments as variables
args = parser.parse_args()
GcsBucket_name = args.GcsBucket_name
dataset_url = args.dataset_url
bq_dataset_name = args.bq_dataset_name
bq_table_name = args.bq_table_name

#Initialize spark session
spark = SparkSession.builder \
  .appName('DE ZC App')\
  .config('spark.jars', 'gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar') \
  .getOrCreate()

#Configure temporary bucket
spark.conf.set('temporaryGcsBucket', GcsBucket_name)

#Set Schema for dataframes
gp_schema = types.StructType([
    types.StructField('App_Name', types.StringType(), True), 
    types.StructField('App_Id', types.StringType(), True), 
    types.StructField('Category', types.StringType(), True), 
    types.StructField('Rating', types.FloatType(), True), 
    types.StructField('Rating_Count', types.LongType(), True), 
    types.StructField('Installs', types.LongType(), True), 
    types.StructField('Minimum_Installs', types.LongType(), True), 
    types.StructField('Maximum_Installs', types.LongType(), True), 
    types.StructField('Free', types.BooleanType(), True), 
    types.StructField('Price', types.DoubleType(), True), 
    types.StructField('Currency', types.StringType(), True), 
    types.StructField('Size', types.DoubleType(), True), 
    types.StructField('Minimum_Android', types.StringType(), True), 
    types.StructField('Developer_Id', types.StringType(), True), 
    types.StructField('Developer_Website', types.StringType(), True), 
    types.StructField('Developer_Email', types.StringType(), True), 
    types.StructField('Released', types.DateType(), True), 
    types.StructField('Last_Updated', types.DateType(), True), 
    types.StructField('Content_Rating', types.StringType(), True), 
    types.StructField('Privacy_Policy', types.StringType(), True), 
    types.StructField('Ad_Supported', types.BooleanType(), True), 
    types.StructField('In_App_Purchases', types.BooleanType(), True), 
    types.StructField('Editors_Choice', types.BooleanType(), True), 
    types.StructField('Scraped_Time', types.TimestampType(), True)
])

#Read raw data
df = spark.read.option('header','true').schema(gp_schema).csv('gs://' + GcsBucket_name +'/'+ dataset_url)

#claning the data
df = df.withColumn('Installs', regexp_replace('Installs', '\+', ''))
df = df.withColumn('Size', regexp_replace('Size', 'M', ''))

# Saving the data to BigQuery
df.write.format('bigquery') \
  .option('table', bq_dataset_name + '.' + bq_table_name) \
  .mode('append')\
  .save()
