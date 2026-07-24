#Task: all_members(teams) — one flat list of unique members, first-seen order, handle None and empty safely.

def all_members(teams:list):
    result=[]
    seen=set()
    for team in teams:
        members=team.get("members") or []
        for member in members:
            if member not in seen:
                seen.add(member)
                result.append(member)
    return result


if __name__=='__main__':
    teams = [
        {"team": "alpha", "members": ["ravi", "sneha", "arjun"]},
        {"team": "beta",  "members": ["priya", "ravi"]},
        {"team": "gamma", "members": []},
        {"team": "delta", "members": None},
        {"team": "epsilon", "members": ["sneha", "kiran"]},
    ]
    print(all_members(teams))
