
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, count, array_distinct, collect_set, flatten, array
from pyspark.sql.types import BooleanType, IntegerType, StringType, StructType, StructField
import calendar
import time

def getCurrentTimestamp():
    return int(calendar.timegm(time.gmtime()))

def main():
    # Initialize Spark Session
    start_time = getCurrentTimestamp()
    # I create 2 collections in my local database: collection testing for reading input and collection testing_summary for writting output
    spark = SparkSession.builder \
        .appName("FacebookRequestProcessor") \
        .config("spark.mongodb.input.uri", "mongodb://localhost:27017/studio_social_qa_20240204.facebook_request") \
        .config("spark.mongodb.output.uri", "mongodb://localhost:27017/studio_social_qa_20240204.facebook_request_summary") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .config("spark.sql.debug.maxToStringFields","200") \
        .getOrCreate()

    # Define the schema for the 'message' field
    message_schema = StructType([
    StructField("error", StructType([
        StructField("message", StringType(), True),
        StructField("type", StringType(), True),
        StructField("code", IntegerType(), True),
        StructField("error_subcode", IntegerType(), True),
        StructField("is_transient", BooleanType(), True),
        StructField("error_user_title", StringType(), True),
        StructField("error_user_msg", StringType(), True),
        StructField("fbtrace_id", StringType(), True)
    ]), True)
])
    # Read data from MongoDB
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    
    # Only keep columns requestUrl + message column
    partitioned_requests = df.select(col('requestUrl'), col('message'))
    
    # partitioned_requests.show(truncate=False)
    # partitioned_requests.printSchema()


    # Parse JSON message and extract error details
    parsed_requests = partitioned_requests.withColumn("message", from_json("message", message_schema)).select(col('requestUrl'), col('message.error.message'),col("message.error.error_user_msg"))
    
    # parsed_requests.show(truncate=False)
    # parsed_requests.printSchema()


    # Group by requestUrl and aggregate message and error_user_msg
    grouped_requests = parsed_requests.groupBy("requestUrl") \
        .agg(
            count("*").alias("count"),
            collect_set("message").alias("messages"),
            collect_set("error_user_msg").alias("error_user_msgs")
        ) \
        .withColumn("messages", array_distinct(flatten(array("messages", "error_user_msgs")))) \
        .drop("error_user_msgs")
        
    # grouped_requests.show(truncate=False)
    # grouped_requests.printSchema()

    # # # Write the summarized data to S3
    # # grouped_requests.write.json("s3://your-bucket/facebook-request-summary/")

    # Write the summarized data back to MongoDB
    grouped_requests.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()

    # Stop Spark Session
    spark.stop()

    end_time = getCurrentTimestamp()

    print(end_time - start_time)    #local 41s, 32s, ...


if __name__ == '__main__':
    main()
