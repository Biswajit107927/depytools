scores = [
    {"player": "p1", "points": 340},
    {"player": "p2", "points": None},
    {"player": "p3", "points": 520},
    {"player": "p4", "points": 180},
    {"player": "p5", "points": 520},
]

def top_players(scores, n):
    result= sorted (
        scores,
        key = lambda x:x.get("points") if x.get("points") is not None else 0,
        reverse=True
    )
    return result[0:n]

if __name__=="__main__":
    print(top_players(scores, 3))
    print(top_players(scores, 10))
