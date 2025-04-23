from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode, from_unixtime, window, avg, sum
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, ArrayType
import os

# ---- Configuration ----
# Get environment variables (Kafka o Cassandra)
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "cassandra")

# Initialize Spark Session m3a configs l-Cassandra
spark = (SparkSession.builder
    .appName("FinancialDataStreaming")
    .config("spark.cassandra.connection.host", CASSANDRA_HOST)
    .config("spark.cassandra.connection.port", "9042")
    .config("spark.streaming.kafka.maxRatePerPartition", "100")
    .getOrCreate())

# ---- Schema ----
# Define schema dyal l-Kafka messages (JSON format)
schema = StructType([
    StructField("type", StringType(), True),
    StructField("data", ArrayType(StructType([
        StructField("s", StringType(), True),   # Symbol (e.g., OANDA:EUR_USD)
        StructField("p", DoubleType(), True),   # Price
        StructField("v", DoubleType(), True),   # Volume (can be 0)
        StructField("t", DoubleType(), True)    # Timestamp (UNIX milliseconds)
    ])), True)
])

# ---- Read from Kafka ----
# Read streaming data mn Kafka topic "financial_data"
df = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
    .option("subscribe", "financial_data")
    .load())

# ---- Parse JSON ----
# Parse l-JSON data o extract l-fields
parsed_df = (df.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("parsed"))
    .select(explode(col("parsed.data")).alias("trade"))
    .select(
        col("trade.s").alias("symbol"),
        col("trade.p").alias("price"),
        col("trade.v").alias("volume"),
        from_unixtime(col("trade.t") / 1000).cast("timestamp").alias("timestamp")
    ))

# ---- Aggregation ----
# Aggregate l-data f-1-minute windows
# - Group by symbol o window (1 minute)
# - Calculate avg_price o total_volume
aggregated_df = (parsed_df
    .withWatermark("timestamp", "1 minute")  # Handle late data
    .groupBy(
        window(col("timestamp"), "1 minute").alias("window"),
        col("symbol")
    )
    .agg(
        avg("price").alias("avg_price"),
        sum("volume").alias("total_volume")
    )
    .select(
        col("symbol"),
        col("window.end").alias("window_end"),
        col("avg_price"),
        col("total_volume"),
        col("window.start").alias("window_start")
    ))

# ---- Sinks ----
# 1. Debug sink l-OANDA:EUR_USD (console)
parsed_df_with_log = (parsed_df.filter(col("symbol") == "OANDA:EUR_USD")
    .writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", False)
    .option("checkpointLocation", "/tmp/spark_checkpoint/debug_eurusd")
    .start())

# 2. Console sink l-kol l-data (debugging)
console_query = (parsed_df
    .writeStream
    .outputMode("append")
    .format("console")
    .option("truncate", False)
    .option("checkpointLocation", "/tmp/spark_checkpoint/console")
    .start())

# 3. Cassandra sink l-raw data (trades table)
cassandra_query = (parsed_df
    .writeStream
    .format("org.apache.spark.sql.cassandra")
    .option("keyspace", "financial_data")
    .option("table", "trades")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/spark_checkpoint/cassandra")
    .start())

# 4. Cassandra sink l-aggregated data (trade_aggregates table)
def write_to_cassandra_aggregates(batch_df, batch_id):
    # Write batch dyal aggregated data f-Cassandra
    batch_df.write \
        .format("org.apache.spark.sql.cassandra") \
        .option("keyspace", "financial_data") \
        .option("table", "trade_aggregates") \
        .mode("append") \
        .save()

cassandra_aggregates_query = (aggregated_df
    .writeStream
    .foreachBatch(write_to_cassandra_aggregates)
    .outputMode("update")
    .option("checkpointLocation", "/tmp/spark_checkpoint/aggregates")
    .start())

# ---- Await Termination ----
# T2akd l-streams t-ystmrru
spark.streams.awaitAnyTermination()



# from pyspark.sql import SparkSession
# from pyspark.sql.functions import from_json, col, explode, from_unixtime
# from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, ArrayType
# import os

# # Get environment variables
# KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
# CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "cassandra")

# # Initialize Spark Session
# spark = (SparkSession.builder
#     .appName("FinancialDataStreaming")
#     .config("spark.cassandra.connection.host", CASSANDRA_HOST)
#     .config("spark.cassandra.connection.port", "9042")
#     .config("spark.streaming.kafka.maxRatePerPartition", "100")
#     .getOrCreate())

# # Define schema for the incoming Kafka messages
# schema = StructType([
#     StructField("type", StringType(), True),
#     StructField("data", ArrayType(StructType([
#         StructField("s", StringType(), True),  # Symbol
#         StructField("p", DoubleType(), True),  # Price
#         StructField("v", DoubleType(), True),  # Volume (can be 0)
#         StructField("t", DoubleType(), True)   # Timestamp (UNIX milliseconds)
#     ])), True)
# ])

# # Read stream from Kafka
# df = (spark.readStream
#     .format("kafka")
#     .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
#     .option("subscribe", "financial_data")
#     .load())

# # Parse JSON data from Kafka
# parsed_df = (df.selectExpr("CAST(value AS STRING)")
#     .select(from_json(col("value"), schema).alias("parsed"))
#     .select(explode(col("parsed.data")).alias("trade"))
#     .select(
#         col("trade.s").alias("symbol"),
#         col("trade.p").alias("price"),
#         col("trade.v").alias("volume"),
#         from_unixtime(col("trade.t") / 1000).cast("timestamp").alias("timestamp")
#     ))

# # Add logging to debug OANDA:EUR_USD
# parsed_df_with_log = parsed_df.filter(col("symbol") == "OANDA:EUR_USD").writeStream \
#     .format("console") \
#     .outputMode("append") \
#     .option("truncate", False) \
#     .option("checkpointLocation", "/tmp/spark_checkpoint/debug_eurusd") \
#     .start()

# # Write to console for debugging
# console_query = (parsed_df.writeStream
#     .outputMode("append")
#     .format("console")
#     .option("truncate", False)
#     .option("checkpointLocation", "/tmp/spark_checkpoint/console")
#     .start())

# # Write stream to Cassandra
# cassandra_query = (parsed_df.writeStream
#     .format("org.apache.spark.sql.cassandra")
#     .option("keyspace", "financial_data")
#     .option("table", "trades")
#     .outputMode("append")
#     .option("checkpointLocation", "/tmp/spark_checkpoint/cassandra")
#     .start())

# # Await termination
# spark.streams.awaitAnyTermination()
