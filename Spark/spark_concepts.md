# PySpark Conceptual Interview Questions

> A reference of the most common conceptual PySpark questions asked in
> Senior / Staff Data Engineer interviews. Focused on **mechanisms, trade-offs,
> and when *not* to use** — the framing that distinguishes senior from junior
> answers.

**Author:** Biswajit Praharaj
**Last updated:** May 2026
**Companion repo:** [depytools](https://github.com/Biswajit107927/depytools)

---

## Why this exists

Most Spark interview prep focuses on syntax. But senior interviews probe
*reasoning*: do you know the mechanism, can you name the trade-off, do you
know when something doesn't apply?

Every answer here follows the same shape:

1. **Define** the concept precisely
2. **Name the mechanism** — what's actually happening under the hood
3. **State the trade-off** — what you're paying for the benefit
4. **Name the caveat** — when *not* to use it

That four-beat structure is what makes an answer sound senior.

---

## Table of contents

**Core 10 (must-know)**

1. [Transformations vs Actions (lazy evaluation)](#1-transformations-vs-actions-lazy-evaluation)
2. [Sort-merge vs Broadcast joins](#2-sort-merge-vs-broadcast-joins)
3. [What is a shuffle and why is it expensive?](#3-what-is-a-shuffle-and-why-is-it-expensive)
4. [Catalyst optimizer](#4-catalyst-optimizer)
5. [Adaptive Query Execution (AQE)](#5-adaptive-query-execution-aqe)
6. [Data skew and how to handle it](#6-data-skew-and-how-to-handle-it)
7. [`cache()` and `persist()`](#7-cache-and-persist)
8. [DataFrame vs RDD](#8-dataframe-vs-rdd)
9. [Partitioning — runtime and storage](#9-partitioning--runtime-and-storage)
10. [Debugging a slow Spark job](#10-debugging-a-slow-spark-job)

**Extended 11–20 (likely with deep interviewers)**

11. [`cache`, `persist`, `checkpoint` — the differences](#11-cache-persist-checkpoint--the-differences)
12. [Narrow vs wide transformations](#12-narrow-vs-wide-transformations)
13. [Tungsten execution engine](#13-tungsten-execution-engine)
14. [Spark stages and the DAG](#14-spark-stages-and-the-dag)
15. [`coalesce` vs `repartition`](#15-coalesce-vs-repartition)
16. [Reading `.explain()` output](#16-reading-explain-output)
17. [Schema evolution in Iceberg / Delta](#17-schema-evolution-in-iceberg--delta)
18. [Spark Streaming vs Structured Streaming](#18-spark-streaming-vs-structured-streaming)
19. [Partition pruning vs predicate pushdown](#19-partition-pruning-vs-predicate-pushdown)
20. [Handling out-of-memory errors](#20-handling-out-of-memory-errors)

**Appendix**

- [The senior-answer pattern](#the-senior-answer-pattern)
- [What interviewers are actually listening for](#what-interviewers-are-actually-listening-for)

---

# Core 10

## 1. Transformations vs Actions (lazy evaluation)

**Q:** *What's the difference between transformations and actions, and why does it matter?*

Transformations are **lazy** — they don't execute, they just build up a logical
plan. Examples: `filter`, `select`, `groupBy`, `join`, `withColumn`.

Actions trigger execution — `show`, `count`, `collect`, `write`, `take`.

**Why it matters:** laziness is what lets Spark's Catalyst optimizer see the
*whole pipeline* before running it. It can rearrange filters (predicate
pushdown), prune columns, and pick join strategies based on the full plan.
If transformations ran eagerly, none of that optimization would be possible.

**Common gotcha:** writing `df.filter(...)` without reassigning. The result
is a new DataFrame; the original is unchanged. Either reassign
(`df = df.filter(...)`) or chain (`df.filter(...).show()`).

---

## 2. Sort-merge vs Broadcast joins

**Q:** *Walk me through what happens in a join. When would you choose sort-merge vs broadcast?*

**Sort-merge join** is the default for large-large joins. Spark shuffles both
DataFrames across the network by the join key, sorts each partition, then
merges. Expensive because of network I/O and disk spill on shuffle.

**Broadcast join** is for small-large joins. Wrap the small side with
`F.broadcast()` — Spark ships a full copy of the small table to every
executor's memory, and the large table never moves. Each executor joins its
local slice against the in-memory copy.

```python
from pyspark.sql import functions as F

# Customers (~10K rows) joined to orders (~50M rows)
result = orders.join(F.broadcast(customers), "customer_id", "inner")
```

**Trade-off:** broadcast trades a small amount of memory on every executor
for eliminating the shuffle of the big table.

**Caveat:** if the "small" side isn't actually small (a few hundred MB),
broadcasting risks executor OOM. Spark's auto-broadcast threshold defaults
around 10MB (`spark.sql.autoBroadcastJoinThreshold`); tune up for small
dimension tables, but never blindly broadcast.

---

## 3. What is a shuffle and why is it expensive?

**Q:** *What is a shuffle, and why is it the most expensive operation in Spark?*

A shuffle is when Spark **redistributes data across executors by key** — for
operations that need data with the same key to land together: `groupBy`,
`join`, `distinct`, `repartition`.

It's expensive because it involves:

- **Serialization** of data on the sender side
- **Network transfer** between executors
- **Disk spill** if partitions don't fit in memory
- **Synchronization** — the next stage can't start until the shuffle completes

Shuffles are the biggest cost in most Spark jobs. The optimizations are:

- **Avoid them when possible** — broadcast joins instead of sort-merge
- **Reduce data before them** — filter early, project columns early
- **Tune `spark.sql.shuffle.partitions`** — the default 200 is wrong for most
  workloads; aim for partitions of ~100–200MB

---

## 4. Catalyst optimizer

**Q:** *What is Catalyst, and what does it do?*

Catalyst is Spark's **query optimizer**. When you write DataFrame code, Spark
builds a logical plan from your transformations, then Catalyst applies
optimizations:

- **Predicate pushdown** — moves filters as close to the source as possible
- **Column pruning** — only reads columns you actually use
- **Constant folding** — evaluates constant expressions at plan time
- **Join reordering** — picks an efficient join order
- **Physical join strategy** — decides sort-merge vs broadcast vs shuffle-hash

That's why DataFrame API outperforms raw RDDs — RDDs are opaque to Catalyst,
but DataFrame operations are inspectable, so the optimizer can rewrite the
plan.

**Practical tip:** call `.explain()` on any DataFrame to see the physical
plan Catalyst produced.

```python
result = orders.join(F.broadcast(customers), "customer_id", "inner")
result.explain()  # see the plan
```

---

## 5. Adaptive Query Execution (AQE)

**Q:** *What is AQE, and why does it matter?*

AQE is Spark's **runtime adaptive optimization**, introduced in Spark 3.0. The
original Catalyst optimizes the plan once, *before* execution, based on
statistics. AQE optimizes *during* execution, using actual runtime data.

Three things it does that matter:

1. **Dynamically coalesces shuffle partitions** — fewer, larger partitions
   when actual data is smaller than estimated
2. **Dynamically switches join strategies** — promoting a sort-merge to a
   broadcast join if the small side is actually small at runtime
3. **Handles skew automatically** — splits heavy partitions

Enable it with:

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

In modern Spark versions it's on by default. Most jobs run faster with no
code changes.

---

## 6. Data skew and how to handle it

**Q:** *What is data skew, and how do you handle it?*

Skew is when **one or a few keys dominate the data** — say 60% of all
transactions belong to one customer. When you group or join by that key, one
executor gets all the work while others sit idle. The job's runtime is
bottlenecked on that one task.

**Three approaches:**

1. **AQE skew handling** — detects skewed partitions and splits them
   automatically. Often enough.
2. **Salting** — append a random suffix to the skewed key, pre-aggregate,
   then remove the salt and finalize. Disperses load.
3. **Isolate the heavy key** — process the skewed key separately from the
   rest, then union results.

**Diagnosis:** if one task in a stage runs 10× longer than the others,
that's skew. The Spark UI's task duration histogram tells you immediately.

---

## 7. `cache()` and `persist()`

**Q:** *When and why would you cache a DataFrame?*

Cache the result of an expensive transformation when you'll **reuse it
multiple times** in the same job. Without caching, every action recomputes
from the source.

```python
df_clean = expensive_transform(df_raw)
df_clean.cache()           # next reuse won't recompute

df_clean.filter(...).show()
df_clean.groupBy(...).agg(...).show()
```

`cache()` is shorthand for `persist(MEMORY_AND_DISK)`. `persist()` lets you
pick: `MEMORY_ONLY`, `MEMORY_AND_DISK`, `DISK_ONLY`, with optional
serialization. For most cases the default is fine.

**When NOT to cache:**

- Used once → never
- Cheap to recompute → never
- Tight memory → caching causes evictions and slows jobs down

Always `unpersist()` when done if memory is tight.

---

## 8. DataFrame vs RDD

**Q:** *When would you ever use RDDs over DataFrames?*

**Almost never, in modern Spark.** DataFrames win because Catalyst can
optimize them — predicate pushdown, column pruning, code generation via
Tungsten. RDDs are opaque to the optimizer, so you give up all of that.

Remaining RDD use cases are narrow:

- Extremely fine-grained control over partitioning that DataFrame API can't express
- Custom serialization
- Legacy code

For 95% of work — and for anything Auger-shaped — reach for DataFrame.

---

## 9. Partitioning — runtime and storage

**Q:** *How do you partition data, and why does it matter?*

Two different things go by "partitioning":

**Runtime partitioning** (how data is distributed across executors during
execution):

- `spark.sql.shuffle.partitions` controls partition count after shuffles
- Default 200 is often wrong — too many for small data, too few for big data
- Tune to roughly match cluster cores or aim for ~100–200MB per partition

**Storage partitioning** (how data is laid out on disk):

```python
df.write.partitionBy("region").parquet("s3://bucket/path/")
# writes separate folders per region
```

Critical for query performance — if downstream readers filter by region,
predicate pushdown reads only the relevant folders. Without it, every query
scans everything.

**Anti-pattern:** partitioning by a high-cardinality column like `user_id` —
you get millions of tiny files and metadata overhead destroys performance.
Partition by low-to-medium cardinality columns that are common filter
predicates.

---

## 10. Debugging a slow Spark job

**Q:** *How do you debug a slow Spark job?*

Three places to look, in order:

**1. Spark UI's stage view.** Look for stages with long task duration.

- One task much longer than the others → **skew**
- All tasks slow → data volume or insufficient parallelism

**2. `.explain()` on the DataFrame.** Verify Catalyst is doing what you expect:

- Predicates being pushed down (`PushedFilters` in the file scan)
- Columns being pruned
- Right join strategy chosen (e.g., `BroadcastHashJoin`, not `SortMergeJoin`)

If a join shows as `SortMergeJoin` but you expected `BroadcastHashJoin`,
that's a finding — maybe the small table isn't being recognized as small.

**3. Shuffle metrics:**

- Large shuffle writes → lots of data crossing the network → reduce or
  broadcast
- Large spills → partitions don't fit in memory → repartition or add executor
  memory

**Common fixes:** broadcast a dimension table, filter earlier, repartition
by the right key, enable AQE, or — last resort — add executor memory.

---

# Extended 11–20

## 11. `cache`, `persist`, `checkpoint` — the differences

**Q:** *What's the difference between `cache()`, `persist()`, and `checkpoint()`?*

- **`cache()` / `persist()`** — store the DataFrame in memory or memory+disk
  for reuse. **Lineage is preserved.** If a partition is lost, Spark recomputes
  it from the lineage.
- **`checkpoint()`** — physically writes the DataFrame to reliable storage
  (HDFS, S3) and **truncates the lineage**.

**When to checkpoint:**

- Lineage is so long that recomputation would be expensive
- Iterative algorithms (graph processing, ML) where the DAG grows unboundedly

**Quick rule:** cache for reuse, checkpoint to break lineage.

---

## 12. Narrow vs wide transformations

**Q:** *What's the difference between narrow and wide transformations?*

**Narrow:** each output partition depends on only one input partition. No
data movement between executors. Cheap.

- `map`, `filter`, `select`, `withColumn`

**Wide:** output partitions depend on multiple input partitions. Requires a
**shuffle**, which is expensive. Wide transformations create stage boundaries
in the Spark DAG.

- `groupBy`, `join`, `distinct`, `repartition`, `orderBy`

**Heuristic:** do as much narrow work as possible before wide. Filter and
project before you join or group. Catalyst tries to do this automatically
via predicate pushdown, but writing it correctly helps.

---

## 13. Tungsten execution engine

**Q:** *What is Tungsten?*

Tungsten is Spark's execution engine underneath Catalyst. Three things it
does:

1. **Off-heap memory management** — avoids JVM garbage collection overhead
2. **Cache-aware computation** — designs operations around CPU cache hierarchies
3. **Whole-stage code generation** — compiles a sequence of operators into a
   single optimized Java function at runtime

**Practical effect:** DataFrame operations run much faster than the
equivalent RDD code. Visible in `.explain()` as operators wrapped in
`WholeStageCodegen`. Tungsten is the reason Spark SQL is competitive with
vendor databases on benchmark workloads.

---

## 14. Spark stages and the DAG

**Q:** *What is a Spark stage, and how do you read the DAG?*

A **stage** is a unit of work that runs without a shuffle — a sequence of
narrow transformations on the same partition. Wide transformations create
stage boundaries.

Execution hierarchy:

- A **job** has stages
- A **stage** has tasks
- **Tasks** are what executors run in parallel — one task per partition per stage

Reading the DAG in the Spark UI — each stage shows:

- Task count
- Duration distribution
- Shuffle read/write size

**Signals:**

- One task much longer than the rest → skew
- Thousands of tiny tasks → partitions too small

---

## 15. `coalesce` vs `repartition`

**Q:** *When do you use `coalesce` vs `repartition`?*

Both change partition count, but the mechanism differs:

- **`repartition(n)`** — triggers a **full shuffle**. Can increase or decrease
  partitions. Produces evenly-distributed partitions. Expensive but balanced.
- **`coalesce(n)`** — only **reduces** partitions, and does it **without a
  full shuffle** by merging existing partitions on the same executor. Cheap,
  but result can be unbalanced if source partitions were uneven.

**Rule:**

- `coalesce` — reducing partition count after a heavy filter (200 → 20)
  before writing
- `repartition` — need balanced partitions, or increasing partition count

**Classic mistake:** `repartition(1)` to write a single output file — for
big data it shuffles everything to one executor and dies. Better: filter to
the small final result, then `coalesce(1)`.

---

## 16. Reading `.explain()` output

**Q:** *What does `.explain()` show you, and what do you look for?*

It prints the execution plan Spark will use. Four levels — parsed, analyzed,
optimized, and physical. The **physical plan** is what actually runs.

**What to look for:**

- **Join strategy chosen** — `BroadcastHashJoin`, `SortMergeJoin`, `ShuffleHashJoin`
- **Filters pushed down** — `PushedFilters` in the file scan node
- **Unused columns pruned**
- **Stages in `WholeStageCodegen`**

**Useful variants:**

```python
df.explain()              # default — physical plan only
df.explain(True)          # all four levels
df.explain("formatted")   # cleaner tree
df.explain("cost")        # estimated row counts
```

Most underused debugging tool in Spark.

---

## 17. Schema evolution in Iceberg / Delta

**Q:** *How does schema evolution work in Iceberg or Delta Lake, and why does it matter?*

Both Iceberg and Delta Lake support schema evolution at the **table format
level** — you can add columns, drop columns, reorder them, or change column
types **without rewriting the entire table**. Old data files keep their
original schema; the table format maintains metadata that maps logical
columns to physical files.

**Why it matters for ingestion pipelines:** source schemas drift constantly.
Without table-level schema evolution, every schema change requires a full
table rewrite — doesn't scale to TB-sized tables. With Iceberg, adding a
column to a 10TB table is a metadata operation — milliseconds.

**Iceberg-specific:** hidden partitioning means the partition strategy can
change over time without breaking historical queries. Operational
flexibility you don't have with plain Parquet on S3.

---

## 18. Spark Streaming vs Structured Streaming

**Q:** *What's the difference between Spark Streaming and Structured Streaming?*

- **Spark Streaming (legacy)** — micro-batch based on RDDs. You write batch
  logic via the DStream API; Spark processes the stream as a series of small
  batches.
- **Structured Streaming (modern)** — uses the DataFrame/Dataset API. You
  write a query as if against a static table; Spark treats incoming data as
  an unbounded table that grows. Same code can run as batch or stream.

**Use Structured Streaming for anything new** — better API, exactly-once
semantics with checkpointing, Catalyst integration. Spark Streaming is
legacy; touch only for existing code.

---

## 19. Partition pruning vs predicate pushdown

**Q:** *What's the difference between partition pruning and predicate pushdown?*

Both reduce data read at the source, but at different layers:

**Partition pruning** — based on how data is **laid out on disk**. If a
Parquet dataset is partitioned by `year`/`month`, and the query filters
`year = 2024`, Spark only reads files in the `year=2024/` directories.
Other partitions never get touched.

**Predicate pushdown** — pushes filter conditions **into the file scan
itself**. For Parquet, filters use min/max stats stored in row group
metadata to skip entire row groups without reading them. Iceberg and Delta
extend this to file-level statistics — Spark can skip whole files.

Together they're how a Spark query against a 100TB table can read 10MB and
return in seconds. Visible in `.explain()` as `PartitionFilters` and
`PushedFilters`.

---

## 20. Handling out-of-memory errors

**Q:** *How do you handle out-of-memory errors in Spark?*

OOM in Spark usually means one of three things:

1. **Executor heap too small** for the partition size
2. **A partition is genuinely huge** due to skew
3. **A broadcast that shouldn't have been broadcast** — the "small" side
   wasn't small

**Diagnosis flow:**

- Check the Spark UI for the failed task — what was the partition size?
- One partition 10× the median → **skew** → AQE skew handling or salting
- All partitions large → repartition to smaller chunks
- Broadcast failure → check whether the small side exceeded the threshold

**Last resort:** increase executor memory. But that's the lazy fix. Usually
the right fix is reducing partition size, not throwing more memory at it.
Add memory only after you've understood *why*.

---

# Appendix

## The senior-answer pattern

Every answer in this doc follows the same four-beat shape. Memorize the
shape, not the words:

1. **Define** the concept precisely (no buzzwords, no hand-waving)
2. **Name the mechanism** — what's actually happening
3. **State the trade-off** — what you're paying for the benefit
4. **Name the caveat** — when *not* to use it

**Junior:** "Broadcast joins are faster."
**Senior:** "Broadcast trades a copy in each executor's memory for eliminating the shuffle of the big table — but only if the small side is actually small. Otherwise you risk executor OOM."

Same fact. Completely different signal.

## What interviewers are actually listening for

When a senior interviewer asks a conceptual Spark question, they're
checking four things:

- Do you know the **mechanism**, or just the **buzzword**?
- Do you name **trade-offs** unprompted?
- Can you connect concept → **decision**?
  ("So if I had a 50M-row table and a 10K-row dimension, I'd broadcast.")
- Do you know when something **doesn't apply**?

Hit those four and the answer reads senior every time.

---

*End of reference.*