import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from botocore.exceptions import ClientError
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType

# Remove columns where all values are null, but always keep essential columns
# Essential columns: cod, asset, type, part, theoricalQty, date


def remove_all_null_columns(df, keep_columns=None):
    if keep_columns is None:
        keep_columns = []
    non_null_counts = df.select([F.count(F.col(c)).alias(c)
                                for c in df.columns]).collect()[0].asDict()
    # Always keep essential columns, even if all values are null
    non_all_null_cols = [
        c for c, count in non_null_counts.items() if count > 0 or c in keep_columns]
    return df.select(*non_all_null_cols)


# @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from Glue Catalog table 'b3_tbl' in schema 'default'
dyf = glueContext.create_dynamic_frame.from_catalog(
    database="default",
    table_name="b3_tbl"
)

df = dyf.toDF()

# Log: show schema and sample after reading from Glue
print('Schema after reading from Glue:')
df.printSchema()
print('Sample data after reading from Glue:')
df.show(5)

# Use the function after renaming columns, passing the original names for protection
# Since columns are renamed to 'code' and 'ticker', protect both original and new names
essential_columns = ['cod', 'asset', 'type', 'part', 'theoricalQty', 'date']
df = remove_all_null_columns(df, keep_columns=essential_columns)

# Log: show schema and sample after removing all-null columns
print('Schema after removing all-null columns:')
df.printSchema()
print('Sample data after removing all-null columns:')
df.show(5)

# Rename columns: 'cod' to 'code', 'asset' to 'ticker'
df = df.withColumnRenamed('cod', 'code').withColumnRenamed(
    'asset', 'ticker').withColumnRenamed('date', 'reference_date')

# Ensure 'part' is numeric: replace comma with dot and cast to DoubleType for precision
# DoubleType is chosen because it provides good precision for financial and fractional values, and is the standard for floating-point numbers in Spark
if 'part' in df.columns:
    df = df.withColumn('part', F.regexp_replace(
        'part', ',', '.').cast(DoubleType()))
else:
    print('Column "part" does not exist in DataFrame!')

# Log: show schema and sample after renaming columns
print("Schema after renaming columns 'cod' to 'code' and 'asset' to 'ticker':")
df.printSchema()
print('Sample data after renaming columns:')
df.show(5)

# Add column initial_date with the earliest date in the DataFrame
df_dates = df.filter(F.col('reference_date').isNotNull())
initial_date = df_dates.agg(F.min('reference_date')).collect()[
    0][0] if df_dates.count() > 0 else None
if initial_date is not None:
    df = df.withColumn('initial_date', F.lit(initial_date))
else:
    print('No date found to calculate initial_date.')
    df = df.withColumn('initial_date', F.lit(None))

# Add column with cumulative sum of 'part' from initial_date to reference_date, grouped by code
window_spec = Window.partitionBy('code').orderBy(
    'reference_date').rowsBetween(Window.unboundedPreceding, Window.currentRow)
df = df.withColumn('part_sum_from_initial_date',
                   F.sum(F.col('part')).over(window_spec))

print("Schema after adding initial_date and part_sum_from_initial_date:")
df.printSchema()
print('Sample data after adding initial_date and part_sum_from_initial_date:')
df.show(5)

# S3 bucket and output path
bucket_name = '861115334572-refined'
output_path = f's3://{bucket_name}/b3'

# Filter out rows with null partition columns before writing
if 'reference_date' in df.columns and 'code' in df.columns:
    df = df.filter(F.col('reference_date').isNotNull()
                   & F.col('code').isNotNull())
    print("Output path:", output_path)
    print("Sample data before write:")
    df.show(5)
    # Check if DataFrame is not empty
    if not df.rdd.isEmpty():
        df.write.partitionBy('code', 'reference_date').mode(
            'overwrite').parquet(output_path)
    else:
        print("DataFrame is empty, nothing to write.")
else:
    print("Partition columns 'reference_date' or 'code' do not exist in DataFrame.")

job.commit()
