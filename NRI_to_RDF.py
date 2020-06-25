from NRI_analyser import *

def ConvertToRDF(graphe, file) :
    """
    Fonction qui serialize un graphe rdflib en fichier turtle
    prend en paramètre un grapherdflib et un nom/chemin de fichier
    """
    graphe.serialize(destination=file, format="turtle", encoding="utf-8")


if __name__ == "__main__":
    NRI = ExtraireNRI("NRI_generate/CitationsP_XP4.nri")
    print(NRI)
    graphe = Graph()
    AnalyserNRI(graphe, NRI, "citationsp")
    ConvertToRDF(graphe, "ConvertedToRDF/CitationsP_XP4.ttl")

    graphe = Graph()
    NRI = ExtraireNRI("NRI_generate/CoAuteurs_XP1.nri")
    print(NRI)
    AnalyserNRI(graphe, NRI, "coauteurs")
    ConvertToRDF(graphe, "ConvertedToRDF/CoAuteurs_XP1.ttl")

    graphe = Graph()
    NRI = ExtraireNRI("NRI_generate/Citations_XP2.nri")
    print(NRI)
    AnalyserNRI(graphe, NRI, "citations")
    ConvertToRDF(graphe, "ConvertedToRDF/Citations_XP2.ttl")

    graphe = Graph()
    NRI = ExtraireNRI("NRI_generate/Copublications_XP3.nri")
    print(NRI)
    AnalyserNRI(graphe, NRI, "copublications")
    ConvertToRDF(graphe, "ConvertedToRDF/Copublications_XP3.ttl")

    graphe = Graph()
    NRI = ExtraireNRI("NRI_generate/Cooccurrences_XP5.nri")
    print(NRI)
    AnalyserNRI(graphe, NRI, "cooccurrences")
    ConvertToRDF(graphe, "ConvertedToRDF/Cooccurrences_XP5.ttl")

    graphe = Graph()
    NRI = ExtraireNRI("NRI_generate/CitationsE_XP6.nri")
    print(NRI)
    AnalyserNRI(graphe, NRI, "citationse")
    ConvertToRDF(graphe, "ConvertedToRDF/CitationsE_XP6.ttl")

    graphe = Graph()
    NRI = ExtraireNRI("NRI_generate/PubAut_bi_XP7.nri")
    print(NRI)
    AnalyserNRI(graphe, NRI, "pubaut")
    ConvertToRDF(graphe, "ConvertedToRDF/PubAut_bi_XP7.ttl")

    graphe = Graph()
    NRI = ExtraireNRI("NRI_generate/AutPubCitees_bi_XP8.nri")
    print(NRI)
    AnalyserNRI(graphe, NRI, "autpubcitees")
    ConvertToRDF(graphe, "ConvertedToRDF/AutPubCitees_bi_XP8.ttl")

    graphe = Graph()
    NRI = ExtraireNRI("NRI_generate/PubAutCites_bi_XP9.nri")
    print(NRI)
    AnalyserNRI(graphe, NRI, "pubautcites")
    ConvertToRDF(graphe, "ConvertedToRDF/PubAutCites_bi_XP9.ttl")

    print("done !\n----------------------------")