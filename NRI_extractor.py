#!/usr/bin/python
#coding=utf-8
def Sommets(ligne) :
    """
    Fonction qui donne les sommets listés d'un fichier NRI_File
    Prend en paramètre la ligne comprenant les sommets
    Retourne un tableau des sommets
    """
    return ligne.split("|")
print("Hello world")
#opening the file in read only
NRI_File = open("../Graphes_attribués_NRI/acl_XP1_aut_pub.nri", encoding="utf-8")
#creer une liste avec toutes les lignes
texte = NRI_File.readlines()
#fermer le fichier pour éviter les problèmes
NRI_File.close()
#parcourir les lignes en sachant ou on est avec ind_ligne
#ind_ligne = 1
#for ligne in texte :
#print(texte[1])
sommets = Sommets(texte[1])
for sommet in sommets :
    print(sommet)
