from NRI_analyser import *
from rdflib import Graph
import time

def ConvertToRDF(graphe, file) :
    """
    Fonction qui serialize un graphe rdflib en fichier turtle
    prend en paramètre un grapherdflib et un nom/chemin de fichier
    """
    print("création de votre fichier ttl ... ")
    graphe.serialize(destination=file, format="turtle", encoding="utf-8")

def ConvertNRIToRDF(NRIFile, RDFFile, graphe, relation, IDToAuthor=None, IDToField=None, IDToPaper=None, AuthorToID=None, FieldToID=None):
    """
    Fonction qui converti un fichier NRI en fichier RDF
    Prend en paramètre un fichier NRI a convertir, un fichier RDF qui sera la destination, un graphe rdflib, et la relation du fichier NRI
    analyse le fichier NRI et ajoute les triplet dans le graphe en fonction de la relation. Serialize le graphe le fichier de destination
    """
    global ace
    print("convertion de " + NRIFile + " vers " + RDFFile)
    NRI = ExtraireNRI(NRIFile)
    graphe.bind("ace", ace)
    AnalyserNRI(graphe, NRI, relation, IDToAuthor=IDToAuthor, IDToField=IDToField, IDToPaper=IDToPaper, AuthorToID=AuthorToID, FieldToID=FieldToID)
    ConvertToRDF(graphe, RDFFile)


def ConvertMultipleNRIToRDF(NRIFileToRelation, RDFFile, graphe, IDToAuthor=None, IDToField=None, IDToPaper=None, AuthorToID=None, FieldToID=None) :
    """
    Fonction qui analyse plusieurs fichiers NRI et converti le tout en un fichier RDF.
    Prend en paramètres un dictionnaire associant des fichiers NRI a leurs relations, un fichier RDF de destination et un graphe rdflib.
    Analyse les fichiers en fonctions de leur relation, ajoute les triplet au graphe rdflib puis serialize le graphe dans le fichier de destination
    """
    global ace
    items = NRIFileToRelation.items()
    graphe.bind("ace", ace)
    for file, relation in items :
        print("Extraction et conversion de " + file)
        NRI = ExtraireNRI(file)
        AnalyserNRI(graphe, NRI, relation, IDToAuthor=IDToAuthor, IDToField=IDToField, IDToPaper=IDToPaper, AuthorToID=AuthorToID, FieldToID=FieldToID)
    ConvertToRDF(graphe, RDFFile)
    print("conversion en RDF terminée !")

if __name__ == "__main__":

    deb = time.time()
    graphe = Graph()

    #en faisant importFromJSON à la place de importFromJSONstruct, les dico ne contiennent pas d'uri, juste ds chaines de caractère
    IDToAuthor = ImportFromJSON("JSON_struct/IDToAuthor.json")
    IDToField = ImportFromJSON("JSON_struct/IDToField.json")
    IDToPaper = ImportFromJSON("JSON_struct/IDToPaper.json")

    #construire le dictionnaire avec tous les fichiers associés a leurs relation
    dicoFichiers = dict()

    #dicoFichiers["TestsSampleXKG/CitationsP_XP4.nri"] = "citationsp"
    #dicoFichiers["TestsSampleXKG/CoAuteurs_XP1.nri"] = "coauteurs"
    #dicoFichiers["TestsSampleXKG/Citations_XP2.nri"] = "citations"
    #dicoFichiers["TestsSampleXKG/Copublications_XP3.nri"] = "copublications"
    #dicoFichiers["TestsSampleXKG/Cooccurrences_XP5.nri"] = "cooccurrences"
    #dicoFichiers["TestsSampleXKG/CitationsE_XP6.nri"] = "citationse"
    #dicoFichiers["TestsSampleXKG/PubAut_bi_XP7.nri"] = "pubaut"
    #dicoFichiers["TestsSampleXKG/AutPubCitees_bi_XP8.nri"] = "autpubcitees"
    #dicoFichiers["TestsSampleXKG/PubAutCites_bi_XP9.nri"] = "pubautcites"

    dicoFichiers["Graphes_attribués_NRI/acl_XP1_aut_pub.nri"] = "coauteurs"
    dicoFichiers["Graphes_attribués_NRI/acl_XP2_aut_cit.nri"] = "citations"
    dicoFichiers["Graphes_attribués_NRI/acl_XP3_pub_aut.nri"] = "copublications"
    dicoFichiers["Graphes_attribués_NRI/acl_XP4_pub_cit.nri"] = "citationsp"
    dicoFichiers["Graphes_attribués_NRI/acl_XP5_conc_pub.nri"] = "cooccurrences"
    dicoFichiers["Graphes_attribués_NRI/acl_XP6_conc_cit.nri"] = "citationse"
    dicoFichiers["Graphes_attribués_NRI/acl_XP7_bi_pub_aut.nri"] = "pubaut"
    dicoFichiers["Graphes_attribués_NRI/acl_XP8_bi_aut_citpub.nri"] = "autpubcitees"
    dicoFichiers["Graphes_attribués_NRI/acl_XP9_bi_pub_citaut.nri"] = "pubautcites"

    #conversion des fichiers vers la destination
    ConvertMultipleNRIToRDF(dicoFichiers, "ACLtoRDF/AClNRIs.ttl", graphe)
    fin = time.time()
    print(fin - deb)
    print("----------")