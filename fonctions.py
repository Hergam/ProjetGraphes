from tabulate import tabulate

def matrice_graphe(numTableau): 
    f = open("contraintes/table "+str(numTableau)+".txt", "r")
    matrice = f.readlines()
    
    #On ouvre le fichier texte et met chaque ligne dans une liste.

    ligneW=[]
    sommets=range(1,len(matrice)+1)
    #étant donné qu'on va ajouter 2 sommets (alpha et w), 
    # on doit créer les sommets allant de 1 à N (range(4)=[0,1,3])


    for n in sommets:
        ligneW.append(n) #j'initialise une ligne dans laquelle on va mettre les informations relatant au sommet w
        #On met d'abord dans cette liste tout les sommets du graphe. Dans l'étape suivante, on enlevera de cette liste
        #tout les sommets ayant un ou plusieurs ,(c'est a dire tout les sommets ayant deja un succésseur)

    for i in range(len(matrice)):
        
        matrice[i] = matrice[i].split() #Je split les lignes du fichier texte pour qu'il ne reste que les nombres, sans les espaces.
        for j in range(len(matrice[i])):
            matrice[i][j]=int(matrice[i][j]) #Je converti le texte en nombre entier
            if j>1:
                if matrice[i][j] in ligneW: #J'enleve les sommets présent dans les prédécesseurs d'un sommets de la ligneW
                    ligneW.remove(matrice[i][j]) # Afin qu'il ne reste que les sommets n'ayant pas de succésseur.
            if len(matrice[i])<3:
                matrice[i].append(0)
            

    matrice.insert(0,[0,0]) #j'ajoute a début de ma matrice de graphe la ligne [0,0] correspondant au sommet alpha

    ligneW.insert(0,len(matrice)) # j'ajoute le reste des informations concernant le sommet w
    ligneW.insert(1,0) 

    matrice.append(ligneW) #j'insert a la fin du graphe la ligne concernant le sommet w

    print(tabulate(matrice, headers=['Sommet', 'Durée', '1','2','3','4'])) #Affichage joli de la matrice avec tabulate
    return matrice

def adjacence(matrice):
    dim=len(matrice)
    
    matAdj = [[None for i in range(dim)] for j in range(dim)] #création de la matrice d'adjacence de taille [nombre de sommets]
    for i in range(dim):
        for j in range(2,len(matrice[i])):
            pred=matrice[i][j] 
            matAdj[pred][i]=1
    #Pour chaque sommet, je regarde les prédécesseurs de celui-ci, et met un 1 dans la colonne correspondante au sommet

    return matAdj

def adjacencePond(matrice):
    dim=len(matrice)
    
    matAdjPond = [[None for i in range(dim)] for j in range(dim)]
    for i in range(dim):
        for j in range(2,len(matrice[i])):
            pred=matrice[i][j]
            matAdjPond[pred][i]=matrice[pred][1]
    #Meme chose que pour la matrice adjacence mais a la place d'un 1, je met la durée de la tache, 
    # afin d'avoir toute les informations nécéssaires dans la matrice

    return matAdjPond
    
    #sommets=range(len(matrice)) 
    #print(tabulate(matAdj, headers=sommets))
    #Pour le test de la matrice d'adjacence

def detectionCircuit(matrice):
    matAdj = adjacence(matrice)
    dim = range(len(matAdj))
    #sommets=range(len(matrice)) # pour les tests
    deleted = [[None for i in dim] for j in dim] 
    #La matrice deleted contient tout les sommets étant supprimés du graphes par ordre de rang

    for iteration in dim: #Pour chaque itération de l'algo faire : 
        #(On utilise le nombre de sommets du graphe comme nombre d'iteration max ; 
        # il ne peut pas avoir plus d'iterations que de sommets)

        deletable = [] #La liste deletable contiendra tout les sommets n'ayant 
                        #pas de prédécésseurs dans l'itération actuelle
        
        for j in dim: # Pour chaque sommet du graphe faire : 
            prede=[]
            for i in dim:  #cette boucle permet de mettre tout les prédecésseurs du sommet i dans la liste prede
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

    return marge_totale



def cheminsCritiques(matrice,marge_totale):
    matAdj = adjacencePond(matrice)
    def dfs(chemin, noeud_actuel, tous_les_chemins):
        chemin.append(noeud_actuel)  
        if noeud_actuel == len(matrice) - 1:
            tous_les_chemins.append(list(chemin))  
            return
        ligneAdj = matAdj[noeud_actuel]
    
        succ = [j for j, z in enumerate(ligneAdj) if z is not None]
        for i in succ:
            dfs(chemin,i,tous_les_chemins)
            chemin.pop()
    
    tous_les_chemins = []
    dfs([], 0, tous_les_chemins)

    chemins_critiques = [
        chemin for chemin in tous_les_chemins if all(marge_totale[i] <= 0 for i in chemin)
    ]

    print("\nCHEMINS CRITIQUES :")
    for chemin in chemins_critiques:
        print(" → ".join(map(str, chemin)))
        
        

                

