books=[]
author=[]
publisher=[]
genre=[]
availability=[]
x="yes"
print("Library Management System")
print("===========================")
while (True):
    print("1. Add New Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. Book Catalogue")
    print("5. Exit")
    ch=int(input("Please enter your choice (1-5):"))
    if ch==1:
        while x=="yes":
            n=input("Enter book name:")
            books+=[n]
            n=input("Enter author's name:")
            author+=[n]
            n=input("Enter publisher's name:")
            publisher+=[n]
            n=input("Enter genre of book:")
            genre+=[n]
            n=input("Enter availability:")
            availability+=[n]
            x=input("Do you want to add more books?(yes/no):")
    elif ch==2:
        print("The list of books available are:")
        for i in range(len(availability)):
        	if availability[i]=="available":
        		print(books[i])
        issue=input("Enter book to issue:")
        print(issue, "has been issued.")
        availability[books.index(issue)]="issued"
    elif ch==3:
        ret=input("Book to be returned:")
        availability[books.index(ret)]="available"
        print(ret, "has been returned.")
    elif ch==4:
        for i in range(len(books)):
            print("Book Name:", books[i])
            print("Book Author:", author[i])
            print("Publisher:", publisher[i])
            print("Genre", genre[i])
            print("Availability:", availability[i])
            print()
    else:
        print('Thank you for using Library Management System.')
        break
