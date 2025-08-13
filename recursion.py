def printnew(n):
    if n==1:
        print(1)
        return
    printnew(n-1)
    print(n)
    
printnew(10)