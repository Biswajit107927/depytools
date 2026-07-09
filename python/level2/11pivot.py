#Task: pivot long → wide. One dict per person, subjects become keys.
records = [
    {"name": "Alice", "subject": "math",    "score": 95},
    {"name": "Alice", "subject": "science", "score": 88},
    {"name": "Bob",   "subject": "math",    "score": 76},
    {"name": "Bob",   "subject": "science", "score": 82},
]

result={}

for record in records:
    name=record.get("name")
    subject=record.get("subject")
    score=record.get("score")
    if name not in result:
        result[name]={subject:score}
    else:
        result[name]={**result[name],subject:score}
print(result)