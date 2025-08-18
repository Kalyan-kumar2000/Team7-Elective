resource "aws_glue_catalog_database" "sales_db" {
  name = "salesdb"
}

resource "aws_glue_catalog_table" "sales_table" {
  database_name = aws_glue_catalog_database.sales_db.name
  name          = "raw_sales"

  storage_descriptor {
    location      = "s3://${var.raw_bucket}/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      name                  = "OpenCSVSerDe"
      serialization_library = "org.apache.hadoop.hive.serde2.OpenCSVSerde"
    }

    columns {
      name = "id"
      type = "int"
    }

    columns {
      name = "product"
      type = "string"
    }

    columns {
      name = "price"
      type = "double"
    }

    columns {
      name = "quantity"
      type = "int"
    }

    columns {
      name = "date"
      type = "string"
    }
  }
}

