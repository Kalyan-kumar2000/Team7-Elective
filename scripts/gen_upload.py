import pandas as pd
import boto3

rows = 50_000_000   
df = pd.DataFrame({
    "id": range(rows),
    "product": ["item"] *rows,
    "price": [10.5] * rows,
    "quantity": [2] * rows,
    "date": ["2025-08-17"] * rows
})

file = "sales_4gb.csv"
df.to_csv(file, index=False)

s3 = boto3.client("s3", region_name="us-east-2")
s3.upload_file(file, "raw-sales-data-batch-etl", "sales_4gb.csv")
s3.upload_file("scripts/sales_etl.py", "raw-sales-data-batch-etl", "scripts/sales_etl.py")

