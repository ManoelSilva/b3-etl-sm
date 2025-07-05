import sys
import boto3
from botocore.exceptions import ClientError
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
import re

# @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Parameters
bucket_name = '861115334572-refined'
input_path = f's3://{bucket_name}/b3/'
database_name = 'default'
table_name = 'b3_tbl_refined'

# Schema definition (adjust as needed)
schema_columns = [
    {'Name': 'ticker', 'Type': 'string'},
    {'Name': 'type', 'Type': 'string'},
    {'Name': 'part', 'Type': 'double'},
    {'Name': 'theoricalQty', 'Type': 'string'},
    {'Name': 'initial_date', 'Type': 'string'},
    {'Name': 'part_sum_from_initial_date', 'Type': 'double'}
]
input_format = 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
output_format = 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
serde_info = {
    'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe',
    'Parameters': {}
}

# Create boto3 client
session = boto3.Session()
glue_client = session.client('glue')

# Create the table in Glue Data Catalog if it does not exist


def ensure_table_exists():
    try:
        glue_client.get_table(DatabaseName=database_name, Name=table_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityNotFoundException':
            glue_client.create_table(
                DatabaseName=database_name,
                TableInput={
                    'Name': table_name,
                    'StorageDescriptor': {
                        'Columns': schema_columns,
                        'Location': input_path,
                        'InputFormat': input_format,
                        'OutputFormat': output_format,
                        'SerdeInfo': serde_info
                    },
                    'PartitionKeys': [
                        {'Name': 'code', 'Type': 'string'},
                        {'Name': 'reference_date', 'Type': 'string'}
                    ],
                    'TableType': 'EXTERNAL_TABLE',
                    'Parameters': {
                        'classification': 'parquet'
                    }
                }
            )
        else:
            raise


ensure_table_exists()

# Read partitioned data from S3
df = spark.read.parquet(input_path)

dyf = DynamicFrame.fromDF(df, glueContext, 'dyf')

# Write to Glue Data Catalog, adding partitions
output = glueContext.write_dynamic_frame.from_options(
    frame=dyf,
    connection_type="s3",
    connection_options={
        "path": input_path,
        "partitionKeys": ["code", "reference_date"],
        "enableUpdateCatalog": True,
        "updateBehavior": "UPDATE_IN_DATABASE",
        "database": database_name,
        "tableName": table_name
    },
    format="parquet",
    format_options={"compression": "SNAPPY"}
)

# Explicitly register partitions in Glue Data Catalog
s3_client = boto3.client('s3')

# Extract bucket and prefix from input_path
bucket = bucket_name
prefix = 'b3/'

# List partition directories in S3 (code=XXX/reference_date=YYYY-MM-DD/)
partitions = set()
paginator = s3_client.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter='/'):
    for obj in page.get('Contents', []):
        match = re.search(r'code=([^/]+)/reference_date=([^/]+)/', obj['Key'])
        if match:
            code = match.group(1)
            reference_date = match.group(2)
            partitions.add((code, reference_date))

# Build the list of partitions for Glue
partition_inputs = []
for code, reference_date in partitions:
    partition_inputs.append({
        'Values': [code, reference_date],
        'StorageDescriptor': {
            'Columns': schema_columns,
            'Location': f's3://{bucket}/b3/code={code}/reference_date={reference_date}/',
            'InputFormat': input_format,
            'OutputFormat': output_format,
            'SerdeInfo': serde_info,
            'Parameters': {}
        },
        'Parameters': {}
    })

# Explicitly register partitions (in batches of up to 100)
if partition_inputs:
    for i in range(0, len(partition_inputs), 100):
        glue_client.batch_create_partition(
            DatabaseName=database_name,
            TableName=table_name,
            PartitionInputList=partition_inputs[i:i+100]
        )

job.commit()
