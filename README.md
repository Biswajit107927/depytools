# depytools README — Corrected Project Structure

Replace the `## Project Structure` section in your README with:

---

## Project Structure

```
depytools/
│
├── python/
│   ├── level1/          # Core patterns — filtering, deduplication, aggregation
│   ├── level2/          # Intermediate — pivoting, merging, sliding windows
│   ├── level3/          # Advanced — OOP pipelines, generators, decorators
│   ├── level4/          # DE-specific — batch processing, streaming patterns
│   ├── Level5/          # Expert — system design patterns
│   └── Practice/        # Hands-on exercises and practice problems
│
├── SQL/
│   └── Chapter/
│       ├── QuestionsAndConcepts.md   # SQL interview questions & concept deep-dives
│       └── Syllabus.md               # Full SQL syllabus coverage map
│
├── Spark/
│   └── spark_concepts.md             # Apache Spark core concepts reference
│
├── AWS/
│   ├── AWSDECertification            # AWS Data Engineer certification overview
│   ├── 7DaysPlan                     # 7-day study plan
│   ├── Module1CheatSheet             # S3, Glue, Kinesis
│   ├── Module2CheatSheet             # Redshift, Athena, Lake Formation
│   ├── Module3                       # Data pipelines & orchestration
│   ├── Module4                       # Security & governance
│   ├── OverAllRev                    # Overall revision notes
│   └── QuestionBank1                 # Practice questions
│
└── README.md
```

---

## Also fix in the SQL Patterns section:

Replace:
```markdown
## SQL Patterns

Production-tested SQL patterns covering:
* **Window Functions** — ROW_NUMBER, RANK, LAG, LEAD, NTILE, running totals
* **JOINs** — INNER, LEFT, SELF, correlated subqueries
* **CTEs** — single, chained, recursive
* **NULL Handling** — COALESCE, NULLIF, IS NULL patterns
* **Date Functions** — DATEDIFF, DATEADD, EXTRACT, TO_CHAR
* **String Functions** — TRIM, REPLACE, SUBSTR, concatenation
```

With:
```markdown
## SQL Patterns

Comprehensive SQL reference covering interview questions and production concepts:

| Resource | Path | Description |
|----------|------|-------------|
| Questions & Concepts | `SQL/Chapter/QuestionsAndConcepts.md` | SQL interview questions with deep-dive explanations |
| Syllabus | `SQL/Chapter/Syllabus.md` | Full SQL topic coverage map |

Topics covered: Window Functions (ROW_NUMBER, RANK, LAG, LEAD, NTILE), JOINs (INNER, LEFT, SELF, correlated subqueries), CTEs (single, chained, recursive), NULL Handling (COALESCE, NULLIF), Date Functions, String Functions.
```

---

## Add new sections for Spark and AWS:

```markdown
## Spark Patterns

Core Apache Spark concepts reference for data engineers:

| Resource | Path | Description |
|----------|------|-------------|
| Spark Concepts | `Spark/spark_concepts.md` | RDDs, DataFrames, partitioning, shuffles, optimization |

---

## AWS Data Engineer Certification

Study materials for the AWS Certified Data Engineer - Associate exam:

| Resource | Path | Description |
|----------|------|-------------|
| Certification Overview | `AWS/AWSDECertification` | Exam blueprint and domains |
| 7-Day Study Plan | `AWS/7DaysPlan` | Structured prep schedule |
| Module 1 Cheat Sheet | `AWS/Module1CheatSheet` | S3, Glue, Kinesis |
| Module 2 Cheat Sheet | `AWS/Module2CheatSheet` | Redshift, Athena, Lake Formation |
| Module 3 | `AWS/Module3` | Data pipelines & orchestration |
| Module 4 | `AWS/Module4` | Security & governance |
| Overall Revision | `AWS/OverAllRev` | Comprehensive review notes |
| Question Bank | `AWS/QuestionBank1` | Practice questions |
```

---

## Additional fix: typo in folder name

Rename `AWS/Module2CheetSheet` → `AWS/Module2CheatSheet` (typo: "Cheet" → "Cheat")

```bash
cd depytools
git mv AWS/Module2CheetSheet AWS/Module2CheatSheet
git commit -m "fix: rename Module2CheetSheet -> Module2CheatSheet (typo)"
```
