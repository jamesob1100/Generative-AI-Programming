"""expenses - expense tracking with CSV file storage

File handling and menu-driven expense tracker per design specification.
"""

import os
import csv
import sys
from collections import defaultdict

PROMPTS = {
    'menu': '\n1. Display expenses\n2. Group by date/category\n3. Add expense\n4. Save\n5. Exit\nChoice: ',
    'date': 'Date (YYYY-MM-DD): ',
    'description': 'Description: ',
    'amount': 'Amount: ',
    'category': 'Category: ',
    'group_key': 'Group by (date/category): ',
    'invalid_choice': 'Invalid choice. Please enter 1-5.',
    'invalid_amount': 'Amount must be numeric.',
    'invalid_date': 'Date must be YYYY-MM-DD format.',
    'cancel_prompt': 'Cancel entry? (y/n): ',
    'entry_error': 'Entry format incorrect. Re-enter or cancel.',
}


def file_function(filename):
    """Ensure expenses CSV has header and read rows.

    Parameters:
      filename (str): CSV file path

    Returns:
      list: list of dicts with keys id,date,description,amount,category

    Tests:
      - new file created returns []
      - existing file with correct header read as dicts
      - incorrect header prompts overwrite
    """
    HEADER = ["id", "date", "description", "amount", "category"]
    created_or_reset = False
    # The context manager closes this handle automatically, even on early exits.
    with open(filename, 'a+', newline='') as fh:
        fh.seek(0)
        first_line = fh.readline().strip().split(',')
        if first_line == [''] or not first_line:
            fh.seek(0)
            fh.write(','.join(HEADER) + "\n")
            created_or_reset = True
        elif first_line != HEADER:
            ans = input(f"{filename} does not contain required header. Overwrite? (y/n): ").strip().lower()
            if ans in ('y', 'yes'):
                with open(filename, 'w', newline='') as fw:
                    csv.writer(fw, lineterminator='\n').writerow(HEADER)
                created_or_reset = True
            else:
                sys.exit(1)
    if created_or_reset:
        return []
    with open(filename, 'r', newline='') as fh:
        return [r for r in csv.DictReader(fh)]


def format_amount(amount):
    """Format numeric amounts using fixed-point with exactly 2 decimal places."""
    return format(amount, '.2f')


def display_table(data, cols):
    """Display expense data as table.

    Parameters:
      data (list): list of dicts
      cols (list): column names to display

    Returns:
      None

    Tests:
      - empty data shows no rows
      - multiple rows display aligned
    """
    if not data:
        print('No entries.')
        return
    widths = {c: max(len(c), max((len(str(r.get(c, ''))) for r in data), default=0)) for c in cols}
    print(' | '.join(f"{c:{widths[c]}}" for c in cols))
    print('-+-'.join('-' * widths[c] for c in cols))
    for row in data:
        print(' | '.join(f"{str(row.get(c, '')):{widths[c]}}" for c in cols))


def group_expenses(data, key):
    """Group expenses by date or category with sums.

    Parameters:
      data (list): list of dicts
      key (str): 'date' or 'category'

    Returns:
      None

    Tests:
      - group by date shows sums per date
      - group by category shows sums per category
    """
    grp = defaultdict(float)
    for row in data:
        try:
            grp[row[key]] += float(row['amount'])
        except (ValueError, KeyError):
            pass
    if not grp:
        print('No valid groups.')
        return
    print(f'\nGrouped by {key}:')
    for k in sorted(grp.keys()):
      print(f'{k}: {format_amount(grp[k])}')


def add_expense(data):
    """Prompt user to add expense; validate format; return True if added.

    Parameters:
      data (list): list of dicts to append to

    Returns:
      bool: True if added, False if cancelled

    Tests:
      - valid entry appended to data
      - invalid amount rejected
      - cancel option handled
    """
    while True:
        entry = input("Enter date,description,amount,category or '<' to cancel: ").strip()
        if entry == '<':
            return False
        parts = [p.strip() for p in entry.split(',')]
        if len(parts) != 4:
            print(PROMPTS['entry_error'])
            if input(PROMPTS['cancel_prompt']).strip().lower() in ('y', 'yes'):
                return False
            continue
        date, desc, amt, cat = parts
        try:
            float(amt)
            if not all([date, desc, cat]):
                raise ValueError('missing field')
            data.append({'id': '', 'date': date, 'description': desc, 'amount': amt, 'category': cat})
            return True
        except ValueError:
            print(PROMPTS['entry_error'])
            if input(PROMPTS['cancel_prompt']).strip().lower() in ('y', 'yes'):
                return False


def save_to_file(filename, data):
    """Save data to CSV with IDs for new entries.

    Parameters:
      filename (str): CSV file path
      data (list): list of dicts to save

    Returns:
      None

    Tests:
      - new entries get sequential IDs
      - file written correctly
    """
    max_id = 0
    for row in data:
        if row['id']:
            try:
                max_id = max(max_id, int(row['id']))
            except ValueError:
                pass
    for row in data:
        if not row['id']:
            max_id += 1
            row['id'] = str(max_id)
    with open(filename, 'w', newline='') as fh:
      writer = csv.DictWriter(fh, ['id', 'date', 'description', 'amount', 'category'], lineterminator='\n')
      writer.writeheader()
      writer.writerows(data)


def main(filename='expenses.csv'):
    """Menu-driven expense tracker.

    Parameters:
      filename (str): CSV file to load/save

    Returns:
      None

    Tests:
      - menu displays options
      - all 5 operations callable
      - save persists data
    """
    data = file_function(filename)
    while True:
        choice = input(PROMPTS['menu']).strip()
        if not choice:
            continue
        if choice == '1':
            display_table(data, ['date', 'description', 'amount', 'category'])
        elif choice == '2':
            key = input(PROMPTS['group_key']).strip().lower()
            if key.startswith('d'):
                group_expenses(data, 'date')
            elif key.startswith('c'):
                group_expenses(data, 'category')
            else:
                print(PROMPTS['invalid_choice'])
        elif choice == '3':
            add_expense(data)
        elif choice == '4':
            save_to_file(filename, data)
            print('Saved.')
        elif choice == '5':
            break
        else:
            print(PROMPTS['invalid_choice'])


if __name__ == '__main__':
    main()
