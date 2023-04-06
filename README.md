# Build an end-to-end automated data pipeline to visualise Google Playstore scrapped data.

This project is created by me for the [Data Engineering Zoomcamp 2023](https://github.com/DataTalksClub/data-engineering-zoomcamp).  


## Problem statement and project description
This Project is about Understanding and getting overview of google playstore data . The dataset contain combination of various categories of Apps such as Entertainment,gaming,study related,
Bussiness Related and much more . 
Here Comes the problem statements:
- Find the most rated apps
- Find the most rated apps category wise
- Find which are the free apps most downloaded
- Find which are the nonfree apps most downloaded category wise

## Technologies, tools and data sources used
- Docker - For containerization of the pipeline.
- Python - To build the data pipeline.
- Terraform - Infrastructure-as-a-Service (IaaS) tool to manage GCP resources.
- Prefect - Orchestration tool to build deployments and monitor tasks and flows.
- Spark - To make data transformations on raw data.
- Google Cloud Platform (GCP) 
  - Google Cloud Storage (GCS) - Data Lake. 
  - Big Query (BQ DWH) - Data warehouse.
  - DataProc Cluster - Spark cluster to run spark jobs. 
- Power BI - To create dashboard and visualise the results.

## Pipeline diagram
 
![Pipeline Diagram](https://github.com/prashantg6838/datatalk-final-project/blob/main/workflow.JPG)


## Pipeline explanation
This Pipe line contain 
- Extraction : Extracting the dataset which i stored on my google drive . it is approx 647MB size and contain more than 2 lakh Rows and 24 columns.
- Ingesting data into the Google cloud storage : Here we are ingesting data in to google cloud storage for further processing the data .
- Ingesting Pyspark-file into the google cloud storage : for further Preprocessing pyspark-file stored in google cloud storage
- Running spark cluster : Here we are extracting pysprk file from google cloud storage and then aading this file with required details to run the spark cluster on dataproc
- Ingesting data into the BigQuery : After Processing the data it pushed into the Big Query for Furthe querying and aanalysing data.

## How to replicate 

### Step 0 - Get the following before starting to replicate.  
- Alpha Vantage API free key - https://www.alphavantage.co/support/#api-key.  
  
- GCP service account key(JSON) - Roles -> Owner - https://cloud.google.com/iam/docs/service-accounts-create and https://cloud.google.com/iam/docs/keys-create-delete. 
- Create a prefect cloud account, create a workspace and an API key - https://docs.prefect.io/ui/cloud-api-keys/.
- Install Docker - https://docs.docker.com/desktop/.

### Step 1 - Set up – Takes approximately 15 mins.  
- Download the entire folder/clone the repo.  
  
- Replace the dummy **gcp_key.json** file inside the codes folder with your own key. Make sure to rename it to gcp_key.json.  
- Start Docker desktop and open terminal in the folder containing your DockerFile.  
- Build Docker image.  
`docker build -t de_zc .`  
- Create container from image/start the container.   
`docker run -it --name de_zc_container de_zc`  
- *Going forward use this command to start the container.  
`docker start -i de_zc_container`  
- Install gcloud cli and authorize gcloud with browser. You’ll also need your GCP project ID handy to initialise gcloud. Note - Docker OS is Debian. https://cloud.google.com/sdk/docs/install#deb.  
- Install Terraform. https://developer.hashicorp.com/terraform/downloads. For installation choose Linux(Ubuntu/Debian).
- Connect to prefect cloud with your key.  
`prefect cloud login -k prefect_key`  
- Set environmental variable for GCP key  
`export GOOGLE_APPLICATION_CREDENTIALS=/app/codes/gcp_key.json`

### Step 2 - Create GCP resources with Terraform.  
- Navigate inside the codes folder.  
`cd codes`  
- Run following commands and follow instructions – **Change the variable names as per your set up**.  
`terraform init`    
`terraform plan -var="project_name=your_gcp_project_id" -var="region=your_region" -var="gcs_bucket_name=your_gcs_bucket_name" -var="bq_dataset_name=your_bq_dataset_name" -var="spark_cluster_name=your-spark-cluster-name"`    
`terraform apply -var="project_name=your_gcp_project_id" -var="region=your_region" -var="gcs_bucket_name=your_gcs_bucket_name" -var="bq_dataset_name=your_bq_dataset_name" -var="spark_cluster_name=your-spark-cluster-name"`    

### Step 3 - Build deployment and save it to cloud (Make sure you are connected to prefect cloud).  
- `python pipeline_deployment_build.py`  

### Step 4 - Run the pipeline  
- Go to prefect cloud to manage your runs. Your deployment ‘Data Pipeline Main Flow - DE ZC 2023’ should be created in the deployments section. Do a quick run and edit the parameters.  
  
- Parameters explanation here.  
  - "gcp_key_path”: "/app/codes/gcp_key.json" – Path to gcp key. You don’t need to change this.  
    
  - "alpha_vantage_key” : "alpha_vantage_api_key" – Your free Alpha Vantage API key.
  - "from_date” : "2023-03-27" – Starting date (**Monday** in YYYY-MM-DD format) to pull data from.
  - "to_date" : "2023-04-03" – Ending date (**Monday** in YYYY-MM-DD) to pull date until. 
  - "gcs_bucket_name" : "your_gcs_bucket_name" – GCS data lake bucket name you have set with terraform.
  - "bq_dataset_name” : "your_bq_dataset_name" – BQ dataset name you have set with terraform.
  - "bq_table_name” : "your_bq_table_name" – BQ table to store data in.
  - "spark_cluster_name” : "your-spark-cluster-name" – DataProc cluster name you have set with Terraform.
  - "spark_job_region” : " your_region" – Region you have set with Terraform.
  - "spark_job_file” : "spark_job.py" – Spark job python file. You don’t need to change this.  

- Start prefect agent in your docker container and wait for the flow run to start.  
`prefect agent start -q default`  
  
- Once the agent picks up the run, you can then monitor its progress in prefect cloud.  

### Step 5(Optional) - Delete project.  
  
- Stop prefect agent with Control C.  
  
- Delete all GCP resources with Terraform – **Change the variable names as per your set up**.  
`terraform destroy -var="project_name=your_gcp_project_id" -var="region=your_region" -var="gcs_bucket_name=your_gcs_bucket_name" -var="bq_dataset_name=your_bq_dataset_name" -var="spark_cluster_name=your-spark-cluster-name"`    
  
- You will also need to delete the temp storage bucket created by the Dataproc cluster. This has to be done manually.   

- Exit from the container.  
`exit`  
  
- Delete container.   
`docker rm de_zc_container`  
  
- Delete image.  
`docker image rm de_zc`

## Dashboard and results 

  

## Reviewing criteria  
- Problem description – *The problem statement and project description is defined [here](#problem-statement-and-project-description).*  
  
  - 0 points: Problem is not described
  - 1 point: Problem is described but shortly or not clearly
  - 2 points: Problem is well described and it's clear what the problem the project solves    
- Cloud – *GCP is used for data lake, data warehouse & dataproc cluster and is managed with Terraform.*
  - 0 points: Cloud is not used, things run only locally
  - 2 points: The project is developed in the cloud
  - 4 points: The project is developed in the cloud and IaC tools are used  
- Data ingestion (choose either batch or stream)  
  - Batch / Workflow orchestration – *Batch processing of end-to-end pipeline with tasks/flows defined in Prefect and Prefect cloud used for orchestrating runs.*
    - 0 points: No workflow orchestration
    - 2 points: Partial workflow orchestration: some steps are orchestrated, some run manually
    - 4 points: End-to-end pipeline: multiple steps in the DAG, uploading data to data lake
- Data warehouse – *Big Query Datawarehouse used to store transformed table. Please note for the sake of optimization, partitioning and clustering is not used for this project as we are not dealing with large size datasets. The final transformed data is in MBs and as discussed in lecture videos it doesn’t make sense to apply table partitioning and clustering in such cases. Reference to lecture - https://youtu.be/-CqXf7vhhDs?t=136*
  - 0 points: No DWH is used
  - 2 points: Tables are created in DWH, but not optimized
  - 4 points: Tables are partitioned and clustered in a way that makes sense for the upstream queries (with explanation)
- Transformations (dbt, spark, etc) – *Spark is used for data transformations.*
  - 0 points: No transformations
  - 2 points: Simple SQL transformation (no dbt or similar tools)
  - 4 points: Transformations are defined with dbt, Spark or similar technologies
- Dashboard – *Dashboard is created with Looker studio. 3 charts/tiles created.*
  - 0 points: No dashboard
  - 2 points: A dashboard with 1 tile
  - 4 points: A dashboard with 2 tiles
- Reproducibility – *Documentation written in detail to include project description, pipeline diagram, pipeline explanation, clear steps to reproduce along with summary of findings and notes on scope for improvement.*
  - 0 points: No instructions how to run code at all
  - 2 points: Some instructions are there, but they are not complete
  - 4 points: Instructions are clear, it's easy to run the code, and the code works
