
#Task: dedupe(events) — unique by event_id, keep first occurrence, skip None ids. Return a list.
#by_user(events, user)

events = [
    {"event_id": "e1", "user": "u1", "action": "login"},
    {"event_id": "e2", "user": "u2", "action": "click"},
    {"event_id": "e1", "user": "u1", "action": "login"},   # dup
    {"event_id": None, "user": "u3", "action": "view"},    # None id
    {"event_id": "e3", "user": "u1", "action": "logout"},
    {"event_id": "e2", "user": "u2", "action": "click"},   # dup
]


def dedupe(events):
    result = {}
    for event in events:
        event_id=event.get("event_id")
        if event_id is not None and event_id not in result :
            result[event_id]=event
    return (list(result.values()))

def by_user(events, user):
    result=[]
    for event in events:
        d_user = event.get("user")
        if d_user==user:
            result.append(event)
    return result




if __name__=="__main__":
    print(dedupe(events))
    print(by_user(events, "u1"))
    print(by_user(events, "u9"))
