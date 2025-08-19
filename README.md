## Batch ETL Pipeline into Amazon Redshift

## Objective
The goal of this project is to design and implement a batch ETL pipeline using AWS services.  
- Store raw sales data in **S3**  
- Transform data with **Glue ETL**  
- Catalog metadata in **Glue Catalog**  
- Load into **Amazon Redshift Serverless** for analytics  
- Manage all infrastructure with **Terraform**, without using the AWS Console  

---

## AWS Services Used
- **Amazon S3** → Raw & processed data storage  
- **AWS Glue** → Data Catalog & ETL jobs  
- **Amazon Redshift Serverless** → Data warehouse for queries  
- **AWS IAM** → Roles and policies for secure access  
- **Terraform** → Infrastructure as Code  
- **Python (Boto3, PySpark)** → Data generation & ETL scripts  

---

##  Project Structure
```
batch_etl_pipeline/
│── providers.tf       # Configures AWS provider & region
│── variables.tf       # Input variables
│── s3.tf              # Raw + processed S3 buckets
│── iam.tf             # IAM roles/policies for Glue & Redshift
│── glue.tf            # Glue database + catalog table
│── glue_etl.tf        # Glue ETL job definition
│── redshift.tf        # Redshift namespace & workgroup
│── scripts/
│    ├── gen_upload.py # Generates & uploads large CSV to S3
│    ├── sales_etl.py  # Glue ETL script (CSV → Parquet)
```

---

##  Architecture
```
Data Generator (Python)
        ↓
     Amazon S3 (Raw CSV)
        ↓
 AWS Glue ETL (sales_etl.py)
        ↓
     Amazon S3 (Parquet)
        ↓
 Amazon Redshift Serverless
        ↓
       SQL Queries
```

---

## What Each File Does
- **providers.tf** → Defines AWS provider and region  
- **variables.tf** → Stores project variables (region, bucket names, etc.)  
- **s3.tf** → Creates raw and processed S3 buckets  
- **iam.tf** → IAM roles for Glue (S3 full access) & Redshift (S3 read access)  
- **glue.tf** → Glue database (`salesdb`) and catalog table (`raw_sales`)  
- **glue_etl.tf** → Glue ETL job (`sales-etl-job`) to transform CSV → Parquet  
- **redshift.tf** → Redshift namespace (`sales-namespace`) and workgroup (`sales-workgroup`)  
- **scripts/gen_upload.py** → Generates large CSV (~4GB) and uploads to S3  
- **scripts/sales_etl.py** → ETL script that converts CSV → Parquet  

---

##  Workflow (Step by Step)

1. **Provision Infrastructure with Terraform**
   ```bash
   terraform init
   terraform apply -auto-approve
   ```

2. **Generate and Upload Raw Data**
   ```bash
   python3 scripts/gen_upload.py
   ```

3. **Run Glue ETL Job**
   ```bash
   aws glue start-job-run --job-name sales-etl-job
   ```

4. **Load Data into Redshift**
   ```bash
   aws redshift-data execute-statement      --workgroup-name sales-workgroup      --database dev      --sql "COPY sales_raw FROM 's3://processed-sales-data-batch-etl/' IAM_ROLE '<redshift-role-arn>' FORMAT AS PARQUET;"
   ```

5. **Query Data in Redshift**
   ```bash
   aws redshift-data execute-statement      --workgroup-name sales-workgroup      --database dev      --sql "SELECT * FROM sales LIMIT 5;"
   ```

---

##  Why Not Use a Glue Crawler?
- Schema is **fixed and known** (`id, product, price, quantity, date`)  
- Defining tables directly in Terraform is **cheaper and reproducible**  
- Avoids manual setup in the console  

---

##  Example Query Results
| id       | product | price | quantity | date       |
|----------|---------|-------|----------|------------|
| 48857866 | item    | 10.5  | 2        | 2025-08-17 |
| 48857867 | item    | 10.5  | 2        | 2025-08-17 |

---

##  Conclusion
This project demonstrates a **scalable, automated Batch ETL pipeline** built on AWS.  
It covers the full lifecycle: **Raw Data → S3 → Glue ETL → Processed Data → Redshift → SQL Analytics**.  

- Infrastructure is fully managed with **Terraform**  
- Jobs and queries are executed via **AWS CLI**  
- No AWS Console was used  
- A reproducible, cost-efficient pipeline suitable for large datasets  
