#!/usr/bin/python
#coding=utf-8
import rdflib
graphe = rdflib.Graph() #l'objet graphe pour l'instant vide qui contientdra tous les triplets
print(len(g))
graphe.parse("field.ttl", format="turtle") #on lui ajouter tous les triplets venant du fichier field.ttl
print("done")
print(len(g))

for sujet, predica, objet in graphe :
    print("----------------\n")
    print(sujet)
    print(predica)
    print(objet)
    print("----------------\n")
