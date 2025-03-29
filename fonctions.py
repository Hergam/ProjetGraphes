from tabulate import tabulate

def matrice_graphe(numTableau):
    f = open("contraintes/table "+str(numTableau)+".txt", "r")
    matrice = f.readlines()

    ligneW=[]
    ligneA=[]
    sommets=range(1,len(matrice)+1);

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
    
    matAdj = [[None for i in range(dim)] for j in range(dim)]
    for i in range(dim):
        for j in range(2,len(matrice[i])):
            pred=matrice[i][j]
            matAdj[pred][i]=1
    
    return matAdj

def adjacencePond(matrice):
    dim=len(matrice)
    
    matAdjPond = [[None for i in range(dim)] for j in range(dim)]
    for i in range(dim):
        for j in range(2,len(matrice[i])):
            pred=matrice[i][j]
            matAdjPond[pred][i]=matrice[pred][1]
    
    return matAdjPond
    
    #sommets=range(len(matrice)) 
    #print(tabulate(matAdj, headers=sommets))
    #Pour le test de la matrice d'adjacence

def detectionCircuit(matrice):
    matAdj = adjacence(matrice)
    dim = range(len(matAdj))
    #sommets=range(len(matrice)) # pour les tests
    deleted = [[None for i in dim] for j in dim]
    for iteration in dim:
        deletable = []
        
        for j in dim:
            prede=[]
            for i in dim:
                if matAdj[i][j]==1:
                    prede.append(i);
            jDejaDeleted = any(j in ligne for ligne in deleted)
            if not prede and not jDejaDeleted:
                deletable.append(j)
        if deletable:
            for i in deletable:
                for j in dim:
                    matAdj[i][j]=0
            for j in range(len(deletable)):
                deleted[iteration][j]=deletable[j]
        deletable = []
    
    #diminution de la taille de la table deleted vers la taille nécéssaire
    lastColNotEmpty=0
    deleted = [ligne for ligne in deleted if any(cell is not None for cell in ligne)]
    for i in range(len(deleted)):
        for j in dim:
            if deleted[i][j] is not None and lastColNotEmpty<j:
                lastColNotEmpty=j
    deleted = [ligne[:lastColNotEmpty + 1] for ligne in deleted]

    return matAdj,deleted

def verif(matrice):
    
    matAdj,rangs = detectionCircuit(matrice)
        #print(tabulate(matAdj, headers=sommets)) # pour les tests
    if not(all(all(case == 0 for case in ligne) for ligne in matAdj)): #teste si la matrice n'a que des 0
        print("\nCe graphe contient un circuit\n")
        return False,rangs
    else:
        print("\nCe graphe ne contient pas de circuit\n")
    for i in range(len(matrice)):
        if matrice[i][1]<0:
            print("\nCe graphe contient un arc a valeur négative\n")
        else:
            print("Ce graphe ne contient pas d'arc a valeur négative\n")
            return True,rangs
    
    
def dateTot(matrice,rangs):
    matAdj = adjacencePond(matrice)
    flatRangs = [item for sublist in rangs for item in sublist]
    dateTo=[0]*len(matAdj)
    dateTo[0]=0
    for i, cell in enumerate(flatRangs):
        if i > 0:
            if cell is not None:    

                pred = []
                for j in range(2,len(matrice[cell])):
                    pred.append(matrice[cell][j])

                for z in pred:
                    if dateTo[z]+matrice[z][1]>=dateTo[cell]:
                        dateTo[cell]=dateTo[z]+matrice[z][1]
                
    return dateTo

def dateTard(matrice, rangs):
    matAdj = adjacencePond(matrice)
    dateTo= dateTot(matrice,rangs)
    rangs_inverses = list(reversed(rangs))
    flatRangs = [item for sublist in rangs_inverses for item in sublist]
    dateTa=[999]*len(matAdj)
    dateTa[len(matAdj)-1]=dateTo[len(matAdj)-1]
    for i, cell in enumerate(flatRangs):
        if i > 0:
            if cell is not None:    
                ligneAdj = matAdj[cell]
            
                succ = []
                for j,z in enumerate(ligneAdj):
                    if z is not None:
                        succ.append(j)
                for z in succ:
                    if dateTa[cell]>=dateTa[z]:
                        
                        dateTa[cell]=dateTa[z]
                dateTa[cell]-=matrice[cell][1]
                
    return dateTa

def calcul_marges(matrice, rangs):
    d_tot = dateTot(matrice,rangs)
    d_tard = dateTard(matrice,rangs)
    print(d_tard)
    print(d_tot)
    #Calcul de la marge totale
    marge_totale = []
    for i in range (len(matrice)):
        marge = d_tard[i] - d_tot[i]
        marge_totale.append(marge)

    marge_libre = []
    for i in range (len(matrice)):
        successeurs = []

        
        for j in range (len(matrice)):
            if i in matrice[j][2:]:
                successeurs.append(j)
               
        
        if successeurs:
            min_d_tot_succ = d_tot[successeurs[0]]
            for j in successeurs:
                if d_tot[j] < min_d_tot_succ:
                    min_d_tot_succ = d_tot[j]
            marge = min_d_tot_succ - (d_tot[i] + matrice[i][1])
        
        else:
            marge = marge_totale[i]
        
        marge_libre.append(marge)


    print("\nRÉCAPITULATIF DES MARGES :")
    print(tabulate(
    [[i, d_tot[i], d_tard[i], marge_totale[i], marge_libre[i]] for i in range(len(matrice))],
    headers=["Tâche", "D. au plus tôt", "D. au plus tard", "Marge Totale", "Marge Libre"]
    ))

    trouver_chemins_critiques(matrice, marge_totale)
    

def trouver_chemins_critiques(matrice, marge_totale):
    # Fonction interne récursive pour faire une recherche en profondeur 
    def dfs(chemin, noeud_actuel, tous_les_chemins):
        # Si on atteint le dernier sommet (tâche de fin), on ajoute le chemin trouvé
        if noeud_actuel == len(matrice) - 1:
            tous_les_chemins.append(list(chemin))  
            return
        
        for i in range(len(matrice)):
            # Si la tâche actuelle est un prédécesseur de la tâche i
            if noeud_actuel in matrice[i][2:] and marge_totale[i] == 0:
                chemin.append(i)            # On ajoute i au chemin en cours
                dfs(chemin, i, tous_les_chemins)  # Appel récursif depuis la tâche i
                chemin.pop()               

    tous_les_chemins = []
    dfs([0], 0, tous_les_chemins)
    print("\nCHEMINS CRITIQUES :")
    for chemin in tous_les_chemins:
        print(" → ".join(map(str, chemin)))


                    
                

