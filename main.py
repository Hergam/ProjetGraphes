from fonctions import *
from tabulate import tabulate

numTableau = input("Entrez le numéro de la table a tester : ")

filename = f"outputs/output_{numTableau}.txt"  # créé un fichier avec le numéro du graphe en titre

with open(filename, "w") as f:

    matrice = matrice_graphe(numTableau) # récupération de la matrice a partir de la fonction
    print(tabulate(matrice, headers=['Sommet', 'Durée', '1','2','3','4']), file=f) #Affichage joli de la matrice avec tabulate
    verification,rangs = verif(matrice,f) # verification de la conformité de la matrice (circuit et arcs négatifs)

    if not verification: #si la vérification n'est pas bonne (= False)
        print("Ce graphe n'est pas valide, il n'y aura pas de calcul de calendrier.", file=f)
    else:
        head=[]
        for i in range(len(rangs)):
            head.append("r="+str(i))
        transposed_rangs = list(map(list, zip(*rangs))) # transposée de la matrice des rangs pour une meilleure lisibilité

        print("\nRANGS :",file=f)

        print(tabulate(transposed_rangs, headers=head), file=f) # affichage des rangs

        d_tot = dateTot(matrice, rangs) # calcul des dates au plus tot
        d_tard = dateTard(matrice,rangs) # calcul des dates au plus tard
        
        marge_totale, marge_libre = calcul_marges(matrice,rangs) # calcul des marges

        print("\nRÉCAPITULATIF DES MARGES :",file=f)
        print(tabulate(
            [[i, d_tot[i], d_tard[i], marge_totale[i], marge_libre[i]] for i in range(len(matrice))],
            headers=["Tâche", "D. au plus tôt", "D. au plus tard", "Marge Totale", "Marge Libre"]
        ),file=f) # Affichage des Dates au plus tot/tard et marges

        chemins_critiques = cheminsCritiques(matrice, marge_totale) #Calcul des chemins critique

        print("\nCHEMINS CRITIQUES :" ,file=f)
        for chemin in chemins_critiques:
            print(" → ".join(map(str, chemin)),file=f) # Affichage des chemins critiques