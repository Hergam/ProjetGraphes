from fonctions import *
from tabulate import tabulate

numTableau=0
while numTableau != "exit":
    numTableau = input("Entrez le numéro de la table a tester : (taper 'exit' pour stopper le programme)")
    if numTableau == "exit":
        break
    filename = f"outputs/output_{numTableau}.txt"  # créé un fichier avec le numéro du graphe en titre

    with open(filename, "w") as f:

        matrice = matrice_graphe(numTableau) # récupération de la matrice a partir de la fonction
        
        matVal = matriceValeurs(matrice,f)
        affmatVal = [row[:] for row in matVal]  # Creation d'une copie de matVal pour l'affichage
        
        sommets=list(range(len(matrice))) 
        sommets.insert(0,"Tâche")
        for i in range(len(affmatVal)):
            affmatVal[i].insert(0,i)

        print("\n",file=f)
        print("\n")
        affmatVal = [[element if element is not None else '*' for element in row] for row in affmatVal] #Remplacemement des None par des *
        print(tabulate(
                [affmatVal[i] for i in range(len(matrice))],
                headers=sommets
            ),file=f)
        print(tabulate(
                [affmatVal[i] for i in range(len(matrice))],
                headers=sommets
            ))
        #Affichage joli de la matrice avec tabulate

        verification,rangs = verif(matrice,f) # verification de la conformité de la matrice (circuit et arcs négatifs)

        if not verification: #si la vérification n'est pas bonne (= False)
            print("Ce graphe n'est pas valide, il n'y aura pas de calcul de calendrier.", file=f)
            print("Ce graphe n'est pas valide, il n'y aura pas de calcul de calendrier.")
        else:
            head=[]
            for i in range(len(rangs)):
                head.append("r="+str(i))
            transposed_rangs = list(map(list, zip(*rangs))) # transposée de la matrice des rangs pour une meilleure lisibilité

            print("\n\nRANGS :",file=f)
            print("\n\nRANGS :")

            print(tabulate(transposed_rangs, headers=head), file=f) # affichage des rangs
            print(tabulate(transposed_rangs, headers=head))

            d_tot = dateTot(matrice, rangs, matVal,f) # calcul des dates au plus tot
            d_tard = dateTard(matrice,rangs, matVal, d_tot,f) # calcul des dates au plus tard
            
            marge_totale, marge_libre = calcul_marges(matrice,rangs,d_tot,d_tard) # calcul des marges

            print("\n\nRÉCAPITULATIF DES MARGES :",file=f)
            print("\n\nRÉCAPITULATIF DES MARGES :")
            print(tabulate(
                [[i, d_tot[i], d_tard[i], marge_totale[i], marge_libre[i]] for i in range(len(matrice))],
                headers=["Tâche", "D. au plus tôt", "D. au plus tard", "Marge Totale", "Marge Libre"]
            ),file=f) # Affichage des Dates au plus tot/tard et marges

            print(tabulate(
                [[i, d_tot[i], d_tard[i], marge_totale[i], marge_libre[i]] for i in range(len(matrice))],
                headers=["Tâche", "D. au plus tôt", "D. au plus tard", "Marge Totale", "Marge Libre"]
            )) 


            print("\n\nCALCUL DES CHEMINS CRITIQUES :" ,file=f)
            print("\n\nCALCUL DES CHEMINS CRITIQUES :")

            chemins_critiques = cheminsCritiques(matrice, marge_totale,matVal,f) #Calcul des chemins critique
            
            print("\nChemins critiques :" ,file=f)
            print("\nChemins critiques :")
            for chemin in chemins_critiques:
                print(" → ".join(map(str, chemin)),file=f) # Affichage des chemins critiques
                print(" → ".join(map(str, chemin)))