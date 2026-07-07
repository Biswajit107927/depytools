#a duplicate = same (user, amount) pair.
#Return the list of txn_ids that are duplicates of an earlier transaction (first occurrence is NOT a duplicate).



transactions = [
    {"txn_id": "t1", "user": "u1", "amount": 100},
    {"txn_id": "t2", "user": "u2", "amount": 250},
    {"txn_id": "t3", "user": "u1", "amount": 100},
    {"txn_id": "t4", "user": "u3", "amount": 300},
    {"txn_id": "t5", "user": "u1", "amount": 100},
    {"txn_id": "t6", "user": "u2", "amount": 250},
]

seen=set()
duplicate=[]

for transaction in transactions:
    txn_id=transaction.get("txn_id")
    user= transaction.get("user")
    amount=transaction.get("amount")
    if ((user,amount) not in seen):
        seen.add((user,amount))
    else:
        duplicate.append(txn_id)

print(seen)
print(duplicate)