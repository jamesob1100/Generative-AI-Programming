# converts a string to uppercase
def to_uppercase(s):
    return s.upper()

# returns the length of a string
def get_length(s):
    return len(s)

# checks if a substring is in a string
def contains_substring(s, substring):
    return substring in s

# replaces a substring with another substring
def replace_substring(s, old, new):
    return s.replace(old, new)

# splits a string into a list of words
def split_string(s):
    return s.split() 