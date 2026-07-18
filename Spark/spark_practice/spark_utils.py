from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper

# Create SparkSession — the entry point
spark = (
    SparkSession.builder
    .appName("HelloSpark")
    .master("local[*]")           # use all cores on your laptop
    .config("spark.sql.shuffle.partitions", "4")   # reduce from default 200 for local dev
    .config("spark.ui.port", "4040")
    .getOrCreate()
)

# Reduce log noise
spark.sparkContext.setLogLevel("WARN")

# Create a DataFrame
data = [
    ("alice", 30, "Seattle"),
    ("bob", 25, "Portland"),
    ("carol", 45, "Seattle"),
    ("dave", 35, "Bellevue"),
]
df = spark.createDataFrame(data, schema=["name", "age", "city"])

df.printSchema()
df.show()

# A transformation and action
result = df.filter(col("age") > 28).select(upper(col("name")).alias("name_upper"), "city")
result.explain(True)   # ← this is the money shot — see all 4 Catalyst plans
result.show()

# Keep Spark UI alive so you can inspect it
input("Press Enter to exit and close Spark UI at http://localhost:4040 ...")

spark.stop()