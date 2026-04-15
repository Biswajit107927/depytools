"""
Pattern 16-18: OOP Basics
- DataEngineer class
- __init__, methods, list attributes
"""

class DataEngineer:

    def __init__(self, name, years):
        self.name = name
        self.years = years
        self.skills = []

    def introduce(self):
        print(f"Hi I'm {self.name} with {self.years} years experience")

    def is_senior(self):
        return self.years >= 10

    def add_skills(self, skill):
        self.skills.append(skill)

    def show_skills(self):
        print(f"{self.name}'s skills: {', '.join(self.skills)}")


if __name__ == "__main__":
    engineer = DataEngineer("Biswajit", 14)
    engineer.introduce()
    print(engineer.is_senior())
    engineer.add_skills("Python")
    engineer.add_skills("SQL")
    engineer.add_skills("Spark")
    engineer.show_skills()