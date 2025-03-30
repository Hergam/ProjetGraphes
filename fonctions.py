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
           
            jDejaDeleted = any(j in ligne for ligne in deleted) # check si le sommet a deja été supprimé
            if not prede and not jDejaDeleted:
                deletable.append(j) #Si la liste des prédécésseurs est vide et si il n'a pas deja été supprimé, on ajoute
                                    # j à la liste des sommets supprimable.
        if deletable:
            for i in deletable:
                for j in dim:
                    matAdj[i][j]=0 # Mise a 0 des lignes correspondant aux successeurs des sommets supprimable 
            for j in range(len(deletable)):
                deleted[iteration][j]=deletable[j] # Ajout a la liste deleted des sommets ayant été supprimé a l'iteration
                                                #actuelle. Cette liste deviens ainsi les rangs du graphes.
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

def verif(matrice,f):
    
    matAdj,rangs = detectionCircuit(matrice)
        #print(tabulate(matAdj, headers=sommets)) # pour les tests
    if not(all(all(case == 0 for case in ligne) for ligne in matAdj)): #teste si la matrice de la detection de circuit n'a que des 0
                                                                    # (si la matrice de la detection de circuit n'a pas que des 0,
                                                                    # il y a un circuit dans le graphe.)
        print("\nCe graphe contient un circuit\n", file=f)
        return False,rangs
    else:
        print("\nCe graphe ne contient pas de circuit\n", file=f)
    for i in range(len(matrice)):
        if matrice[i][1]<0: # Check que pour toutes les durées des taches elles ne soient pas négatives
            print("\nCe graphe contient un arc a valeur négative\n", file=f)
        else:
            print("Ce graphe ne contient pas d'arc a valeur négative\n", file=f)
            return True,rangs
    
    
def dateTot(matrice,rangs):
    matAdj = adjacencePond(matrice)
    flatRangs = [item for sublist in rangs for item in sublist if item is not None]
    # met les sommets dans une liste par ordre de rangs croissant
    dateTo=[0]*len(matAdj) # Initialise les dates au plus tot à 0 pour tout les sommets
    for i, cell in enumerate(flatRangs): # chaque sommet dans la liste flatRangs (liste des sommets ordonnés par ordre croissant de rangs)
        if i > 0:    
            pred = matrice[cell][2:] #Récupère les prédécésseurs du sommet

            for z in pred: #Pour chaque prédécésseur du sommet faire
                if dateTo[z]+matrice[z][1]>=dateTo[cell]: #si date au plus tot(prédécésseur)+Durée Tache(prédécésseur)>date au plus tot actuelle du sommet,
                    dateTo[cell]=dateTo[z]+matrice[z][1]  # date au plus tot actuelle du sommet = date au plus tot(prédécésseur)+Durée Tache(prédécésseur)
                
    return dateTo

def dateTard(matrice, rangs):
    matAdj = adjacencePond(matrice)
    dateTo= dateTot(matrice,rangs)
    rangs_inverses = list(reversed(rangs)) 
    flatRangs = [item for sublist in rangs_inverses for item in sublist if item is not None] 
    #met les sommets dans une liste par ordre de rangs décroissant
    dateTa=[999]*len(matAdj) # initialise la date au plus tard de tout les sommets à 999
    dateTa[len(matAdj)-1]=dateTo[len(matAdj)-1] # initialise la date au plus tard du sommet W à la date au plus tot du sommet W
    for i, cell in enumerate(flatRangs): #Pour chaque sommet de la liste flatRangs
        if i > 0:
            ligneAdj = matAdj[cell]
        
            succ = [j for j, z in enumerate(ligneAdj) if z is not None] #récupère les succésseurs du sommet actuel
            for z in succ: # Pour chaque succésseurs du sommet actuel
                if dateTa[cell]>=dateTa[z]: # si date au plus tard(sommet actuel) > date au plus tard(succésseurs)
                    dateTa[cell]=dateTa[z] # alors date au plus tard(sommet actuel) = date au plus tard(succésseurs)
            dateTa[cell]-=matrice[cell][1] #on enleve la durée de la tache du sommet à sa date au plus tard
                
    return dateTa

def calcul_marges(matrice, rangs):
    # On récupère les dates au plus tôt pour chaque tâche
    d_tot = dateTot(matrice, rangs)
    
    # On récupère les dates au plus tard pour chaque tâche
    d_tard = dateTard(matrice, rangs)

    
    # CALCUL DES MARGES TOTALES
    
    marge_totale = []

    for i in range(len(matrice)):
        # La marge totale est la différence entre la date au plus tard et la date au plus tôt
        # Si elle vaut 0, la tâche est critique
        marge = d_tard[i] - d_tot[i]
        marge_totale.append(marge)

    
    # CALCUL DES MARGES LIBRES

    marge_libre = []

    for i in range(len(matrice)):
        successeurs = []

        # On cherche tous les successeurs de la tâche i
        for j in range(len(matrice)):
            # Si la tâche i est un prédécesseur de la tâche j
            if i in matrice[j][2:]:
                successeurs.append(j)

        # Si la tâche a des successeurs
        if successeurs:
            # On initialise avec la date au plus tôt du premier successeur
            min_d_tot_succ = d_tot[successeurs[0]]

            # On cherche le plus petit d_tot parmi les successeurs
            for j in successeurs:
                if d_tot[j] < min_d_tot_succ:
                    min_d_tot_succ = d_tot[j]

            # La marge libre est la date au plus tôt du plus rapide des successeurs
            # moins (la date au plus tôt de la tâche + sa durée)
            marge = min_d_tot_succ - (d_tot[i] + matrice[i][1])
        else:
            # Si la tâche n'a pas de successeurs, sa marge libre = marge totale
            marge = marge_totale[i]

        marge_libre.append(marge)

    # On retourne les deux listes de marges
    return marge_totale, marge_libre


def cheminsCritiques(matrice,marge_totale):
    matAdj = adjacencePond(matrice)

    def dfs(chemin, noeud_actuel, tous_les_chemins): # Fonction récursive pour parcourir le graphe et trouver les chemins
        chemin.append(noeud_actuel) # On ajoute au chemin actuel le sommet actuel
        if noeud_actuel == len(matrice) - 1: # si le sommet actuel est W
            tous_les_chemins.append(list(chemin)) #on ajoute le chemin a la liste de tout les chemins
            return
        ligneAdj = matAdj[noeud_actuel]
    
        succ = [j for j, z in enumerate(ligneAdj) if z is not None] # récupération des succésseurs du sommet actuel
        for i in succ: # Pour tout les succésseurs du sommet actuel, appeler la fonction récursive
            dfs(chemin,i,tous_les_chemins) 
            chemin.pop()
    
    tous_les_chemins = []
    dfs([], 0, tous_les_chemins) # initialisation de la fonction récursive au sommet alpha (0)

    chemins_critiques = [ #On met dans la liste des chemins critique tout les chemins n'ayant que des sommet ayant une marge totale = 0
        chemin for chemin in tous_les_chemins if all(marge_totale[i] == 0 for i in chemin) 
    ]

    return chemins_critiques
    
        
        

                

