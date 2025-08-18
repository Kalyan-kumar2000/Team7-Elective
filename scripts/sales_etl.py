import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Read raw CSV from S3
datasource = glueContext.create_dynamic_frame.from_options(
    "s3",
    {"paths": ["s3://raw-sales-data-batch-etl/sales_4gb.csv"]},
    format="csv",
    format_options={"withHeader": True}
)

# Convert to Parquet
datasink = glueContext.write_dynamic_frame.from_options(
    frame=datasource,
    connection_type="s3",
    connection_options={"path": "s3://processed-sales-data-batch-etl/"},
    format="parquet"
)

job.commit()

