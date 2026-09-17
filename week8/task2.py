import random
import datetime


class Column:
    def __init__(self, name, values=None):
        self.name = name
        self.values = values or []

    def generate(self, row_index):
        raise NotImplementedError("Subclasses must implement generate")


class CategoricalColumn(Column):
    def __init__(self, name, categories):
        super().__init__(name, categories)
        if not categories:
            raise ValueError("categories list cannot be empty")

    def generate(self, row_index):
        return random.choice(self.values)


class NormalColumn(Column):
    def __init__(self, name, mean=0.0, std=1.0):
        super().__init__(name)
        self.mean = mean
        self.std = std

    def generate(self, row_index):
        # Return integer values sampled from a normal distribution
        return int(round(random.gauss(self.mean, self.std)))


class UniformColumn(Column):
    def __init__(self, name, low=0.0, high=1.0):
        super().__init__(name)
        self.low = low
        self.high = high

    def generate(self, row_index):
        return random.uniform(self.low, self.high)


class NameColumn(Column):
    def __init__(self, name, first_names=None, surnames=None):
        super().__init__(name)
        self.first_names = first_names or [
            "Amina", "Bao", "Carlos", "Deepa", "Elena", "Farah", "Giovanni", "Hiro", "Ibrahim", "Jaya",
            "Keiko", "Liam", "Maya", "Nadia", "Omar", "Pia", "Qiang", "Ravi", "Sofia", "Tariq",
            "Usha", "Valentina", "Wang", "Ximena", "Yara", "Zain", "Aditya", "Bong", "Chi", "Devon",
            "Esi", "Fatima", "Gurpreet", "Hassan", "Iris", "Jin", "Kofi", "Lakshmi", "Mateo", "Naomi",
        ]
        self.surnames = surnames or [
            "Abebe", "Bae", "Chen", "Dalal", "Eze", "Fernandez", "Gonzalez", "Hussein", "Ivanov", "Jensen",
            "Khan", "Liu", "Mendoza", "Nguyen", "Osei", "Patel", "Qureshi", "Ramirez", "Santos", "Tan",
            "Uchida", "Vasquez", "Wang", "Xavier", "Yamamoto", "Zhang", "Andersson", "Bennett", "Cruz", "Dias",
            "Eriksson", "Fischer", "García", "Hernández", "Islam", "Jalili", "Khatri", "Leclerc", "Müller", "Novák",
            "O’Connor", "Papadopoulos", "Quispe", "Rossi", "Svensson", "Takahashi", "Uddin", "Vargas", "Wright", "Zubair",
        ]

    def generate(self, row_index):
        first = random.choice(self.first_names).title()
        last = random.choice(self.surnames).title()
        return f"{first} {last}"


class DateColumn(Column):
    def __init__(self, name, start, end):
        super().__init__(name)
        if isinstance(start, str):
            start = datetime.datetime.fromisoformat(start).date()
        if isinstance(end, str):
            end = datetime.datetime.fromisoformat(end).date()

        if not isinstance(start, datetime.date) or not isinstance(end, datetime.date):
            raise TypeError("start and end must be date or ISO date string")

        if start > end:
            raise ValueError("start date must be <= end date")

        self.start = start
        self.end = end

    def generate(self, row_index):
        days_range = (self.end - self.start).days
        random_days = random.randint(0, days_range)
        return (self.start + datetime.timedelta(days=random_days)).isoformat()


class IDColumn(Column):
    def __init__(self, name, start=0, step=1):
        super().__init__(name)
        self.start = start
        self.step = step

    def generate(self, row_index):
        return self.start + self.step * row_index


class DataGenerator:
    def __init__(self, columns):
        self.columns = columns
        self._data = []

    @classmethod
    def from_config(cls, config):
        columns = []
        for c in config:
            typ = c.get("type")
            name = c["name"]

            if typ == "categorical":
                columns.append(CategoricalColumn(name, c["values"]))
            elif typ == "normal":
                columns.append(NormalColumn(name, c.get("mean", 0), c.get("std", 1)))
            elif typ == "uniform":
                columns.append(UniformColumn(name, c.get("low", 0), c.get("high", 1)))
            elif typ == "name":
                columns.append(NameColumn(name, c.get("first_names"), c.get("surnames")))
            elif typ == "date":
                columns.append(DateColumn(name, c["start"], c["end"]))
            elif typ == "id":
                columns.append(IDColumn(name, c.get("start", 1), c.get("step", 1)))
            else:
                raise ValueError(f"Unknown column type: {typ}")

        return cls(columns)

    def generate(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a non-negative integer")

        self._data = []
        for i in range(n):
            row = {}
            for col in self.columns:
                row[col.name] = col.generate(i)
            self._data.append(row)

        return self._data

    def getData(self):
        return list(self._data)


if __name__ == "__main__":
    schema = [
        {"name": "id", "type": "id", "start": 1000, "step": 1},
        {"name": "name", "type": "name"},
        {"name": "normal", "type": "normal", "mean": 35, "std": 10},
        {"name": "uniform", "type": "uniform", "low": 0, "high": 100},
        {"name": "categorical", "type": "categorical", "values": [
            "Brazil", "India", "USA", "Kenya", "Japan", "China", "Germany", "France", "Italy", "Spain",
            "Canada", "Mexico", "Australia", "South Africa", "Egypt", "Russia", "Turkey", "Argentina", "Nigeria", "South Korea",
            "Indonesia", "Pakistan", "Bangladesh", "Poland", "Sweden", "Norway", "Denmark", "Finland", "Greece", "Netherlands",
            "Switzerland", "Belgium", "Austria", "Ireland", "Portugal", "New Zealand", "Chile", "Colombia", "Peru", "Morocco",
            "Thailand", "Vietnam", "Philippines", "Malaysia", "Singapore", "Saudi Arabia", "Ireland", "Ukraine", "Czech Republic", "Hungary"
        ]},
        {"name": "date", "type": "date", "start": "2020-01-01", "end": "2025-12-31"},
    ]

    gen = DataGenerator.from_config(schema)

    # Normal operation test (no error path) with one of every supported column type
    n = 10
    print(f"Generating {n} rows of data using all column types...")
    gen.generate(n)

    data = gen.getData()
    print(f"Generated {len(data)} rows")
    for row in data:
        print(row)
