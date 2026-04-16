"""
Pattern 23: Full OOP Pipeline Class
- __init__, run(), __str__, @property
"""

class Pipeline:

    def __init__(self, name, source, destination):
        self.name = name
        self.source = source
        self.destination = destination

    def run(self):
        print(f"Running {self.name}: {self.source} → {self.destination}")

    def __str__(self):
        return f"Pipeline({self.name})"

    @property
    def status(self):
        return "active" if self.name else "inactive"


if __name__ == "__main__":
    p = Pipeline("sales_etl", "S3", "Redshift")
    p.run()
    print(p)
    print(p.status)