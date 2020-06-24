from Extractors import *
from NRI_analyser import *


def ConvertToRDF(graphe, file) :
    """
    Fonction qui serialize un graphe rdflib en fichier turtle
    prend en paramètre un grapherdflib et un nom/chemin de fichier
    """
    graphe.serialize(destination=file, format="turtle", encoding="utf-8")

citations = open("NRI_generate/CitationsP_XP4.nri", encoding="utf-8")
contenu = citations.readlines()
NRICitations = ExtraireNRI(contenu)
print(NRICitations)
graphe = Graph()
AnalyserNRI(graphe, NRICitations, "citationsp")
ConvertToRDF(graphe, "convertedToRDF/test1.ttl")
