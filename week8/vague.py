import random


def generate_name(prefixes=None, stems=None, suffixes=None, count=1):
    """Generate `count` random names from the given parts.

    If no part lists are provided, a default set of fantasy-style name fragments
    is used.

    Args:
        prefixes (list[str] | None): Leading syllables.
        stems (list[str] | None): Middle syllables.
        suffixes (list[str] | None): Final syllables.
        count (int): How many names to generate (must be >=1).

    Returns:
        list[str]: Generated names.
    """

    if count < 1:
        raise ValueError("count must be at least 1")

    default_prefixes = ["Ari", "Bel", "Cor", "Dra", "Ela", "Fen", "Gal", "Haz", "Ith", "Jor"]
    default_stems = ["na", "ri", "sel", "van", "lor", "wyn", "mos", "thar", "kel", "mir"]
    default_suffixes = ["a", "en", "in", "or", "us", "ia", "ir", "on", "ys", "el"]

    prefixes = prefixes or default_prefixes
    stems = stems or default_stems
    suffixes = suffixes or default_suffixes

    names = []
    for _ in range(count):
        prefix = random.choice(prefixes)
        stem = random.choice(stems)
        suffix = random.choice(suffixes)
        name = prefix + stem + suffix

        # Capitalize only first character for readability
        names.append(name.capitalize())

    return names


if __name__ == "__main__":
    print("Example name generation:", generate_name(count=5))
