def reverse(str):
    if len(str)==1:
        return str
    str=reverse(str[1:])+str[0]
    return str
print(reverse("hello"))