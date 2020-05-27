#!/usr/bin/python
#coding=utf-8
def Sommets(texte) :
    """
    Fonction qui donne les sommets listés d'un fichier NRI
    Prend en paramètre la liste des lignes du fichier (créée avec readlines())
    Retourne un tableau des sommets
    """
    return texte[1].split("|")

def Attributs(texte) :
    """
    Fonction qui donne les attributs listés d'un fichier NRI
    Prend en paramètre la liste des lignes du fichier (créée avec readlines())
    Retourne un tableau des attributs
    """
    return texte[2].split("|")

def Itemsets(texte) :
    """
    Fonction qui donne l'itemsets d'un fichier NRI
    Prend en paramètre la liste des lignes du fichier (créée avec readlines())
    Retourne un tableau associatif/dictionnaire des sommet->attributs
    """
    itemsets = dict()
    #on commence a la 4eme ligne
    i = 3
    # le diese marque la fin de l'itemsets dans le fichier mais comme il y peut-être un espace on vérifie le premier carac de la ligne
    while texte[i][0] != "#" :
        tab1 = texte[i].split() #on sépare avec l'espace pour avoir d'un coté le numéros de sommet et de l'autre les numéros d'attributs
        nSommet = int(tab1[0])
        if len(tab1) > 1 : #attention aussi si on se retrouve avec un sommet sans attribut la vase tab[1] n'existe pas faudra la vérifier
            listAttributs = tab1[1].split(",") #attention listAttribut est un liste de numéros mais ce sont des String
        else :
            listAttributs = [] #un tableau vide
        itemsets[nSommet] = listAttributs
        i += 1
    return itemsets

def AfficherListe(liste):
    for item in liste :
        print(item)

def AfficherDico(dico):
    n = len(dico)
    i = 0
    print("{")
    while i < n :
        j = 0
        o = len(dico[i])
        ligne = str(i) + "=>{"
        while j < o :
            if j == o - 1 :
                ligne += dico[i][j]
            else :
                ligne += dico[i][j] + ","
            j += 1
        ligne += "}"
        print(ligne)
        i += 1
    print("}")
