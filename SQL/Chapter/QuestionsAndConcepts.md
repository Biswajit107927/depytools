# SQL Practice Bank — Biswajit Praharaj
# Complete Question Bank with Sample Data

---

## DATASET REFERENCE

### employees table
```sql
| emp_id | name    | manager_id | dept_id | salary | hire_date  | level |
|--------|---------|------------|---------|--------|------------|-------|
| e001   | Alice   | NULL       | d01     | 95000  | 2020-01-15 | 1     |
| e002   | Bob     | e001       | d01     | 85000  | 2019-03-20 | 2     |
| e003   | Charlie | e001       | d01     | 120000 | 2018-07-10 | 2     |
| e004   | Diana   | e002       | d02     | 98000  | 2021-05-01 | 3     |
| e005   | Eve     | e002       | d02     | 72000  | 2022-09-15 | 3     |
| e006   | Frank   | e003       | d02     | 115000 | 2019-01-10 | 3     |
| e007   | Grace   | e004       | d03     | 92000  | 2020-11-20 | 4     |
| e008   | Henry   | e004       | d03     | 105000 | 2019-08-05 | 4     |
```

### sales table
```sql
| sale_id | emp_id | amount | sale_date  |
|---------|--------|--------|------------|
| s001    | e001   | 1200   | 2024-01-15 |
| s002    | e001   | 800    | 2024-02-20 |
| s003    | e002   | 1500   | 2024-01-10 |
| s004    | e002   | 900    | 2024-03-15 |
| s005    | e003   | 2000   | 2024-02-01 |
| s006    | e003   | 1100   | 2024-03-20 |
```

---

## TOPIC 1 — WINDOW FUNCTIONS

### ROW_NUMBER, RANK, DENSE_RANK

**Q1: Rank employees by salary within department**
```sql
SELECT
    name,
    dept_id,
    salary,
    ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS row_num,
    RANK()       OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dense_rnk
FROM employees;
```

**Q2: Top 2 earners per department**
```sql
WITH CTE AS (
    SELECT name, dept_id, salary,
           ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn
    FROM employees
)
SELECT * FROM CTE WHERE rn <= 2;
```

### LAG / LEAD

**Q3: Show each employee salary vs previous employee salary**
```sql
SELECT
    name,
    salary,
    LAG(salary)  OVER (PARTITION BY dept_id ORDER BY salary DESC) AS prev_salary,
    LEAD(salary) OVER (PARTITION BY dept_id ORDER BY salary DESC) AS next_salary,
    salary - LAG(salary) OVER (PARTITION BY dept_id ORDER BY salary DESC) AS diff
FROM employees;
```

### SUM OVER / AVG OVER

**Q4: Running total of salary by department**
```sql
SELECT
    name,
    dept_id,
    salary,
    SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary DESC
                      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM employees;
```

**Q5: Each employee salary vs dept average vs company average**
```sql
SELECT
    name,
    salary,
    AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg,
    AVG(salary) OVER ()                     AS company_avg
FROM employees;
```

### FIRST_VALUE / LAST_VALUE

**Q6: Highest salary in department for each row**
```sql
SELECT
    name,
    dept_id,
    salary,
    FIRST_VALUE(salary) OVER (
        PARTITION BY dept_id
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS highest_in_dept
FROM employees;
```

**Q7: Lowest salary in department for each row**
```sql
SELECT
    name,
    dept_id,
    salary,
    LAST_VALUE(salary) OVER (
        PARTITION BY dept_id
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_in_dept
FROM employees;
```

**Q8: Salary difference from highest in dept**
```sql
SELECT
    name,
    salary,
    FIRST_VALUE(salary) OVER (
        PARTITION BY dept_id ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS highest,
    FIRST_VALUE(salary) OVER (
        PARTITION BY dept_id ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) - salary AS difference
FROM employees;
```

### ROWS BETWEEN

**Q9: Running average salary within department**
```sql
SELECT
    name,
    dept_id,
    salary,
    AVG(salary) OVER (
        PARTITION BY dept_id
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_avg
FROM employees;
```

### NTILE

**Q10: Divide employees into 4 salary quartiles**
```sql
SELECT
    name,
    salary,
    NTILE(4) OVER (ORDER BY salary DESC) AS quartile
FROM employees;
```

---

## TOPIC 2 — CTEs

### Single CTE

**Q11: Departments where avg salary > company average**
```sql
WITH dept_avg AS (
    SELECT dept_id, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY dept_id
),
company_avg AS (
    SELECT AVG(salary) AS company_avg
    FROM employees
)
SELECT d.dept_id, d.avg_sal, c.company_avg
FROM dept_avg d
CROSS JOIN company_avg c
WHERE d.avg_sal > c.company_avg;
```

### Recursive CTE

**Q12: Show all employees under Alice (all levels)**
```sql
WITH CTE1 AS (
    SELECT emp_id, name, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e2.emp_id, e2.name, c.depth + 1
    FROM employees e2
    JOIN CTE1 c ON e2.manager_id = c.emp_id
)
SELECT * FROM CTE1;
```

**Q13: Show full path from root to each employee**
```sql
WITH CTE1 AS (
    SELECT emp_id, name, name AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e2.emp_id, e2.name,
           c.path || ' → ' || e2.name AS path
    FROM employees e2
    JOIN CTE1 c ON e2.manager_id = c.emp_id
)
SELECT name, path FROM CTE1;
```

**Q14: Count all reports (direct + indirect) per manager**
```sql
WITH hierarchy AS (
    SELECT emp_id AS ancestor_id, emp_id AS descendant_id
    FROM employees
    UNION ALL
    SELECT h.ancestor_id, e.emp_id
    FROM employees e
    JOIN hierarchy h ON e.manager_id = h.descendant_id
),
report_counts AS (
    SELECT ancestor_id, COUNT(*) - 1 AS total_reports
    FROM hierarchy
    GROUP BY ancestor_id
    HAVING COUNT(*) > 1
)
SELECT e.name, r.total_reports
FROM report_counts r
JOIN employees e ON r.ancestor_id = e.emp_id
ORDER BY total_reports DESC;
```

**Q15: Show employees at depth level 3**
```sql
WITH CTE AS (
    SELECT emp_id, name, 1 AS depth
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e2.emp_id, e2.name, c.depth + 1
    FROM employees e2
    JOIN CTE c ON e2.manager_id = c.emp_id
)
SELECT * FROM CTE WHERE depth = 3;
```

**Q16: Total employees at each depth level**
```sql
WITH CTE AS (
    SELECT emp_id, name, 1 AS depth
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e2.emp_id, e2.name, c.depth + 1
    FROM employees e2
    JOIN CTE c ON e2.manager_id = c.emp_id
)
SELECT depth, COUNT(emp_id) AS employee_count
FROM CTE
GROUP BY depth
ORDER BY depth;
```

**Q17: Show leaf nodes (no direct reports)**
```sql
SELECT emp_id, name
FROM employees
WHERE emp_id NOT IN (
    SELECT DISTINCT manager_id
    FROM employees
    WHERE manager_id IS NOT NULL
);
```

---

## TOPIC 3 — JOINS

### SELF JOIN

**Q18: Show each employee with their manager name**
```sql
SELECT
    e1.name AS employee,
    COALESCE(e2.name, 'No Manager') AS manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.emp_id;
```

**Q19: Show managers with count of direct reports**
```sql
WITH CTE AS (
    SELECT e.emp_id, e.name,
           e2.name AS manager
    FROM employees e
    JOIN employees e2 ON e.manager_id = e2.emp_id
)
SELECT manager, COUNT(*) AS direct_reports
FROM CTE
GROUP BY manager;
```

---

## TOPIC 4 — NULL HANDLING

**Q20: Replace NULL salary with 0, NULL commission with 'No Commission'**
```sql
SELECT
    name,
    COALESCE(salary, 0) AS salary,
    COALESCE(TO_CHAR(commission), 'No Commission') AS commission,
    COALESCE(salary, 0) + COALESCE(commission, 0) AS total_comp
FROM employees;
```

---

## TOPIC 5 — STRING FUNCTIONS

**Q21: Show employees whose name starts with a vowel**
```sql
SELECT
    UPPER(name) AS name,
    LENGTH(name) AS name_length
FROM employees
WHERE LEFT(LOWER(name), 1) IN ('a', 'e', 'i', 'o', 'u');
```

---

## TOPIC 6 — DATE FUNCTIONS

**Q22: Show employees hired in last 3 years with years of service**
```sql
SELECT
    name,
    hire_date,
    DATEDIFF('year', hire_date, SYSDATE) AS years_of_service
FROM employees
WHERE hire_date >= DATEADD('year', -3, SYSDATE);
```

---

## TOPIC 7 — PIVOT / UNPIVOT

**Q23: Total salary per department as columns**
```sql
SELECT
    SUM(CASE WHEN dept_id = 'd01' THEN salary END) AS d01,
    SUM(CASE WHEN dept_id = 'd02' THEN salary END) AS d02,
    SUM(CASE WHEN dept_id = 'd03' THEN salary END) AS d03
FROM employees;
```

**Q24: Count employees per department as columns**
```sql
SELECT
    COUNT(CASE WHEN dept_id = 'd01' THEN 1 END) AS d01,
    COUNT(CASE WHEN dept_id = 'd02' THEN 1 END) AS d02,
    COUNT(CASE WHEN dept_id = 'd03' THEN 1 END) AS d03
FROM employees;
```

**Q25: Average salary per department as columns**
```sql
SELECT
    AVG(CASE WHEN dept_id = 'd01' THEN salary END) AS d01,
    AVG(CASE WHEN dept_id = 'd02' THEN salary END) AS d02,
    AVG(CASE WHEN dept_id = 'd03' THEN salary END) AS d03
FROM employees;
```

**Q26: Count of employees hired per year as columns**
```sql
SELECT
    COUNT(CASE WHEN hire_year = 2019 THEN 1 END) AS yr_2019,
    COUNT(CASE WHEN hire_year = 2020 THEN 1 END) AS yr_2020,
    COUNT(CASE WHEN hire_year = 2021 THEN 1 END) AS yr_2021
FROM employees;
```

**Q27: UNPIVOT — dept averages as rows**
```sql
WITH pivoted AS (
    SELECT
        AVG(CASE WHEN dept_id = 'd01' THEN salary END) AS d01,
        AVG(CASE WHEN dept_id = 'd02' THEN salary END) AS d02,
        AVG(CASE WHEN dept_id = 'd03' THEN salary END) AS d03
    FROM employees
)
SELECT 'd01' AS dept, d01 AS avg_salary FROM pivoted
UNION ALL
SELECT 'd02', d02 FROM pivoted
UNION ALL
SELECT 'd03', d03 FROM pivoted;
```

---

## TOPIC 8 — LATERAL JOIN

**Q28: Top 2 sales per employee**
```sql
SELECT
    e.name,
    top_sale.amount
FROM employees e
CROSS JOIN LATERAL (
    SELECT amount
    FROM sales s
    WHERE s.emp_id = e.emp_id
    ORDER BY amount DESC
    LIMIT 2
) top_sale;
```

**Q29: Most recent sale per employee**
```sql
SELECT
    e.name,
    top_sale.amount,
    top_sale.sale_date
FROM employees e
CROSS JOIN LATERAL (
    SELECT s.amount, s.sale_date
    FROM sales s
    WHERE s.emp_id = e.emp_id
    ORDER BY sale_date DESC
    LIMIT 1
) top_sale;
```

**Q30: Total, average, count of sales per employee**
```sql
SELECT
    e.name,
    sale_stats.total,
    sale_stats.avg_sale,
    sale_stats.sale_count
FROM employees e
CROSS JOIN LATERAL (
    SELECT
        SUM(amount)    AS total,
        AVG(amount)    AS avg_sale,
        COUNT(sale_id) AS sale_count
    FROM sales s
    WHERE s.emp_id = e.emp_id
) sale_stats;
```

**Q31: Sales above $1000 per employee**
```sql
SELECT
    e.name,
    high.high_sales,
    high.high_total
FROM employees e
CROSS JOIN LATERAL (
    SELECT
        COUNT(sale_id) AS high_sales,
        SUM(amount)    AS high_total
    FROM sales s
    WHERE s.emp_id = e.emp_id
    AND s.amount > 1000
) high;
```

**Q32: Employees whose total sales exceed company average**
```sql
WITH emp_totals AS (
    SELECT e.emp_id, e.name, tot.total_amount
    FROM employees e
    CROSS JOIN LATERAL (
        SELECT SUM(amount) AS total_amount
        FROM sales s
        WHERE s.emp_id = e.emp_id
    ) tot
),
company_avg AS (
    SELECT AVG(total_amount) AS avg_total
    FROM emp_totals
)
SELECT e.name, e.total_amount
FROM emp_totals e
CROSS JOIN company_avg c
WHERE e.total_amount > c.avg_total;
```

---

## TOPIC 9 — SUBQUERIES

**Q 33: Employees earning above average salary**
```sql
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

**Q 34: Departments with at least one employee earning > 100000**
```sql
SELECT DISTINCT dept_id
FROM employees
WHERE EXISTS (
    SELECT 1 FROM employees e2
    WHERE e2.dept_id = employees.dept_id
    AND e2.salary > 100000
);
```

---

## TOPIC 10 — MIXED HARD PROBLEMS

**Q35: Department salary distribution**
```sql
SELECT
    dept_id,
    MAX(salary)              AS max_salary,
    MIN(salary)              AS min_salary,
    ROUND(AVG(salary), 0)    AS avg_salary,
    MAX(salary) - MIN(salary) AS salary_range
FROM employees
GROUP BY dept_id
ORDER BY dept_id;
```

**Q 36: Employees above BOTH dept avg AND company avg**
```sql
WITH stats AS (
    SELECT
        name,
        salary,
        AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg,
        AVG(salary) OVER ()                     AS company_avg
    FROM employees
)
SELECT name, salary, dept_avg, company_avg
FROM stats
WHERE salary > dept_avg
AND salary > company_avg;
```

**Q 37: Each dept total, avg, highest paid, lowest paid**
```sql
WITH CTE AS (
    SELECT
        dept_id,
        SUM(salary) OVER (PARTITION BY dept_id) AS total_salary,
        AVG(salary) OVER (PARTITION BY dept_id) AS avg_salary,
        FIRST_VALUE(name) OVER (
            PARTITION BY dept_id ORDER BY salary DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS highest_paid,
        FIRST_VALUE(name) OVER (
            PARTITION BY dept_id ORDER BY salary ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS lowest_paid
    FROM employees
)
SELECT DISTINCT dept_id, total_salary, avg_salary,
       highest_paid, lowest_paid
FROM CTE
ORDER BY dept_id;
