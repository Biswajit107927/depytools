#Task: revenue_by_region(orders) — sum revenue per region, skip None revenues. Note: south must still appear (it has one valid order).


def revenue_by_region(orders:list):
    result={}
    for order in orders:
        if order.get("revenue") is not None:
            region=order.get("region")
            if region not in result:
                result[region]=order.get("revenue")
            else:
                result[region]+=order.get("revenue")
    return result

if __name__=='__main__':
    orders = [
        {"order_id": "o1", "region": "west", "revenue": 1200},
        {"order_id": "o2", "region": "east", "revenue": 800},
        {"order_id": "o3", "region": "west", "revenue": 450},
        {"order_id": "o4", "region": "south", "revenue": None},
        {"order_id": "o5", "region": "east", "revenue": 300},
        {"order_id": "o6", "region": "south", "revenue": 950},
    ]

    print(revenue_by_region(orders))



