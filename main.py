from fonctions import *
from tabulate import tabulate

numTableau = input("Entrez le numéro de la table a tester : ")

matrice = matrice_graphe(numTableau)

verification,rangs = verif(matrice)

if not verification:
    print("Ce graphe n'est pas valide, il n'y aura pas de calcul de calendrier.")
else:
    head=[]
    for i in range(len(rangs)):
        head.append("r="+str(i))
    transposed_rangs = list(map(list, zip(*rangs)))
    print(tabulate(transposed_rangs, headers=head))

    margeTot=calcul_marges(matrice,rangs)

    cheminsCritiques(matrice, margeTot)