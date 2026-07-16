scores = [
    {"player": "p1", "points": 340},
    {"player": None,  "points": 200},
    {"player": "p3", "points": None},
    {"player": "p4", "points": 0},      # ← zero is VALID, not None
]

def clean(scores):
    result=[]
    for score in scores:
        if score.get("player") is not None  and score.get("points") is not None:
            result.append(score)
    return result

if __name__=='__main__':
    print(clean(scores))