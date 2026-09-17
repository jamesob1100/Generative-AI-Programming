"""
 👩‍🏫 Teacher Persona: Python Name Generator for Beginners

Fantastic news: this is exactly the kind of small project that helps learners build confidence fast.  
I’ve already implemented the function in detailed.py with clear behavior, and now I’ll explain it in a beginner-friendly teaching tone.

---

📌 Function: `generate_person_names(count)`

- Input: `count` (number of names to generate)
- Output: list of tuples like `[("Maya", "Patel"), ("Hiro", "Chen"), ...]`
- Validation:
  - `TypeError` if `count` is not an `int`
  - `ValueError` if `count < 0`
  - `ValueError` if `count` > 2000 (because we generate from 40×50 unique name pool)
- Names are capitalized (`.title()`)

---
"""
## 🧩 Code (from detailed.py)

import random

def generate_person_names(count):
    if not isinstance(count, int):
        raise TypeError("count must be an integer")

    if count < 0:
        raise ValueError("count must be a non-negative integer")

    first_names = [
        "Amina", "Bao", "Carlos", "Deepa", "Elena", "Farah", "Giovanni", "Hiro", "Ibrahim", "Jaya",
        "Keiko", "Liam", "Maya", "Nadia", "Omar", "Pia", "Qiang", "Ravi", "Sofia", "Tariq",
        "Usha", "Valentina", "Wang", "Ximena", "Yara", "Zain", "Aditya", "Bong", "Chi", "Devon",
        "Esi", "Fatima", "Gurpreet", "Hassan", "Iris", "Jin", "Kofi", "Lakshmi", "Mateo", "Naomi",
    ]

    surnames = [
        "Abebe", "Bae", "Chen", "Dalal", "Eze", "Fernandez", "Gonzalez", "Hussein", "Ivanov", "Jensen",
        "Khan", "Liu", "Mendoza", "Nguyen", "Osei", "Patel", "Qureshi", "Ramirez", "Santos", "Tan",
        "Uchida", "Vasquez", "Wang", "Xavier", "Yamamoto", "Zhang", "Andersson", "Bennett", "Cruz", "Dias",
        "Eriksson", "Fischer", "García", "Hernández", "Islam", "Jalili", "Khatri", "Leclerc", "Müller", "Novák",
        "O’Connor", "Papadopoulos", "Quispe", "Rossi", "Svensson", "Takahashi", "Uddin", "Vargas", "Wright", "Zubair",
    ]

    max_pool = len(first_names) * len(surnames)
    if count > max_pool:
        raise ValueError(f"count must be at most {max_pool}, got {count}")

    all_pairs = [(fn.title(), sn.title()) for fn in first_names for sn in surnames]
    chosen = random.sample(all_pairs, count)

    return chosen

if __name__ == "__main__":
    print(generate_person_names(5))

"""

🎯 Teaching notes

1. **Start with simple validation**: `if not isinstance(count, int)` and `if count < 0`.
2. **Show list structure**: first names and surnames are separate sources.
3. **Explain combinations**: 40 × 50 = 2000 unique tuples.
4. **Use `random.sample`** for unique output.
5. **Encourage experimentation**: add own culturally diverse names, 1000+ combos.

---

## ✅ Try it in class

- `generate_person_names(0)` → `[]`
- `generate_person_names(3)` → 3 unique pairs
- `generate_person_names(2001)` → raises `ValueError` (nice classroom test)

"""