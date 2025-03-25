from tabulate import tabulate



numTableau = input("Enter table to test :")
f = open("contraintes/table "+str(numTableau)+".txt", "r")
texte = f.readlines()

tableau = []
for i in range(len(texte)):
    texte[i] = texte[i].split()

print(tabulate(texte, headers=['Sommet', 'Durée', '1','2','3','4']))
