from pathlib import Path
from prefect import flow,task
from random import randint
from google.cloud import storage
from google.cloud import bigquery
import pandas as pd
import subprocess
import os
import re

# Here we are ingesting google playstore .csv file from local system to the google storage so that we can further process data.
@task (log_prints=True)
def ingesting_data_to_gcs(dataset_url:str,GcsBucket_name:str) -> str:
    "upload local paraquet file to gcs"
    command_to_run = f"gsutil -m cp -r {dataset_url} gs://{GcsBucket_name}/{dataset_url}"
    process = subprocess.run(command_to_run,shell=True,capture_output=True)
    if process.returncode !=0:
        print('Ingesting dataset to gcs failed !')
        print('Error messege :' + str(process.stderr))
    else:
        print('Dataset Ingested Successfully')
    return

#Here we are ingesting pyspark(.py) file in to google storage so that we can directly pass the file to the dataproc.
@task()
def ingesting_spark_file_to_gcs(spark_file_path:str,GcsBucket_name:str)->str :
    "upload local pyspark file to gcs"
    command_to_run = f"gsutil -m cp -r {spark_file_path} gs://{GcsBucket_name}/{spark_file_path}"
    process = subprocess.run(command_to_run,shell=True,capture_output=True)
    if process.returncode !=0:
        print('Job failed! Please check file path or Gcs CLI setup or check if file is already submitted.')
        print('Error messege :' + str(process.stderr))
    else:
        print('spark_file uploaded Successfully')
    return

# Here we are passing the pyspark file from google storage to dataproc and the result will be stored in BigQuery .
@task(name='data_processing',log_prints=True)
def submit_spark_job(spark_cluster_name:str, spark_job_region:str, GcsBucket_name:str, bq_dataset_name:str, bq_table_name:str, spark_file_path:str, dataset_url:str) -> str:
    #Write gcloud command to run in subprocess
    command_to_run = f"gcloud dataproc jobs submit pyspark \
                        --cluster={spark_cluster_name}\
                        --region={spark_job_region} \
                        --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
                        gs://{GcsBucket_name}/{spark_file_path}  \
                        -- \
                        --GcsBucket_name={GcsBucket_name}\
                        --dataset_url={dataset_url}\
                        --bq_dataset_name={bq_dataset_name}\
                        --bq_table_name={bq_table_name}"
    #Run command in subprocess
    process = subprocess.run(command_to_run, shell=True, capture_output=True)
    if process.returncode != 0:
        print('Job failed. Please check logs in Dataproc cluster.')
        print('Error message : ' + str(process.stderr))
    else:
        print('Job submitted successfully with following message : ' + str(process.stdout))
    return 
   
# This is the main function which Run's the all process.
@flow()
def etl_web_to_gcs() -> None:
    "The main ETL function"
    dataset_file = "Google-Playstore"
    dataset_url = "raw_data/Google-Playstore.csv" 
    GcsBucket_name = "datatalk-de-final-project"
    spark_file_path = "spark/test.py"
    bq_dataset_name = "de_final_project"
    bq_table_name = 'googleplaystore'
    spark_cluster_name = 'datatalk-final-spark-project'
    spark_job_region = 'asia-south1'
    ingesting_data_to_gcs(dataset_url,GcsBucket_name)
    ingesting_spark_file_to_gcs(spark_file_path,GcsBucket_name)
    submit_spark_job(spark_cluster_name,spark_job_region,GcsBucket_name,bq_dataset_name,bq_table_name,spark_file_path,dataset_url)


if __name__=='__main__':
    etl_web_to_gcs()
