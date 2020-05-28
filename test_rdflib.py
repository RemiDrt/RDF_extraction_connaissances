#!/usr/bin/python
#coding=utf-8
import rdflib
g = rdflib.Graph()
print(len(g))
g.parse("acemap.ttl", format="turtle")
print(len(g))
for s, p, o in g :
    print("----------------\n")
    print(s)
    print(p)
    print(o)
    print("----------------\n")
