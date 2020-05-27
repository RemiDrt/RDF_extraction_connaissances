#!/usr/bin/python
#coding=utf-8
def Sommets(texte) :
    """
    Fonction qui donne les sommets listés d'un fichier NRI_File
    Prend en paramètre la liste des lignes du fichier (créée avec readlines())
    Retourne un tableau des sommets
    """
    return texte[1].split("|")

def Attributs(texte) :
    """
    Fonction qui donne les attributs listés d'un fichier NRI_File
    Prend en paramètre la liste des lignes du fichier (créée avec readlines())
    Retourne un tableau des attributs
    """
    return texte[2].split("|")
