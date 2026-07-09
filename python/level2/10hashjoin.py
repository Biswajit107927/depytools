# Inner join

employees = [
    {"emp_id": "e1", "name": "Ravi",   "dept_id": "d1"},
    {"emp_id": "e2", "name": "Sneha",  "dept_id": "d2"},
    {"emp_id": "e3", "name": "Arjun",  "dept_id": "d1"},
    {"emp_id": "e4", "name": "Priya",  "dept_id": "d9"},   # no matching dept
]
departments = [
    {"dept_id": "d1", "dept_name": "Finance"},
    {"dept_id": "d2", "dept_name": "Engineering"},
    {"dept_id": "d3", "dept_name": "HR"},
]

result=[]

department_lookup={department["dept_id"]:department for department in departments }

for employee in employees:
    e_dept_id =employee.get("dept_id")
    if e_dept_id in department_lookup:
        result.append({**employee,**department_lookup[e_dept_id]})

print(result)