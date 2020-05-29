#!/usr/bin/python
#coding=utf-8
from Extractors import *
graphe = getGrapheRDF("field.ttl")
print(graphe)
print("\n-----------------\n")
graphe.bind("ace", "http://www.semanticweb.org/acemap#")
graphe.bind("ptdr", "http://biteurr#")
"""for index, (s, p, o) in enumerate(graphe):
    print((s, p, o))
    if index == 10 :
        break
file = open("test3.ttl", "w")
file.write(graphe.serialize(format='ttl').decode("utf-8"))"""
#for field in graphe.subjects(RDF.type, "http://www.semanticweb.org/acemap#Field") :
name = URIRef("http://www.semanticweb.org/acemap#field_name")
for field in graphe.subjects():
 for obj in graphe.objects(field, name) :
     print(obj)


#AfficherTriplets(graphe)
