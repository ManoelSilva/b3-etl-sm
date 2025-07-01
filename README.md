# [Versão em Português](README.pt-br.md)

# ETL Project S3 → Glue with Step Functions

This project implements an ETL pipeline orchestrated by AWS Step Functions, triggered by persistence events in an S3 bucket. The infrastructure is provisioned via Terraform.

## Architecture

- **S3 Trigger**: When a file is persisted in the S3 bucket, an event triggers a Lambda function.
- **Lambda**: Responsible for starting a Step Function.
- **Step Function**: Orchestrates 3 sequential jobs in AWS Glue.
- **Glue Jobs**: Each job represents a stage of the ETL.
- **Terraform**: Provisions Lambda, Step Function, Glue Jobs, and triggers.

## Directory Structure

```
infra/           # Infrastructure as code (Terraform)
lambda/          # Lambda function code
jobs/            # Glue job scripts
```

## How to use

1. Configure variables in Terraform according to your environment.
2. Deploy the infrastructure with Terraform.
3. Upload files to the S3 bucket to trigger the pipeline. 