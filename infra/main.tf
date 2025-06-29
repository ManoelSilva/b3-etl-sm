// Terraform principal para ETL S3 → Glue

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
  required_version = ">= 1.0.0"
}

provider "aws" {
  region = var.aws_region
}

module "glue" {
  source     = "./glue_module"
}

module "step_function" {
  source = "./step_function_module"
}

module "lambda" {
  source = "./lambda_module"
}