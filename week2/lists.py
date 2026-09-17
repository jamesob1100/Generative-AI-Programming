# list of 10 names
names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]

# list contains
def contains_name(name_list, name):
    return name in name_list 

# reverse order of the list
def reverse_names(name_list):
    return name_list[::-1]

# remove an element by value
def remove_name(name_list, name):
    if name in name_list:
        name_list.remove(name)
    return name_list

# replace sublist with another sublist
def replace_sublist(name_list, old_sublist, new_sublist):
    start_index = -1 # find start index of old_sublist
    for i in range(len(name_list) - len(old_sublist) + 1): # check for sublist match
        if name_list[i:i+len(old_sublist)] == old_sublist: # match found
            start_index = i 
            break
    if start_index != -1: # replace old_sublist with new_sublist
        name_list[start_index:start_index+len(old_sublist)] = new_sublist 
    return name_list

# print functions for testing
print(names)  # Original list
print(contains_name(names, "Alice"))  # True
print(reverse_names(names))  # Reversed list
print(remove_name(names, "Eve"))  # List without "Eve"
print(replace_sublist(names, ["Charlie", "Diana",], ["Xander", "Yara", "Anna"]))  # List with sublist replaced