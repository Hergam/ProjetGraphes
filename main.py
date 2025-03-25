
numTableau = input("Enter table to test :")
f = open("contraintes/table "+str(numTableau)+".txt", "r")
texte = f.readlines()
tableau = [[]]
for i in range(len(texte)):
    splittedLine = texte[i].split()
    tableau[i][0]=splittedLine[0]
    tableau[i][1]=splittedLine[1]
    for j in range(2,len(splittedLine)):
        tableau[i][j]=splittedLine[j]

print(tableau)

