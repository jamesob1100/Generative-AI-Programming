# function that takes two lists of strings, joins them together, 
# discards any duplicates and orders the list alphabetically
def merge_and_sort_lists(list1, list2):
    # Combine the two lists
    combined = list1 + list2
    # Remove duplicates by converting to a set and back to a list
    unique_list = list(set(combined))
    # Sort alphabetically
    unique_list.sort()
    return unique_list

# call to the function at the bottom of the file, passing in two lists of words, 
# each containing at least three alphabetically out-of-order elements and with at least one duplicate between them
list1 = ["zebra", "apple", "banana", "cherry"]
list2 = ["date", "apple", "fig", "grape"]
result = merge_and_sort_lists(list1, list2)
print(result)