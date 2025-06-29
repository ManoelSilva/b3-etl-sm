import sys
import boto3
from botocore.exceptions import ClientError
import re

## @params: [JOB_NAME]
# (Mantido para compatibilidade, mas não usado)
# args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Parâmetros do S3 e Glue
ds3_path = 's3://861115334572-raw/'
database = 'b3_db'
table_name = 'b3_tbl'

# Definição do schema e formatos (usado na tabela e nas partições)
schema_columns = [
    {'Name': 'segment', 'Type': 'int'},
    {'Name': 'cod', 'Type': 'string'},
    {'Name': 'asset', 'Type': 'string'},
    {'Name': 'type', 'Type': 'string'},
    {'Name': 'part', 'Type': 'string'},
    {'Name': 'partAcum', 'Type': 'int'},
    {'Name': 'theoricalQty', 'Type': 'string'}
]
input_format = 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
output_format = 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
serde_info = {
    'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe',
    'Parameters': {}
}

# Cria boto3 clients
session = boto3.Session()
glue_client = session.client('glue')
s3_client = session.client('s3')

# Cria o database se não existir
try:
    glue_client.create_database(DatabaseInput={'Name': database})
except ClientError as e:
    if e.response['Error']['Code'] != 'AlreadyExistsException':
        raise

# Cria a tabela se não existir
try:
    glue_client.get_table(DatabaseName=database, Name=table_name)
    # Se não lançar exceção, a tabela já existe
except ClientError as e:
    if e.response['Error']['Code'] == 'EntityNotFoundException':
        # Tabela não existe, então cria
        glue_client.create_table(
            DatabaseName=database,
            TableInput={
                'Name': table_name,
                'StorageDescriptor': {
                    'Columns': schema_columns,
                    'Location': ds3_path,
                    'InputFormat': input_format,
                    'OutputFormat': output_format,
                    'SerdeInfo': serde_info
                },
                'PartitionKeys': [
                    {'Name': 'date', 'Type': 'string'}
                ],
                'TableType': 'EXTERNAL_TABLE',
                'Parameters': {
                    'classification': 'parquet'
                }
            }
        )
    elif e.response['Error']['Code'] != 'AlreadyExistsException':
        raise

# Descobre as partições 'date' presentes no S3
bucket = ds3_path.replace('s3://', '').split('/')[0]
prefix = ds3_path.replace(f's3://{bucket}/', '')
if prefix and not prefix.endswith('/'):
    prefix += '/'

# Lista as pastas de partição
paginator = s3_client.get_paginator('list_objects_v2')
partition_values = set()
for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
    for obj in page.get('Contents', []):
        match = re.search(r'date=([0-9\-]+)/', obj['Key'])
        if match:
            partition_values.add(match.group(1))

# Registra as partições no Glue
partitions = []
for value in partition_values:
    partitions.append({
        'Values': [value],
        'StorageDescriptor': {
            'Columns': schema_columns,
            'Location': f'{ds3_path}date={value}/',
            'InputFormat': input_format,
            'OutputFormat': output_format,
            'SerdeInfo': serde_info
        },
        'Parameters': {}
    })

if partitions:
    # O batch_create_partition aceita até 100 partições por chamada
    for i in range(0, len(partitions), 100):
        glue_client.batch_create_partition(
            DatabaseName=database,
            TableName=table_name,
            PartitionInputList=partitions[i:i+100]
        )