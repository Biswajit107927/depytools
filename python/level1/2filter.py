#by_user(events, user)

events = [
    {"event_id": "e1", "user": "u1", "action": "login"},
    {"event_id": "e2", "user": "u2", "action": "click"},
    {"event_id": "e1", "user": "u1", "action": "login"},   # dup
    {"event_id": None, "user": "u3", "action": "view"},    # None id
    {"event_id": "e3", "user": "u1", "action": "logout"},
    {"event_id": "e2", "user": "u2", "action": "click"},   # dup
]

def by_user(events, user):
    result=[]
    for event in events:
        d_user = event.get("user")
        event_id=event.get("event_id")
        if d_user==user and event_id is not None:
            result.append(event)
    return result




if __name__=="__main__":
    print(by_user(events, "u1"))
    print(by_user(events, "u9"))
