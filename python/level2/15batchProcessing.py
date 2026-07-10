record_ids = ["r1","r2","r3","r4","r5","r6","r7","r8","r9","r10"]
def make_batches(record_ids,batch_size):
    if batch_size <= 0:
        return []
    else:
        result = []
        for i in range(0,len(record_ids),batch_size):
            result.append(record_ids[i:i+batch_size])
    return result

print(make_batches(record_ids,3))
print(make_batches(record_ids,5))
print(make_batches(record_ids,0))
