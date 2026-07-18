"""
Generate sample e-commerce datasets for Spark practice.
Run this ONCE. It creates Parquet files under ./data/
"""
import os
import sys

# Make driver and worker use the same Python
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, expr, rand, when, lit, to_date, date_add, concat, floor
)

spark = (
    SparkSession.builder
    .appName("GenerateSampleData")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# Output directory
OUT = "./data"
os.makedirs(OUT, exist_ok=True)

# ============================================================
# 1. USERS — 100,000 users, dimension table (small, joinable)
# ============================================================
print("Generating users...")
users = (
    spark.range(1, 100_001).withColumnRenamed("id", "user_id")
    .withColumn("age",
                (rand(seed=1) * 60 + 18).cast("int"))          # 18-77
    .withColumn("country",
                when(rand(seed=2) < 0.60, "US")
                .when(rand(seed=2) < 0.75, "IN")
                .when(rand(seed=2) < 0.85, "UK")
                .when(rand(seed=2) < 0.92, "DE")
                .otherwise("BR"))
    .withColumn("signup_date",
                date_add(to_date(lit("2020-01-01")),
                         (rand(seed=3) * 1825).cast("int")))    # 5-year range
    .withColumn("is_premium",
                when(rand(seed=4) < 0.15, True).otherwise(False))
    .withColumn("email",
                concat(lit("user_"), col("user_id"), lit("@example.com")))
)
users.write.mode("overwrite").parquet(f"{OUT}/users")
print(f"  wrote {users.count():,} users")

# ============================================================
# 2. PRODUCTS — 5,000 products, dimension table
# ============================================================
print("Generating products...")
categories = ["Electronics", "Clothing", "Books", "Home", "Sports", "Beauty", "Toys"]

products = (
    spark.range(1, 5_001).withColumnRenamed("id", "product_id")
    .withColumn("category_idx", (rand(seed=10) * len(categories)).cast("int"))
    .withColumn("category",
                expr(f"element_at(array({','.join([repr(c) for c in categories])}), category_idx + 1)"))
    .drop("category_idx")
    .withColumn("price",
                (rand(seed=11) * 500 + 5).cast("decimal(10,2)"))    # $5 - $505
    .withColumn("brand",
                concat(lit("Brand_"), (rand(seed=12) * 100).cast("int")))
    .withColumn("in_stock",
                when(rand(seed=13) < 0.9, True).otherwise(False))
)
products.write.mode("overwrite").parquet(f"{OUT}/products")
print(f"  wrote {products.count():,} products")

# ============================================================
# 3. ORDERS — 2,000,000 orders. Big fact table. SKEWED on user.
# One user (user_id=1) has 5% of all orders (aka the "power user").
# This is realistic — most e-commerce data has whales.
# ============================================================
print("Generating orders (this takes ~30 sec)...")
orders = (
    spark.range(1, 2_000_001).withColumnRenamed("id", "order_id")
    # INTENTIONAL SKEW: 5% of orders go to user_id=1
    .withColumn("user_id",
                when(rand(seed=20) < 0.05, lit(1))
                .otherwise((rand(seed=21) * 99_999 + 2).cast("int")))
    .withColumn("order_date",
                date_add(to_date(lit("2024-01-01")),
                         (rand(seed=22) * 365).cast("int")))
    .withColumn("status",
                when(rand(seed=23) < 0.85, "completed")
                .when(rand(seed=23) < 0.95, "shipped")
                .otherwise("cancelled"))
    .withColumn("total_amount",
                (rand(seed=24) * 300 + 10).cast("decimal(10,2)"))
)
orders.write.mode("overwrite").parquet(f"{OUT}/orders")
print(f"  wrote {orders.count():,} orders")

# ============================================================
# 4. ORDER_ITEMS — line items. ~5M rows. Each order has 1-5 items.
# This is your practice ground for joins and aggregations.
# ============================================================
print("Generating order_items (this takes ~30 sec)...")
# Each order gets 1-5 items via explode
order_items = (
    spark.range(1, 2_000_001).withColumnRenamed("id", "order_id")
    .withColumn("num_items", (rand(seed=30) * 4 + 1).cast("int"))
    .withColumn("item_seq", expr("sequence(1, num_items)"))
    .withColumn("item_num", expr("explode(item_seq)"))
    .drop("num_items", "item_seq")
    .withColumn("product_id", (rand(seed=31) * 4_999 + 1).cast("int"))
    .withColumn("quantity", (rand(seed=32) * 4 + 1).cast("int"))
    .withColumn("unit_price", (rand(seed=33) * 200 + 5).cast("decimal(10,2)"))
    .withColumn("item_id",
                concat(col("order_id"), lit("_"), col("item_num")))
    .select("item_id", "order_id", "product_id", "quantity", "unit_price")
)
order_items.write.mode("overwrite").parquet(f"{OUT}/order_items")
print(f"  wrote {order_items.count():,} order_items")

# ============================================================
# 5. EVENTS — clickstream / page views. 10M rows.
# For streaming + window function practice. Contains nulls
# and dirty data on purpose.
# ============================================================
print("Generating events (this takes ~45 sec)...")
event_types = ["page_view", "add_to_cart", "purchase", "search", "logout"]

events = (
    spark.range(1, 10_000_001).withColumnRenamed("id", "event_id")
    .withColumn("user_id",
                when(rand(seed=40) < 0.02, lit(None))              # 2% nulls
                .otherwise((rand(seed=41) * 99_999 + 1).cast("int")))
    .withColumn("event_type_idx", (rand(seed=42) * len(event_types)).cast("int"))
    .withColumn("event_type",
                expr(f"element_at(array({','.join([repr(e) for e in event_types])}), event_type_idx + 1)"))
    .drop("event_type_idx")
    # FIX: build timestamp using PySpark functions instead of a SQL expression
    .withColumn("random_offset_sec", (rand(seed=43) * 31_536_000).cast("long"))   # seconds in a year
    .withColumn("event_ts",
                expr("cast(unix_timestamp(to_timestamp('2024-01-01')) + random_offset_sec as timestamp)"))
    .drop("random_offset_sec")
    .withColumn("session_id",
                concat(lit("sess_"), (rand(seed=44) * 500_000).cast("int")))
    .withColumn("page_url",
                concat(lit("/products/"), (rand(seed=45) * 4_999 + 1).cast("int")))
)
events.write.mode("overwrite").parquet(f"{OUT}/events")
print(f"  wrote {events.count():,} events")

print("\n=== DONE ===")
print(f"Data written to: {os.path.abspath(OUT)}")
print("\nSummary:")
for name in ["users", "products", "orders", "order_items", "events"]:
    path = f"{OUT}/{name}"
    size_mb = sum(
        os.path.getsize(os.path.join(dp, f))
        for dp, _, files in os.walk(path)
        for f in files
    ) / 1024 / 1024
    print(f"  {name:15} → {path}  ({size_mb:.1f} MB)")

spark.stop()