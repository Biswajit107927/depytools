


def add_flag(events):
    result = []
    for event in events:
        if event.get("event_id") is not None:
            flag = event.get("action") == "login"
            result.append({**event, "suspicious": flag})
    return result



if __name__ == "__main__":
    events = [
        {"event_id": "e1", "user": "u1", "action": "login"},
        {"event_id": "e2", "user": "u2", "action": "click"},
        {"event_id": "e1", "user": "u1", "action": "login"},
        {"event_id": None, "user": "u3", "action": "view"},  # ← the row that tests clause 3
        {"event_id": "e3", "user": "u1", "action": "logout"},
        {"event_id": "e2", "user": "u2", "action": "click"},
    ]
    print(add_flag(events))


