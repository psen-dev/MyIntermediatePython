import re
str="Mr. Sam Ms. Rose Mrs. Norris"
print(re.findall(r"M(r|s|rs)\.\s(Sam|Rose|Norris)",str))
match=(re.search(r"M(r|s|rs)\.\s(Sam|Rose|Norris)",str))
print(match.group())
print(match.groups())
print(match.group(1))
print(match.group())