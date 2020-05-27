#!/usr/bin/python
#coding=utf-8
#import des fonctions d'extractions spécifiques aux fichier NRI
from Extractors import *
#opening the file in read only
NRI_File = open("testfile.nri", encoding="utf-8")
#creer une liste avec toutes les lignes
texte = NRI_File.readlines()
#fermer le fichier pour éviter les problèmes
NRI_File.close()

sommets = Sommets(texte)
attributs = Attributs(texte)
itemsets = Itemsets(texte)
graphe = Graphe(texte)

AfficherListe(sommets)
AfficherListe(attributs)
AfficherDico(itemsets)
AfficherDico(graphe)
