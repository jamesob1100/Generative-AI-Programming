"""
#filter function
#function header
    Filter and display data matching the criteria given by the user

    Parameters:
        option1 (non-negative int): selecting favourite dinner course/setting
        option2 (non-negative int): selecting which dinner course/setting to filter by

    Returns:
        list: A list of filtered data based on the selection criteria.

#doctests
    test valid arguments
    >>> filter_data(0, 0)
    [{'course': 'appetizer', 'setting': 'formal'}]
    
    >>> filter_data(1, 1)
    [{'course': 'main', 'setting': 'casual'}]

    >>> filter_data(2, 0)
    [{'course': 'dessert', 'setting': 'formal'}]

    >>> filter_data(0, 1)
    [{'course': 'appetizer', 'setting': 'casual'}]

    >>> filter_data(0, 0)
    [{'course': 'appetizer', 'setting': 'formal'}]

    test valid arguments with no matching data
    >>> filter_data(2, 1)
    []

    test invalid arguments
    >>> filter_data(3, 0)
    Traceback (most recent call last):
     ...
    ValueError: Invalid options. Please select valid course and setting.

    >>> filter_data(-1, 0)
    Traceback (most recent call last):
     ...
    ValueError: Invalid options. Please select valid course and setting.

    >>> filter_data(0, 2)
    Traceback (most recent call last):
     ...
    ValueError: Invalid options. Please select valid course and setting.

    >>> filter_data(0, -1)
    Traceback (most recent call last):
     ...
    ValueError: Invalid options. Please select valid course and setting.

    >>> filter_data(5, 10)
    Traceback (most recent call last):
     ...
    ValueError: Invalid options. Please select valid course and setting.

#file reader function
#function header
    The File Reader Function reads in a CSV file and stores its contents in a list which the 
    Filter Data Function can access and search through.

    Parameters:
    filename (str): The name of the CSV file to read.

    Returns:
    list: A list of dictionaries representing the rows of the CSV file, 
    where each dictionary's keys are the column headers and values are the corresponding cell values.
#doctests  
    (check individual lines)
    >>> read_dining_csv("dining.csv")[0]
    ['Jemima', 'Lockley', 'dessert', 'home']
    >>> read_dining_csv("dining.csv")[1]
    ['Pip', 'Robelow', 'main', 'restaurant']
    >>> read_dining_csv("dining.csv")[2]
    ['Crista', 'Enderson', 'dessert', 'home']
    >>> read_dining_csv("dining.csv")[3]
    ['Manya', 'Sarchwell', 'main', 'home']
    
    edge case: file not found
    >>> read_dining_csv("nonexistent.csv")
    []

    error case: invalid filename type
    >>> read_dining_csv(123)
    Traceback (most recent call last):
     ...
    TypeError: join() argument must be str, bytes, or os.PathLike object, not 'int'

#main function
#function header
    The user:
    1.	Prompted with searching either ‘favourite course’ or ‘favourite setting’
    2.	Chooses ‘favourite course’ and is prompted with ‘starter’, ‘main’, or ‘dessert’
    3.	Selects one and is presented all data with the selected course
    Alternative a:
    1a.  Enters an invalid search request
    2a.  Repeats 1
    Alternative b:
    2b. Chooses ‘favourite setting’ and is prompted with ‘restaurant’, ‘home’, ‘picnic’, or ‘takeaway’
    3b.  Selects one and is presented all data with matching selection
    Alternative c:
    2c.  Enters invalid search request
    3c.  Repeats 2
#doctests for entire program 
    test 1: valid filter returns matching entries
    >>> filter_data(0, 0)
    [{'course': 'appetizer', 'setting': 'formal'}]

    test 2: invalid filter raises ValueError
    >>> filter_data(3, 0)
    Traceback (most recent call last):
     ...
    ValueError: Invalid options. Please select valid course and setting.

    test 3: CSV reader returns list of lists with actual data
    >>> len(read_dining_csv("dining.csv")) > 0
    True

    test 4: CSV reader handles missing file gracefully
    >>> read_dining_csv("missing.csv")
    []

    test 5: integration - filter with valid settings finds data
    >>> result = filter_data(1, 1); len(result) > 0 and result[0]['course'] == 'main'
    True
"""



def filter_data(option1, option2):
    # Sample data representing dinner courses/settings
    data = [
        {"course": "appetizer", "setting": "formal"},
        {"course": "main", "setting": "casual"},
        {"course": "dessert", "setting": "formal"},
        {"course": "appetizer", "setting": "casual"},
        {"course": "main", "setting": "formal"},
    ]

    # Define the mapping of options to actual values
    course_options = {0: "appetizer", 1: "main", 2: "dessert"}
    setting_options = {0: "formal", 1: "casual"}

    # Validate the input options
    if option1 not in course_options or option2 not in setting_options:
        raise ValueError("Invalid options. Please select valid course and setting.")

    selected_course = course_options[option1]
    selected_setting = setting_options[option2]

    # Filter the data based on the selected course and setting
    filtered_data = [entry for entry in data if entry["course"] == selected_course and entry["setting"] == selected_setting]

    return filtered_data


def read_dining_csv(filename="dining.csv"):
    import csv
    import os

    base_dir = os.path.dirname(__file__)
    filepath = os.path.join(base_dir, filename)

    rows = []
    try:
        with open(filepath, newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            for row in reader:
                rows.append([cell.strip() for cell in row])
    except FileNotFoundError:
        rows = []

    return rows


def main():

    course_options = {0: "appetizer", 1: "main", 2: "dessert"}
    setting_options = {0: "formal", 1: "casual"}

    print("Select course:")
    for k, v in course_options.items():
        print(f"  {k}: {v}")

    try:
        c = int(input("Enter course number: ").strip())
    except Exception:
        print("Invalid input for course; please enter a number.")
        return

    print("Select setting:")
    for k, v in setting_options.items():
        print(f"  {k}: {v}")

    try:
        s = int(input("Enter setting number: ").strip())
    except Exception:
        print("Invalid input for setting; please enter a number.")
        return

    try:
        results = filter_data(c, s)
    except ValueError as exc:
        print(exc)
        return

    if not results:
        print("No matching entries found.")
        return

    print("Matches:")
    for entry in results:
        print(entry)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)