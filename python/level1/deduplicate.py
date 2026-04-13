"""
Pattern 1: Deduplicate list of dicts by key
- Skip None keys
- Keep first occurrence
"""

def deduplicate(items, key="id"):
    seen = {}
    for item in items:
        k = item.get(key)
        if k and k not in seen:
            seen[k] = item
    return list(seen.values())


if __name__ == "__main__":
    items = [
        {"id": "a1", "name": "laptop",  "amount": 999},
        {"id": "a2", "name": "phone",   "amount": 599},
        {"id": "a1", "name": "laptop",  "amount": 999},
        {"id": None, "name": "tablet",  "amount": 399},
        {"id": "a3", "name": "mouse",   "amount": None},
    ]
    print(deduplicate(items))