def pal(str):
    if len(str)==1:
        return True
    if len(str)==2 and str[0]==str[-1]:
        return True
    if len(str)==2 and str[0]!=str[-1]:
        return False
    if str[0]==str[-1]:
        return pal(str[1:len(str)-1])
    else:
        return False
    
print(pal("hello"))
    