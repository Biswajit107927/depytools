items = [
    {"id": "a1", "category": "electronics", "amount": 999},
    {"id": "a2", "category": "electronics", "amount": 599},
    {"id": "a3", "category": "clothing",    "amount": 49},
    {"id": "a4", "category": "electronics", "amount": 79},
    {"id": "a5", "category": "clothing",    "amount": 89},
    {"id": "a6", "category": "electronics", "amount": None},
]

result = {}
for item in items:
    category = item.get("category")
    amount = item.get("amount") or 0
    if category not in result:          # new category
        result[category] = amount
    elif category in result:            # existing category
        result[category] = amount + result.get(category)

print(result)