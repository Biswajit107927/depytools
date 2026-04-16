

items = [
    {"id": "a1", "name": "laptop",  "amount": 999},
    {"id": "a2", "name": "phone",   "amount": 599},
    {"id": "a1", "name": "laptop",  "amount": 999},  # duplicate
    {"id": None, "name": "tablet",  "amount": 399},  # None id
    {"id": "a3", "name": "mouse",   "amount": None},
]

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Q1
"""Given list of dicts with possible duplicate ids and None ids Return unique items — keep first occurrence, skip None ids"""
#Q2
"""Given same items list Return only items where amount > 500 Skip None amounts"""
#Q3
""" Given same items list  Add amount_gbp field = round(amount * 0.79, 2) Skip items where amount is None"""
#Q4
""" # Given same items list  Sort by amount descending Handle None amounts (treat as 0) Return top 2 items"""
#Q5
"""  Given same items list Skip items where id is None Skip items where amount is None Print valid items only"""



