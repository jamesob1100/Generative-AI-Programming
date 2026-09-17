import os
import csv
import sys


def file_function(filename):
    """Handle an expenses CSV file: ensure header, optionally overwrite, and read data.

    Parameters:
      filename (str): The name of the file to read from or write to.

    Returns:
      list: A list of dictionaries with keys 'id','date','description','amount','category'.

    #Tests:
      - check that a new file is created and an empty list is returned
      - check that an existing file with correct header is read into a list of dicts
      - check that when header is incorrect the user can choose to overwrite
    """
    HEADER = ["id", "date", "description", "amount", "category"]
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(HEADER)
        return []

    # file exists - check header or emptiness
    with open(filename, "r", newline="") as fh:
        reader = csv.reader(fh)
        try:
            first = next(reader)
        except StopIteration:
            # empty file: write header and treat as new
            with open(filename, "w", newline="") as fw:
                csv.writer(fw).writerow(HEADER)
            return []

    if first != HEADER:
        answer = input(
            f"{filename} does not contain required header {','.join(HEADER)}. Overwrite file? (y/n): "
        ).strip().lower()
        if answer in ("y", "yes"):
            with open(filename, "w", newline="") as fw:
                csv.writer(fw).writerow(HEADER)
            return []
        else:
            print("Incompatible file header; exiting.")
            sys.exit(1)

    # header is present and correct: read data
    with open(filename, "r", newline="") as fh:
        dr = csv.DictReader(fh)
        return [row for row in dr]
