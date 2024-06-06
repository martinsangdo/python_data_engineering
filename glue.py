import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark_local.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame
from datetime import datetime
from pyspark_local.sql.types import StructType, StructField, StringType

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Define the schema of the data
schema = StructType([
    StructField("ip", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("method", StringType(), True),
    StructField("path", StringType(), True),
    StructField("params", StringType(), True)
])

# External value
current_timestamp = datetime.utcnow().strftime('%d%b%YT%H')

# Script generated for node Amazon S3 and read the data directly from S3( with specifying partition keys and prefilter folder with matching timestamp only)
AmazonS3_node1716879376751 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://quin-click-stream/click_stream/"],
        "recurse": True,
        "groupFiles": "inPartition",
        "partitionKeys": ["timestamp", "path"],
        "pushDownPredicate": f"timestamp = '{current_timestamp}'"
    },
    transformation_ctx="AmazonS3_node1716879376751"
)

# Script generated for node SQL Query
SqlQuery340 = '''
SELECT
    path AS api_path,
    FIRST(timestamp) AS hour_window,
    COUNT(*) AS total_requests
FROM myDataSource
GROUP BY path;
'''

SQLQuery_node1716879530275 = sparkSqlQuery(glueContext, query = SqlQuery340, mapping = {"myDataSource":AmazonS3_node1716879376751}, transformation_ctx = "SQLQuery_node1716879530275")

# Script generated for node Amazon Redshift
AmazonRedshift_node1716887836380 = glueContext.write_dynamic_frame.from_options(frame=SQLQuery_node1716879530275, connection_type="redshift", connection_options={"redshiftTmpDir": "s3://aws-glue-assets-767397925699-ap-southeast-1/temporary/", "useConnectionProperties": "true", "dbtable": "public.clickstreamcounts", "connectionName": "Redshift connection", "preactions": "CREATE TABLE IF NOT EXISTS public.clickstreamcounts (api_path VARCHAR, hour_window VARCHAR, total_requests BIGINT);"}, transformation_ctx="AmazonRedshift_node1716887836380")

job.commit()
