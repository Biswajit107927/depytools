#P10 — Find Duplicates
#Task: flag_repeats(logins) — duplicate = same (ip, device) pair seen before. Return the list of attempt ids that repeat an earlier pair.

def flag_repeats(logins:list):
    result=[]
    seen = set()
    for login in logins:
        ip=login.get("ip")
        device=login.get("device")
        if ((ip,device) not in seen):
            seen.add((ip,device))
        else:
            result.append(login.get("attempt"))
    return result


if __name__=='__main__':
    logins = [
        {"attempt": "a1", "ip": "10.0.0.1", "device": "mobile"},
        {"attempt": "a2", "ip": "10.0.0.2", "device": "desktop"},
        {"attempt": "a3", "ip": "10.0.0.1", "device": "mobile"},
        {"attempt": "a4", "ip": "10.0.0.1", "device": "desktop"},
        {"attempt": "a5", "ip": "10.0.0.2", "device": "desktop"},
        {"attempt": "a6", "ip": "10.0.0.1", "device": "mobile"},
    ]
    print(flag_repeats(logins))










