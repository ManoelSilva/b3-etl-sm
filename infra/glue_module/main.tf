resource "aws_s3_bucket" "scripts" {
  bucket        = var.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket" "refined" {
  bucket        = var.refined_bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "block" {
  bucket = aws_s3_bucket.scripts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "extract_script" {
  bucket = aws_s3_bucket.scripts.id
  key    = "scripts/extract.py"
  source = "${path.module}/../../jobs/extract.py"
  etag   = filemd5("${path.module}/../../jobs/extract.py")
}

resource "aws_s3_object" "transform_script" {
  bucket = aws_s3_bucket.scripts.id
  key    = "scripts/transform.py"
  source = "${path.module}/../../jobs/transform.py"
  etag   = filemd5("${path.module}/../../jobs/transform.py")
}

resource "aws_s3_object" "load_script" {
  bucket = aws_s3_bucket.scripts.id
  key    = "scripts/load.py"
  source = "${path.module}/../../jobs/load.py"
  etag   = filemd5("${path.module}/../../jobs/load.py")
}

resource "aws_glue_job" "extract" {
  name     = "b3-etl-extract-step"
  role_arn = var.lab_role_arn
  command {
    name            = "glueetl"
    script_location = "s3://${var.bucket_name}/scripts/extract.py"
    python_version  = "3"
  }
  glue_version = "5.0"
  max_capacity = 2
}

resource "aws_glue_job" "transform" {
  name     = "b3-etl-transform-step"
  role_arn = var.lab_role_arn
  command {
    name            = "glueetl"
    script_location = "s3://${var.bucket_name}/scripts/transform.py"
    python_version  = "3"
  }
  glue_version = "5.0"
  max_capacity = 2
}

resource "aws_glue_job" "load" {
  name     = "b3-etl-load-step"
  role_arn = var.lab_role_arn
  command {
    name            = "glueetl"
    script_location = "s3://${var.bucket_name}/scripts/load.py"
    python_version  = "3"
  }
  glue_version = "5.0"
  max_capacity = 2
}

output "glue_extract_job_name" {
  value = aws_glue_job.extract.name
}
output "glue_transform_job_name" {
  value = aws_glue_job.transform.name
}
output "glue_load_job_name" {
  value = aws_glue_job.load.name
} 