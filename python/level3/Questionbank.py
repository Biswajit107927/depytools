""""P16 → Basic class + __init__
P17 → Methods + return
P18 → List attributes
P19 → Inheritance + super()
P20 → @property
P21 → @classmethod
P22 → __str__
P23 → Full Pipeline class
P24 → Encapsulation
P25 → @staticmethod
P26 → Dataclass"""


#Q16  Basic Class
"""
Create DataEngineer class with:
 → name, years attributes  → introduce() method prints: "Hi I'm {name} with {years} years experience """

#Q17  Instance Method + Return
"""Add to DataEngineer:  → is_senior() method returns True if years >= 10 returns False otherwise """

#Q18 Class With List Attribute
"""  Add to DataEngineer: → skills = [] attribute → add_skills(skill) → appends to list → show_skills() → 
prints:   "{name}'s skills: Python, SQL, Spark" """

#Q19 Inheritance + super()
"""
Create SeniorDataEngineer(DataEngineer):
→ adds team_size attribute
 → overrides introduce():
#  "Hi I'm {name}, Senior DE leading {team_size} engineers"

sde = SeniorDataEngineer("Biswajit", 14, 8)
sde.introduce() """

#Q20 @property Decorator
"""
Add to DataEngineer:
 → @property level →
   "Senior" if years >= 10
   "Mid"    if years >= 5
   "Junior" if years < 5

print(engineer.level)  # no brackets!

"""

#Q21   Full Pipeline Class
"""
Add to DataEngineer: 
→ class variable total_engineers = 0
 → increment in __init__
 → @classmethod get_total(cls) → returns total
print(DataEngineer.get_total())  # → 3
"""

#Q22  str Method
""""
# Add to DataEngineer:
# → __str__ returns:
#   "DataEngineer(Biswajit, 14 years)"

engineer = DataEngineer("Biswajit", 14)
print(engineer)  # → DataEngineer(Biswajit, 14 years)
"""

#Q23 Full Pipeline Class
"""
# Create Pipeline class with:
# → name, source, destination attributes
# → run() → "Running {name}: {source} → {destination}"
# → __str__ → "Pipeline({name})"
# → @property status → "active" if name else "inactive"

p = Pipeline("sales_etl", "S3", "Redshift")
p.run()
print(p)
print(p.status)
"""

#Q24 — Encapsulation
"""
# Create DataEngineer with:
# → __salary → private attribute
# → get_salary() → returns salary
# → set_salary(new_salary):
#   updates if > 0
#   else prints "Invalid salary!"

engineer = DataEngineer("Biswajit", 150000)
print(engineer.get_salary())  # → 150000
engineer.set_salary(180000)
engineer.set_salary(-5000)    # → Invalid salary!

"""

#P25 — @staticmethod
"""
# Add to DataEngineer:
# → @staticmethod validate_salary(salary)
#   returns True if 50000 <= salary <= 500000
#   returns False otherwise

print(DataEngineer.validate_salary(150000))  # → True
print(DataEngineer.validate_salary(-5000))   # → False
print(DataEngineer.validate_salary(999999))  # → False

"""

# P26 — Dataclass
"""
from dataclasses import dataclass

# Create DataEngineer dataclass with:
# → name: str
# → years: int
# → salary: float
# → @property level →
#   "Senior/Mid/Junior"

e = DataEngineer("Biswajit", 14, 150000)
print(e)        # → DataEngineer(name='Biswajit', years=14, salary=150000)
print(e.level)  # → Senior

"""







