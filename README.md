# depytools

> A curated library of production-grade Python and SQL patterns for Data Engineers.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

---

## Overview

**depytools** is a practical reference library of data engineering patterns — built and tested for real-world production use cases. Every pattern handles edge cases (None values, duplicates, empty lists) and is designed to be readable, reusable, and interview-ready.

This library covers the most common data transformation challenges faced by data engineers working with Python and SQL — from basic deduplication to advanced windowing, pivoting, and batch processing.

---

## Project Structure

```
depytools/
│
├── python/
│   ├── level1/          # Core patterns — filtering, deduplication, aggregation
│   ├── level2/          # Intermediate — pivoting, merging, sliding windows
│   ├── level3/          # Advanced — OOP pipelines, generators, decorators
│   └── level4/          # DE-specific — batch processing, streaming patterns
│
├── sql/
│   ├── window_functions.sql
│   ├── joins.sql
│   ├── ctes.sql
│   ├── string_functions.sql
│   ├── date_functions.sql
│   └── null_handling.sql
│
└── tests/
    └── test_level1.py
```

---

## Python Patterns

### Level 1 — Core Patterns

| Pattern | Description | File |
|---------|-------------|------|
| Deduplicate | Remove duplicates by key, skip None | `level1/deduplicate.py` |
| Filter | Filter dicts by field conditions | `level1/filter.py` |
| Aggregate | Transform and enrich dict fields | `level1/aggregate.py` |
| Sort + Top N | Sort by field, return top N | `level1/sort_topn.py` |
| Edge Cases | Handle None, missing, invalid data | `level1/edge_cases.py` |

### Level 2 — Intermediate Patterns

| Pattern | Description | File |
|---------|-------------|------|
| Group By + Sum | Group dicts by key, aggregate values | `level2/group_by.py` |
| Flatten Nested | Flatten lists within dicts | `level2/flatten.py` |
| Merge Lists | Join two lists of dicts by key | `level2/merge.py` |
| Running Total | Cumulative sum across records | `level2/running_total.py` |
| Find Duplicates | Identify and return duplicate records | `level2/duplicates.py` |
| Pivot | Pivot records into column-based structure | `level2/pivot.py` |
| Transpose | Convert column dict to list of row dicts | `level2/transpose.py` |
| Sliding Window | Rolling averages across sequences | `level2/sliding_window.py` |
| Two Pointer | Pair finding with two pointer technique | `level2/two_pointer.py` |
| Batch Processing | Split data into configurable batches | `level2/batch_processing.py` |

---

## Quick Start

```bash
git clone https://github.com/Biswajit107927/depytools.git
cd depytools
```

### Example — Deduplicate

```python
from python.level1.deduplicate import deduplicate

items = [
    {"id": "a1", "name": "laptop",  "amount": 999},
    {"id": "a2", "name": "phone",   "amount": 599},
    {"id": "a1", "name": "laptop",  "amount": 999},  # duplicate
    {"id": None, "name": "tablet",  "amount": 399},  # missing id
    {"id": "a3", "name": "mouse",   "amount": None},
]

result = deduplicate(items)
# Returns unique items — skips None keys, keeps first occurrence
```

### Example — Batch Processing

```python
from python.level2.batch_processing import batch

items = list(range(1, 11))
result = batch(items, batch_size=3)
# Returns [[1,2,3], [4,5,6], [7,8,9], [10]]
```

### Example — Running Total

```python
from python.level2.running_total import running_total

transactions = [
    {"id": "t1", "amount": 100},
    {"id": "t2", "amount": 250},
    {"id": "t3", "amount": 75},
]

result = running_total(transactions)
# Adds running_total field to each record
```

---

## SQL Patterns

Production-tested SQL patterns covering:

- **Window Functions** — ROW_NUMBER, RANK, LAG, LEAD, NTILE, running totals
- **JOINs** — INNER, LEFT, SELF, correlated subqueries
- **CTEs** — single, chained, recursive
- **NULL Handling** — COALESCE, NULLIF, IS NULL patterns
- **Date Functions** — DATEDIFF, DATEADD, EXTRACT, TO_CHAR
- **String Functions** — TRIM, REPLACE, SUBSTR, concatenation

### Example — NULL Handling

```sql
-- Replace NULL commission with 0, calculate total comp
SELECT
    name,
    salary,
    COALESCE(commission, 0) AS commission,
    salary + COALESCE(commission, 0) AS total_comp
FROM employees;
```

### Example — Running Total with Window Function

```sql
SELECT
    emp_id,
    sale_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY dept_id
        ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM sales;
```

---

## Design Principles

Every pattern in this library follows these rules:

```
✅ Handle None/NULL values explicitly
✅ Handle empty lists gracefully
✅ Use .get() for safe dict access
✅ Return consistent data structures
✅ No side effects on input data
✅ Readable over clever
```

---

## Related Projects

- [data-platform-quicksight](https://github.com/Biswajit107927/data-platform-quicksight) — Event-driven QuickSight data catalog automation using Amazon Bedrock and MCP server architecture

---

## Author

**Biswajit Praharaj** — Senior Data Engineer  
10+ years at Amazon | AWS | Spark | Airflow | dbt  
[LinkedIn](https://linkedin.com/in/biswajit) | [GitHub](https://github.com/Biswajit107927)

---

## License

MIT License — free to use, modify, and distribute.
