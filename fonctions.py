from tabulate import tabulate

def matrice_graphe(numTableau):
    f = open("contraintes/table "+str(numTableau)+".txt", "r")
    matrice = f.readlines()

    ligneW=[]
    ligneA=[]
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
            if len(matrice[i])<3:
                matrice[i].append(0)
            

    matrice.insert(0,[0,0])

    ligneW.insert(0,len(matrice))
    ligneW.insert(1,0)

    matrice.append(ligneW)

    print(tabulate(matrice, headers=['Sommet', 'Durée', '1','2','3','4']))
    return matrice

def adjacence(matrice):
    dim=len(matrice)
    
    matAdj = [[0 for i in range(dim)] for j in range(dim)]
    for i in range(dim):
        for j in range(2,len(matrice[i])):
            pred=matrice[i][j]
            matAdj[pred][i]=1
    
    return matAdj
    
    #sommets=range(len(matrice)) 
    #print(tabulate(matAdj, headers=sommets))
    #Pour le test de la matrice d'adjacence

def verif(matrice):
    matAdj = adjacence(matrice)
    dim = range(len(matAdj))
    #sommets=range(len(matrice)) # pour les tests
    deleted = []
    
    for iteration in dim:
        deletable = False
        for j in dim:
            prede=[]
            for i in dim:
                if matAdj[i][j]==1:
                    prede.append(i);
            if not prede and j not in deleted:
                deletable = j
        if deletable!=[]:
            for j in dim:
                matAdj[deletable][j]=0
            deleted.append(deletable)
        #print(tabulate(matAdj, headers=sommets)) # pour les tests
    if not(all(all(case == 0 for case in ligne) for ligne in matAdj)):
        print("\n\nCe graphe contient un circuit")
        return False
    else:
        print("Ce graphe ne contient pas de circuit")
    
