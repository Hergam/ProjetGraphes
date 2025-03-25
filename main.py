from tabulate import tabulate

numTableau = input("Enter table to test :")
f = open("contraintes/table "+str(numTableau)+".txt", "r")
texte = f.readlines()
texte.insert(0,'0 0\n')

ligneW=[]
sommets=range(1,len(texte));

for n in sommets:
    ligneW.append(n)


for i in range(len(texte)):
    texte[i] = texte[i].split()
    for j in range(len(texte[i])):
        texte[i][j]=int(texte[i][j])
        if j>1:
            if texte[i][j] in ligneW:
                ligneW.remove(texte[i][j])

ligneW.insert(0,len(texte))
ligneW.insert(1,0)
texte.append(ligneW)

print(tabulate(texte, headers=['Sommet', 'Durée', '1','2','3','4']))
