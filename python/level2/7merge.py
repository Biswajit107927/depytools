#Task: join_shipments(shipments, warehouses) — inner join on warehouse, hash-join style (lookup dict + one pass — nested loops score 5 max). s4 drops out.


def join_shipments(shipments:list,warehouses:list):
    result=[]
    warehouse_lookup={}
    for warehouse in warehouses:
        w_warehouse=warehouse.get("warehouse")
        warehouse_lookup[w_warehouse]=warehouse

    for shipment in shipments:
        s_warehouse=shipment.get("warehouse")
        if s_warehouse in warehouse_lookup:
            result.append(
                { **warehouse_lookup.get(s_warehouse),
                  **shipment
                  }
            )
    return result

if __name__=='__main__':

    shipments = [
        {"ship_id": "s1", "warehouse": "w1", "weight": 120},
        {"ship_id": "s2", "warehouse": "w2", "weight": 340},
        {"ship_id": "s3", "warehouse": "w1", "weight": 95},
        {"ship_id": "s4", "warehouse": "w9", "weight": 210},   # no matching warehouse
    ]
    warehouses = [
        {"warehouse": "w1", "city": "Seattle"},
        {"warehouse": "w2", "city": "Portland"},
        {"warehouse": "w3", "city": "Boise"},
    ]
    print(join_shipments(shipments,warehouses))