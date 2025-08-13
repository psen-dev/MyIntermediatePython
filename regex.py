import re

text = "apple, banana orange,pear"
parts = re.split(r"[ ,]+", text)
print(parts)

parts = re.split(r"([ ,])+", text)
print(parts)

