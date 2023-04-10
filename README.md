# Build an end-to-end automated data pipeline to visualize Google Playstore data.
This project is created by me for the [Data Engineering Zoomcamp 2023](https://github.com/DataTalksClub/data-engineering-zoomcamp). 

![Background Diagram](https://github.com/prashantg6838/datatalk-final-project/blob/main/background%20image%20.JPG)

## Problem statement and project description
This Project is about Understanding and getting overview of google playstore data . The dataset contain combination of various categories of Apps such as Entertainment,gaming,study related,
Bussiness Related and much more . 
Here Comes the problem statements:
- Find the most rated apps.
- Find the most rated apps category wise.
- Find the most downloaded free apps.
- Find which are the nonfree apps most downloaded category wise.

## Technologies, tools and data sources used
- **Docker** - For containerization of the pipeline.
- **Python** - To build the data pipeline.
- **Terraform** - Infrastructure-as-a-Service (IaaS) tool to manage GCP resources.
- **Prefect** - Orchestration tool to build deployments and monitor tasks and flows.
- **Spark** - To make data transformations on raw data.
- **Google Cloud Platform (GCP)** 
  - **Google Cloud Storage (GCS)** - Data Lake. 
  - **Big Query (BQ DWH)** - Data warehouse.
  - **DataProc Cluster** - Spark cluster to run spark jobs. 
- **Power BI** - To create dashboard and visualise the results.

## Pipeline diagram
 
![Pipeline Diagram](https://github.com/prashantg6838/datatalk-final-project/blob/main/Data-talk-final-project-Diagram.jpg)


## Pipeline explanation
This Pipe line contain five stages such as follows : 
- **Extraction** : Extracting the raw dataset from web and storing it in local storage.
- **Ingesting data into the Google cloud storage** : Here we are ingesting data in to google cloud storage for further processing the data .
- **Ingesting Pyspark-file into the google cloud storage** : for further Preprocessing pyspark-file stored in google cloud storage
- **Running spark cluster** : Here we are extracting pysprk file from google cloud storage and then aading this file with required details to run the spark cluster on dataproc
- **Ingesting data into the BigQuery** : After Processing the data it pushed into the Big Query for Further querying and analysing data.

### Step 1 - Set up – Takes approximately 15 mins.  
- 1) Download File form git hub to local system :Go to command prompt --> change location using cd -->  Copy this command --> 
     - git clone https://github.com/prashantg6838/datatalk-final-project.git and paste into the command prompt  
- 2) Download data using linux shell/git bash prompt .
  - git clone https://github.com/gauthamp10/Google-Playstore-Dataset.git
  - cd Google-Playstore-Dataset/dataset/
  - for f in *.tar.gz; do tar -xvf "$f"; done
  - cat Part?.csv > Google-Playstore.csv
- 3) create raw_data named folder and store the csv data . 
- 4) Install gcloud cli and authorize gcloud with browser. You’ll also need your GCP project ID handy to initialise gcloud. 
    https://cloud.google.com/sdk/docs/downloads-interactive.
- 5) open ANACONDA PROMPT direct to project folder and create virtual enviornment using following commands .
    - conda create -n virtual-env-name python=3.9  
    - once virtual env created the activate it using 
      - conda activate virtual-env-name 
    - once virtual env activated install librarires using 
      - pip install requirement.txt 
- 6) open another on command prompt to Set environmental variable for GCP key  
      - export GOOGLE_APPLICATION_CREDENTIALS=/app/codes/gcp_key.json (note - change path to your json key)
- 7) download terraform from this location https://developer.hashicorp.com/terraform/downloads and install it .
note. Check as of now anaconda prompt and command prompt is running .

### Step 2 - Create GCP resources with Terraform.  
- 1) Navigate inside the terraform folder.  
      - open variable.tf file it contain some variable names and default setup please keep as it is .
      - if you want to change variable region you can chang it but it keep in mind we need that.
      - Run following command in command prompt .
      - `terraform init`    
      - `terraform plan -var="project_name = your_gcp_project_id" "` (note . copy and paste your gcp project id) 
    Now it will automatically create all the resources we required . 
    
### Step 3 - Run the pipeline  
- 1) goto the project folder and open file in vscode or any editor flows\complete_etl_pipeline.py  
  -  set parameters as explained below . 
  - **datset_url** = "raw_data/Google-Playstore.csv" - raw data file in local system
  - **GcsBucket_name** : "your_gcs_bucket_name" – GCS data lake bucket name you have set with terraform.
  - **bq_dataset_name**: "your_bq_dataset_name" – BQ dataset name you have set with terraform.
  - **bq_table_name** : "your_bq_table_name" – BQ table to store data in.
  - **spark_cluster_name** : "your-spark-cluster-name" – DataProc cluster name you have set with Terraform.
  - **spark_job_region** : " your_region" – Region you have set with Terraform.
  - **spark_job_file** : "test.py" – Spark job python file. You don’t need to change this.  
- 2) Lets run the file :
  - open ANACONDA PROMT run prefect orion start 
  - once you see prefect logo on prompt keep it running and open another one anacoda prompt navigate to project folder and activate vitual env .
  - now run python flows\complete_etl_pipeline.py
  - it will take few minutes and runs all the steps. 
  - 
### Step 5(Optional) - Delete project.  
  
- Stop prefect agent with Control C.  
  
- Delete all GCP resources with Terraform – **Change the variable names as per your set up**.  
  - `terraform destroy -var="project_name=your_gcp_project_id" 
- You will also need to delete the temp storage bucket created by the Dataproc cluster. This has to be done manually.   
- exit the anaconda prompt and command prompt.
- 
## Dashboards 
- This dashoards explains Revenue generated by app category . 
![Dahboard 1](https://github.com/prashantg6838/datatalk-final-project/blob/main/Dashboards/app-category-dashboard.JPG)
- This dashbord explains Best apps by Ratings and No of Installs.
![Dahboard 2](https://github.com/prashantg6838/datatalk-final-project/blob/main/Dashboards/app-price-dashboard.JPG)

## Reviewing criteria  
- Problem description – *The problem statement and project description is defined [here](#problem-statement-and-project-description).*  
  - 0 points: Problem is not described
  - 1 point: Problem is described but shortly or not clearly
  - 2 points: Problem is well described and it's clear what the problem the project solves    
- **Cloud** – *GCP is used for data lake, data warehouse & dataproc cluster and is managed with Terraform.*
  - 0 points: Cloud is not used, things run only locally
  - 2 points: The project is developed in the cloud
  - 4 points: The project is developed in the cloud and IaC tools are used  
- **Data ingestion** (choose either batch or stream)  
  - Batch / Workflow orchestration – *Batch processing of end-to-end pipeline with tasks/flows defined in Prefect and Prefect cloud used for orchestrating runs.*
    - 0 points: No workflow orchestration
    - 2 points: Partial workflow orchestration: some steps are orchestrated, some run manually
    - 4 points: End-to-end pipeline: multiple steps in the DAG, uploading data to data lake
- **Data warehouse** – *Big Query Datawarehouse used to store transformed table. Please note for the sake of optimization, partitioning and clustering is not used for this project as we are not dealing with large size datasets. The final transformed data is in MBs and as discussed in lecture videos it doesn’t make sense to apply table partitioning and clustering in such cases. Reference to lecture - https://youtu.be/-CqXf7vhhDs?t=136*
  - 0 points: No DWH is used
  - 2 points: Tables are created in DWH, but not optimized
  - 4 points: Tables are partitioned and clustered in a way that makes sense for the upstream queries (with explanation)
- **Transformations** (dbt, spark, etc) – *Spark is used for data transformations.*
  - 0 points: No transformations
  - 2 points: Simple SQL transformation (no dbt or similar tools)
  - 4 points: Transformations are defined with dbt, Spark or similar technologies
- **Dashboard** – *Dashboard is created with Looker studio. 3 charts/tiles created.*
  - 0 points: No dashboard
  - 2 points: A dashboard with 1 tile
  - 4 points: A dashboard with 2 tiles
-**Reproducibility** – *Documentation written in detail to include project description, pipeline diagram, pipeline explanation, clear steps to reproduce along with summary of findings and notes on scope for improvement.*
  - 0 points: No instructions how to run code at all
  - 2 points: Some instructions are there, but they are not complete
  - 4 points: Instructions are clear, it's easy to run the code, and the code works
