from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, format_number, lit
import os

# Initializes and returns a Spark session
def initialize_spark_session():
    return SparkSession.builder.appName("hello-spark").getOrCreate()

# Reads data from a specified location and returns a DataFrame
def read_data(spark):
    return spark.read.option("basePath", "./inputs/").parquet("./inputs/date=*/")

# Extracts and transforms data based on the direction (input/output) and returns a DataFrame
def extract_data(df, direction):
    if direction == "input":
        explode_col = "inputs"
    else:
        explode_col = "outputs"
    return df.select(
        col("hash"),
        col("block_timestamp"),
        col("date"),
        explode(explode_col).alias(direction)
    ).select(
        col("hash"),
        col("block_timestamp"),
        col("date"),
        col(f"{direction}.address").alias("address"),
        col(f"{direction}.value").alias("amount")
    ).withColumn("direction", lit(direction))

# Combines input and output DataFrames, orders, and formats them, then returns the resulting DataFrame
def combine_and_format_data(inputs_df, outputs_df):
    tx_df = inputs_df.union(outputs_df)
    tx_df = tx_df.select("hash", "block_timestamp", "direction", "address", "amount", "date")
    tx_df = tx_df.orderBy("hash", "direction")
    return tx_df.withColumn("amount", format_number("amount", 8))

# Exports the final DataFrame to a specified location in Parquet format
def export_data(tx_df):
    os.makedirs("./outputs", exist_ok=True)
    tx_df.coalesce(1).write.mode("overwrite").partitionBy("date").parquet("./outputs/")
    
if __name__ == '__main__':
    spark = initialize_spark_session()
    spark.conf.set("mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
    df = read_data(spark)
    inputs_df = extract_data(df, "input")
    outputs_df = extract_data(df, "output")
    tx_df = combine_and_format_data(inputs_df, outputs_df)
    export_data(tx_df)
