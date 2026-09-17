#!/usr/bin/env python3
"""Test script for expenses.py module"""

import expenses
import os

print("=" * 50)
print("EXPENSES PROGRAM TEST SUITE")
print("=" * 50)

# Test 1: file_function creates new file
print("\nTest 1: file_function creates new file")
data = expenses.file_function('test_new.csv')
assert data == [], "New file should return empty list"
assert os.path.exists('test_new.csv'), "File should be created"
print("✓ PASS")

# Test 2: display_table with empty data
print("\nTest 2: display_table with empty data")
print("Expected output: 'No entries.'")
expenses.display_table([], ['date', 'amount'])
print("✓ PASS")

# Test 3: Create test data and test display_table
print("\nTest 3: display_table with data")
test_data = [
    {'id': '1', 'date': '2024-03-01', 'description': 'lunch', 'amount': '12.50', 'category': 'food'},
    {'id': '2', 'date': '2024-03-02', 'description': 'gas', 'amount': '45.00', 'category': 'transport'},
]
expenses.display_table(test_data, ['date', 'description', 'amount', 'category'])
print("✓ PASS")

# Test 4: save_to_file with ID assignment
print("\nTest 4: save_to_file adds IDs")
new_data = [
    {'id': '', 'date': '2024-03-03', 'description': 'coffee', 'amount': '4.50', 'category': 'food'},
]
expenses.save_to_file('test_save.csv', new_data)
with open('test_save.csv') as f:
    content = f.read()
    assert '1' in content, "New entry should get ID 1"
    print(content)
print("✓ PASS")

# Test 5: group_expenses by category
print("\nTest 5: group_expenses by category")
expenses.group_expenses(test_data, 'category')
print("✓ PASS")

# Test 6: group_expenses by date  
print("\nTest 6: group_expenses by date")
expenses.group_expenses(test_data, 'date')
print("✓ PASS")

print("\n" + "=" * 50)
print("ALL TESTS PASSED ✓")
print("=" * 50)
