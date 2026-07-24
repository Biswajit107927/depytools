#Task: with_balance(deposits) — new list (no mutation — spread pattern), each record gains balance = running total, None counts as 0 but the record stays in the output.

def with_balance(deposits:list):
    running_total=0
    result=[]
    for deposit in deposits:
        amount=deposit.get("amount")
        if amount is not None:
            running_total=running_total+amount
        result.append({**deposit,"balance":running_total})
    return result


if __name__=='__main__':
    deposits = [
        {"txn": "d1", "amount": 500},
        {"txn": "d2", "amount": None},
        {"txn": "d3", "amount": 250},
        {"txn": "d4", "amount": 1000},
    ]
    print(with_balance(deposits))

