from NRI_analyser import *

def ConvertToRDF(graphe, file) :
    """
    Fonction qui serialize un graphe rdflib en fichier turtle
    prend en paramètre un grapherdflib et un nom/chemin de fichier
    """
    graphe.serialize(destination=file, format="turtle", encoding="utf-8")

def ConvertNRIToRDF(NRIFile, RDFFile, graphe, relation):
    """
    Fonction qui converti un fichier NRI en fichier RDF
    Prend en paramètre un fichier NRI a convertir, un fichier RDF qui sera la destination, un graphe rdflib, et la relation du fichier NRI
    analyse le fichier NRI et ajoute les triplet dans le graphe en fonction de la relation. Serialize le graphe le fichier de destination
    """
    global ace
    NRI = ExtraireNRI(NRIFile)
    graphe.bind("ace", ace)
    AnalyserNRI(graphe, NRI, relation)
    ConvertToRDF(graphe, RDFFile)

if __name__ == "__main__":
    graphe = Graph()
    ConvertNRIToRDF("NRI_generate/CitationsP_XP4.nri", "ConvertedToRDF/CitationsP_XP4.ttl", graphe, "citationsp")

    graphe = Graph()
    ConvertNRIToRDF("NRI_generate/CoAuteurs_XP1.nri", "ConvertedToRDF/CoAuteurs_XP1.ttl", graphe, "coauteurs")

    graphe = Graph()
    ConvertNRIToRDF("NRI_generate/Citations_XP2.nri", "ConvertedToRDF/Citations_XP2.ttl", graphe, "citations")

    graphe = Graph()
    ConvertNRIToRDF("NRI_generate/Copublications_XP3.nri", "ConvertedToRDF/Copublications_XP3.ttl", graphe, "copublications")


    graphe = Graph()
    ConvertNRIToRDF("NRI_generate/Cooccurrences_XP5.nri", "ConvertedToRDF/Cooccurrences_XP5.ttl", graphe, "cooccurrences")


    graphe = Graph()
    ConvertNRIToRDF("NRI_generate/CitationsE_XP6.nri", "ConvertedToRDF/CitationsE_XP6.ttl", graphe, "citationse")


    graphe = Graph()
    ConvertNRIToRDF("NRI_generate/PubAut_bi_XP7.nri", "ConvertedToRDF/PubAut_bi_XP7.ttl", graphe, "pubaut")


    graphe = Graph()
    ConvertNRIToRDF("NRI_generate/AutPubCitees_bi_XP8.nri", "ConvertedToRDF/AutPubCitees_bi_XP8.ttl", graphe, "autpubcitees")

    graphe = Graph()
    ConvertNRIToRDF("NRI_generate/PubAutCites_bi_XP9.nri", "ConvertedToRDF/PubAutCites_bi_XP9.ttl", graphe, "pubautcites")

    print("done !\n----------------------------")