import random


def generate_person_names(count):
    """Generate a list of culturally-diverse (first_name, surname) tuples.

    The name pool is effectively 2000 unique pairs from:
      - 40 culturally diverse first names
      - 50 culturally diverse surnames

    Args:
        count (int): number of names to generate (>= 0 and <= 2000).

    Returns:
        list[tuple[str, str]]: list of (first_name, surname) tuples.

    Raises:
        TypeError: if count is not an int.
        ValueError: if count is negative or exceeds available unique pairs.
    """

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

    # Index that maps to exactly one pair in the 2000-pair space
    all_pairs = [(fn.title(), sn.title()) for fn in first_names for sn in surnames]

    # Get unique names; sampling without replacement
    chosen = random.sample(all_pairs, count)

    return chosen


if __name__ == "__main__":
    print(generate_person_names(5))
