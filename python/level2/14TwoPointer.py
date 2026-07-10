#find_pair(prices, target) — return the indices [i, j] of the two numbers that sum to exactly target. Exactly one solution exists. If none, return [

prices = [10, 25, 40, 55, 70, 85, 110]   # sorted ascending

def find_pair(prices,target):
    left=0
    right=len(prices)-1
    while( left < right ):
        if prices[left]+ prices[right] ==target:
            return [left,right]
        if prices[left]+prices[right] < target:
            left+=1
        else: right-=1
    return []

print(find_pair(prices,125))
print(find_pair(prices,300))


