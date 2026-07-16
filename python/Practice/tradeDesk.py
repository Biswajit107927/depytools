from collections import Counter

class EventTracker():
    def __init__(self):
         self.records=[]
    def record(self,user:str,event:str):
        self.records.append({user:event})
        return True
    def show_records(self):
        print(self.records)
    def count_events(self,user:str):
        counter=0
        for i in self.records:
            if user in i:
                counter+=1
        return counter
    def count_by_type(self, type: str):
        counter = 0
        for i in self.records:
            if type in i.values():
                counter += 1
        return counter

    def top_user(self) -> str:
        if not self.records:
            return ""  # or None — check what the problem specifies
        c = Counter(next(iter(d)) for d in self.records)
        return c.most_common(1)[0][0]




if __name__=="__main__":
    et=EventTracker()
    et.record("user1", "click")
    et.record("user1", a"view")
    et.record("user2", "click")
    et.record("user1", "click")
    et.show_records()
    print(et.count_events("user1"))
    print(et.count_events("user3"))
    print(et.count_by_type("click"))
    print(et.count_by_type("view"))
    print(et.top_user())




