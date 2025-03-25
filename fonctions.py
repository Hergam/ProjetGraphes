from tabulate import tabulate

def matrice_graphe(numTableau):
    f = open("contraintes/table "+str(numTableau)+".txt", "r")
    matrice = f.readlines()

    ligneW=[]
    sommets=range(1,len(matrice));

    for n in sommets:
        ligneW.append(n)

    for i in range(len(matrice)):
        matrice[i] = matrice[i].split()
        for j in range(len(matrice[i])):
            matrice[i][j]=int(matrice[i][j])
            if j>1:
                if matrice[i][j] in ligneW:
                    ligneW.remove(matrice[i][j])

    matrice.insert(0,[0,0])

    ligneW.insert(0,len(matrice))
    ligneW.insert(1,0)

    matrice.append(ligneW)

    print(tabulate(matrice, headers=['Sommet', 'Durée', '1','2','3','4']))
    return matrice

def adjacence(matrice):
    dim=len(matrice)
    MA=[[0]*dim]*dim
    for i in range(dim):
        for j in range(2,len(matrice[i])):
            pred=matrice[i][j]
            MA[pred][i]=1
            print(pred,i)

    
    print(MA)
    #sommets=range(len(matrice));
    #print(tabulate(MA, headers=sommets))


