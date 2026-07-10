#Task: moving_sum(data, k) — sum of every window of size k.
daily_sales = [120, 340, 210, 500, 180, 420, 310]
def moving_sum(daily_sales,k):
    moving_sum=[]
    if k <= 0 or k > len(daily_sales):
        return (moving_sum)
    for i in range(0,len(daily_sales)-k+1):
        total=sum(daily_sales[i:i+k])
        moving_sum.append(total)
    return (moving_sum)

print(moving_sum(daily_sales,0))
print(moving_sum(daily_sales,10))
print(moving_sum(daily_sales, 3))