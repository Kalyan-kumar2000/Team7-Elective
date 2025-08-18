resource "aws_glue_job" "sales_etl" {
  name     = "sales-etl-job"
  role_arn = aws_iam_role.glue_role.arn

  command {
    name            = "glueetl"
    script_location = "s3://${var.raw_bucket}/scripts/sales_etl.py"
    python_version  = "3"
  }

  default_arguments = {
    "--TempDir" = "s3://${var.processed_bucket}/temp/"
  }
}

