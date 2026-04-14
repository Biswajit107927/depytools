"""
Pattern 2: Filter list of dicts by field threshold
- Skip None values
- Return items above threshold
- Configurable key and threshold
"""

def filter_items(items, key="amount", threshold=500):
    return [
        item for item in items
        if item.get(key) is not None
        and item.get(key) > threshold
    ]


if __name__ == "__main__":
    items = [
        {"id": "a1", "name": "laptop",  "amount": 999},
        {"id": "a2", "name": "phone",   "amount": 599},
        {"id": "a1", "name": "laptop",  "amount": 999},
        {"id": None, "name": "tablet",  "amount": 399},
        {"id": "a3", "name": "mouse",   "amount": None},
    ]

    result = filter_items(items, threshold=500)
    print(result)
    # Returns laptop and phone only