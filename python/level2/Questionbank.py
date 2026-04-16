items = [
    {"id": "a1", "category": "electronics", "amount": 999},
    {"id": "a2", "category": "electronics", "amount": 599},
    {"id": "a3", "category": "clothing",    "amount": 49},
    {"id": "a4", "category": "electronics", "amount": 79},
    {"id": "a5", "category": "clothing",    "amount": 89},
    {"id": "a6", "category": "electronics", "amount": None},
]
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Q6 Group by category + sum
""" Group by category Sum amounts per category Skip None amounts"""

#Q7  Flatten nested tags

nested = [
    {"id": "a1", "tags": ["python", "sql", "aws"]},
    {"id": "a2", "tags": ["python", "spark"]},
    {"id": "a3", "tags": ["aws", "redshift"]},
    {"id": "a4", "tags": []},
    {"id": "a5", "tags": None},
]

""" Flatten all tags into one unique list Skip None and empty tags"""

#Q8  Merge two lists by key

orders = [
    {"id": "o1", "amount": 100},
    {"id": "o2", "amount": 200},
    {"id": "o3", "amount": 300},
]
customers = [
    {"id": "o1", "name": "Alice"},
    {"id": "o2", "name": "Bob"},
    {"id": "o4", "name": "Charlie"},
]
""" Merge orders and customers by id  Only include matched records """

#Q9  Running total

items = [
    {"id": "t1", "amount": 100},
    {"id": "t2", "amount": 250},
    {"id": "t3", "amount": 75},
    {"id": "t4", "amount": 300},
    {"id": "t5", "amount": 150},
]
""" Add running_total field to each item  Handle None amounts (treat as 0) """

#Q10 Find duplicates

items = [
    {"id": "t1", "amount": 100},
    {"id": "t2", "amount": 250},
    {"id": "t3", "amount": 75},
    {"id": "t4", "amount": 300},
    {"id": "t5", "amount": 150},
]
""" Add running_total field to each item Handle None amounts (treat as 0)"""

#Q11  Pivot data

records = [
    {"name": "Alice", "subject": "math",    "score": 95},
    {"name": "Alice", "subject": "science", "score": 88},
    {"name": "Bob",   "subject": "math",    "score": 76},
    {"name": "Bob",   "subject": "science", "score": 82},
]
""" Pivot so each name is a row Subjects become columns 
Output: [{"name": "Alice", "math": 95, "science": 88}, ...] """

#Q12  Transpose
data = {
    "name":   ["Alice", "Bob", "Charlie"],
    "age":    [25, 30, 35],
    "salary": [90000, 85000, 120000],
}
""" Convert column dict to list of row dicts
 Output: [{"name": "Alice", "age": 25, "salary": 90000}, ...] """

#Q13  Sliding window average

numbers = [100, 200, 150, 300, 250, 400, 350]
window_size = 3
""" Calculate average for each window of 3
 Output: [150.0, 216.67, 233.33, 316.67, 333.33] """

#Q14 Two pointer

numbers = [1, 3, 5, 7, 9, 11, 13]
target = 14
""" Find all pairs that sum to target No duplicate pairs
 Output: [(1, 13), (3, 11), (5, 9)] """

# Q15  Batch processing

items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
batch_size = 3
"""Split into batches of 3
 Output: [[1,2,3], [4,5,6], [7,8,9], [10]] """

