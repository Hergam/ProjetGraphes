
numtableau = input("Enter table to test :")
f = open("contraintes/table "+str(numtableau)+".txt", "r")
tableau = f.read() 
print(tableau)
