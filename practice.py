import re

# Starts with a digit
print(re.findall(r"^[0-9]", "7 cats 9")) # ['7']
print(re.findall(r"^[0-9]", "cats 7")) # []

# Not a digit
print(re.findall(r"[^0-9]", "7cats 9"))  # ['c', 'a', 't', 's']


