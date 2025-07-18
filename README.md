# [Versão em Português](README.pt-br.md)

# ETL Project S3 → Glue with Step Functions

This project implements an ETL pipeline orchestrated by AWS Step Functions, triggered by persistence events in an S3 bucket. The infrastructure is provisioned via Terraform.

## Architecture

- **S3 Trigger**: When a file is persisted in the S3 bucket, an event triggers a Lambda function.
- **Lambda**: Responsible for starting a Step Function execution.
- **Step Function**: Orchestrates 3 sequential jobs in AWS Glue (extract, transform, load).
- **Glue Jobs**:
  - **extract.py**: Creates the Glue table and registers partitions from the raw S3 bucket.
  - **transform.py**: Reads, cleans, and transforms the data, generating rolling statistics and writing to the refined bucket.
  - **load.py**: Registers the transformed data in a new Glue table and updates partitions.
- **Terraform**: Provisions Lambda, Step Function, Glue Jobs, S3 buckets, and triggers.
- **Notebook**: Athena visualization notebook for data analysis and dashboards.

## Directory Structure

```
infra/           # Infrastructure as code (Terraform)
lambda/          # Lambda function code (start Step Function)
jobs/            # Glue job scripts (extract, transform, load)
notebook/        # Athena visualization notebook
```

## How to use

1. Configure variables in Terraform according to your environment (see `infra/variables.tf`).
2. Deploy the infrastructure with Terraform:
   ```sh
   cd infra
   terraform init
   terraform apply
   ```
3. Upload files to the S3 raw bucket to trigger the pipeline.
4. The Lambda function (`lambda/start_step.py`, dependency: `boto3`) will start the Step Function execution.
5. The Step Function will run the Glue jobs in sequence:
   - **extract.py**: Creates/updates the Glue table and partitions for raw data.
   - **transform.py**: Cleans and transforms the data, computes rolling statistics, and writes to the refined bucket.
   - **load.py**: Registers the refined data in a new Glue table and updates partitions.
6. (Optional) Use the Jupyter notebook in `notebook/athena_visualization.ipynb` to analyze and visualize the processed data with Athena.

## Lambda Dependencies

- The Lambda function requires `boto3` (see `lambda/requirements.txt`).

## Notebook Visualization

- The notebook requires: `PyAthena`, `pandas`, `plotly`, `boto3`, `sqlalchemy`.
- Install dependencies in your Jupyter environment:
  ```python
  %pip install PyAthena pandas plotly boto3 sqlalchemy
  ```
- Adjust the connection settings in the notebook as needed (AWS region, S3 staging dir, database/table names).
- Run the notebook to generate dashboards and analyses from the processed data.

## Notes

- All infrastructure is managed via Terraform modules in `infra/`.
- Glue jobs and Lambda code are in `jobs/` and `lambda/` respectively.
- The pipeline is fully event-driven: uploading a file to the S3 raw bucket triggers the entire ETL process automatically. 