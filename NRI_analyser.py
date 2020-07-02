from Extractors import *
from Utilities import *
from rdflib import XSD, Literal
#si on a un nom sans un id il faudra attribuer a in a l'element et pour ne pas attribuer 2 fois un id il faut garder le compte des tous les ID
IDs = [] #ensemble des id attribués venant directement des dico NRI
ID = 0 #valeur du prochain id attribué
ElementToID = {}#dictionnaire associant un element à son id
#quon on va ajouter au graphe un element avec elementID type Element, on va aussi l'ajouter a ce tableau pour par la suite dnas l'analyse du graphe et de l'itemsets
#pouvoir retrouver l'id des elements


def AjouterTriplet(graphe, sujet, predicat, objet) :#fonction général
    """
    Ajoute à un graphe un triplet avec les sujet predicats et objets mis en paramètres
    graphe est un objet graphe de rdflib, sujet et prédicat sont des objet URIRef et objet peut-être un objet URIef ou un objet Literal xsd.string/xsd.date
    """
    graphe.add((sujet, predicat, objet))

def AnalyserSommet(chaine) :#spécifique
    """
    Fonction qui donne la nature d'un sommet grâce à son préfixe.
    Prend en paramètres une chaine de caractères.
    Retourne le préfixe de la chaine (c'est lui qui donne la nature du sommet) retourne la valeure "FALSE" s'il y a une incohérence
    """
    tab = chaine.split("_")
    if len(tab) > 1 :
        if len(tab[0]) == 4 :
            #on est sur le préfixe
            prefixe = tab[0]
        elif len(tab[1]) == 4 :#sinon cest surement le cas A_Year ou p_Year donc on s'interesse à "Year"
            #dans le cas des graphes bipartis pour les années c'est possible
            prefixe = tab[1]
        else : #sinon pas de cas connu
            prefixe = "FALSE"
    else : #si cest une publication acl cest de type A00-0000 donc on peut essayer de separer avec un "-" et de faire les memes verifs
        tab = tab[0].split("-")
        if len(tab) > 1 :
            if len(tab[0]) == 3 :#c'est surement ACL
                prefixe = "PAPE"#on met PAPE pour faciliter la suite 
        else :
            prefixe = "FALSE"

    return prefixe

def ValeurSommet(chaine) :#spécifique
    """
    Fonction qui va donner la valeur d'un sommet, ca peut etre un nom ou un id.
    Prend en paramètres une chaine de caratères.
    Retourne la valeur du sommet (nom ou id) sous forme de str.
    """

    tab = chaine.split("_")
    chaine = ""
    if len(tab) > 1 :
        if len(tab[0]) == 4 :
            #schéma classique il faut jsute retourer la suite du tableau sans le préfixe et avec des espaces
            i = 1
            n = len(tab)
            while i < n :
                if i == 1:
                    chaine += tab[i]
                else:
                    chaine += " " + tab[i]
                i += 1
        elif len(tab[1]) == 4 :
            #schéma graphe biparti pour les années
            chaine = tab[2] 
        else :
            chaine = "FALSE"
    else :#cas ACL peut etre
        tab = tab[0].split("-")
        if len(tab) > 1 :
            if len(tab[0]) == 3 :#c'est surement ACL
                chaine = tab[0]+tab[1]
            else :
                chaine = "FALSE"
        else :
            chaine = "FALSE"

    return chaine

def AnalyserSommets(graphe, sommets, IDToAuthor=None, IDToField=None, IDToPaper=None, AuthorToID=None, FieldToID=None):#spécifique
    """
    Fonction qui analyse les sommets (objets) d'un dictionnaire NRI et les ajoutes au graphe.
    Prend en paramètre un tableaux NRI["Objets"] ou NRI["Sommets"] et un graphe rdflib, on peut ajouter si on en dispose des dictionnaire associant des id a des noms (!! attention les clés doivent etre des str pas des uri !!).
    la fonction doit prendre en compte le préfixe des sommets pour ajouter les bonnes infos du graphe, 
    en fonction des sommets il peut aussi ajouter des noms/titre (dico JSON).
    Pour ajouter les bons id, il faut soit aller chercher dans les dictionnaires JSON soit attribuer des id en faisant attention a ne pas attribuer 2 fois le même.
    Cette fonction est spécifiques aux 9 graphes de recherche d'experts venant de ACE et de ACL
    """
    global ace
    global IDs
    global ID
    global ElementToID

    for sommet in sommets :
        pref = AnalyserSommet(sommet)
        if pref == "AUTH" : #cest un auteur 
            vSom = ValeurSommet(sommet)
            if isID(vSom) :
                IDs.append(vSom)
                id = ace + vSom
                if IDToAuthor :#si on a un tableau qui peut nous donner un nom on utilise le nom
                    nom = IDToAuthor[id]
                    AjouterTriplet(graphe, URIRef(id), ace.author_name, Literal(nom, datatype=XSD.string))
            else :
                nom = vSom
                if AuthorToID :#si on a un tableau qui peut nous donner un id on utilise l'id de celui ci
                    id = AuthorToID[vSom]
                else :#sinon on utilise notre variable global
                    while str(ID) in IDs :
                        ID += 1
                    id = ace + str(ID)
                    ID += 1
                AjouterTriplet(graphe, URIRef(id), ace.author_name, Literal(nom, datatype=XSD.string))

            AjouterTriplet(graphe, URIRef(id), RDF.type, ace.Author)#on ajoute l'element avec son id
            ElementToID[vSom] = id
            
        elif pref == "CONC":
            vSom = ValeurSommet(sommet)
            if isID(vSom) :
                IDs.append(vSom)
                id = ace + vSom
                if IDToField :
                    nom = IDToField[id]
                    AjouterTriplet(graphe, URIRef(id), ace.field_name, Literal(nom, datatype=XSD.string))
            else :
                nom = vSom
                if FieldToID :
                    id = FieldToID[nom]
                else :
                    while str(ID) in IDs :
                        ID += 1
                    id = ace + str(ID)
                    ID += 1
                AjouterTriplet(graphe, URIRef(id), ace.field_name, Literal(nom, datatype=XSD.string))

            AjouterTriplet(graphe, URIRef(id), RDF.type, ace.Field)
            ElementToID[vSom] = id

        elif pref == "PAPE" :#quoi qu'il arrive ca sera un ID : j'ai codé pour faire en sorte que les PAPE qui viennent d'ace soient des ID et ceux qui viennent de acl sont des id
            vSom = ValeurSommet(sommet)
            IDs.append(vSom)
            id = ace + vSom
            if IDToPaper :
                nom = IDToPaper[id]
                AjouterTriplet(graphe, URIRef(id), ace.paper_title, Literal(nom, datatype=XSD.string))

            AjouterTriplet(graphe, URIRef(id), RDF.type, ace.Paper)
            ElementToID[vSom] = id

        elif pref == "FALSE" :
            #ca veut dire qu'il y a eu une erreur
            print("Erreur sommet inconnu, on ne le traitra pas : " + str(sommet))

def AnalyserElements(graphe, NRI, IDToAuthor=None, IDToField=None, IDToPaper=None, AuthorToID=None, FieldToID=None) :#spécifique car utilise des fonctions spécifiques
    """
    Fonctions qui analyse et ajoute les élements du tableau des objets et des items dans le graphe.
    Prend en paramètres un graphe rdflib un dictionnaire NRI et les dictionnaires intermediaires si besoin.
    Analyse et ajoute les différents élément des liste dans le graphe
    """
    AnalyserSommets(graphe, NRI["Objets"], IDToAuthor=IDToAuthor, IDToField=IDToField, IDToPaper=IDToPaper, AuthorToID=AuthorToID, FieldToID=FieldToID)
    AnalyserSommets(graphe, NRI["Items"], IDToAuthor=IDToAuthor, IDToField=IDToField, IDToPaper=IDToPaper, AuthorToID=AuthorToID, FieldToID=FieldToID)


def AnalyserItemsets(graphe, NRI):#spécifique
    """
    Fonction analyse un itemsets, trouve les sujets et en fonction de leurs relations avec les objets ajoute au graphe rdf les triplets
    Prend en paramètre un graphe rdflib et un dictionnaire NRI
    Analyse les éléments et relations de l'itemsets et ajoute les triplets au graphe
    """
    global ace
    global ElementToID

    dico = NRI["Itemsets"]
    items = dico.items()
    for sommet, valeurs in items :
        #dans le dico itemsets il n'y a que des index pointant vers des elements de Objets ou Items (clé=>Objets Valeurs=>Items), il faut juste convertir l'index en int
        sujet = NRI["Objets"][int(sommet)]
        prefixeS = AnalyserSommet(sujet)
        for valeur in valeurs :
            objet = NRI["Items"][int(valeur)]
            prefixeO = AnalyserSommet(objet)
            if prefixeS == "PAPE":#si c'est une publication :
                idS = ElementToID[ValeurSommet(sujet)]
                if prefixeO == "AUTH" :
                    idO = ElementToID[ValeurSommet(objet)]
                    AjouterTriplet(graphe, URIRef(idS), ace.paper_is_written_by, URIRef(idO))
                elif prefixeO == "Year" :
                    annee = ValeurSommet(objet)
                    AjouterTriplet(graphe, URIRef(idS), ace.paper_publish_date, Literal(annee, datatype=XSD.date))
                elif prefixeO == "CONC" :
                    idO = ElementToID[ValeurSommet(objet)]
                    AjouterTriplet(graphe, URIRef(idS), ace.paper_is_in_field, URIRef(idO))
                else :
                    #dans les itemsets des graphes de recherches peut pas y avoir autre chose que des auteurs, des thématiques ou des années
                    print("problème dans l'itemsets")
                    print("objet : " + str(objet))
                    print("sujet : " + str(sujet))
            elif prefixeS == "AUTH":
                idS = ElementToID[ValeurSommet(sujet)]
                if prefixeO == "CONC":
                    #c'est la seule propriété utilisable pour un itemsets d'un auteur : author_is_in_field
                    #c'est pas encore valider de le mettre donc on ecrit mais faudra peut etre l'enlever
                    idO = ElementToID[ValeurSommet(objet)]
                    AjouterTriplet(graphe, URIRef(idS), ace.author_is_in_field, URIRef(idO))
                else : 
                    print("objet : " + str(objet) + " pas de propriété exploitable pour un auteur")
            elif prefixeS == "CONC" :
                idS = ElementToID[ValeurSommet(sujet)]
                if prefixeO == "AUTH":
                    #c'est une relation entre un field et un auteur on peut ajouter un triplet avec author is in field faut juste inverser sujet et objet
                    #cette propriété n'est pas encore validé faudra peut-etre enlever
                    idO = ElementToID[ValeurSommet(objet)]
                    AjouterTriplet(graphe, URIRef(idO), ace.author_is_in_field, URIRef(idS))
                else : 
                    print("objet : " + str(objet) + " pas de propriété exploitable pour un domaine")
            else :
                print("problème itemsets, sujet suspect")
                print("objet : " + str(objet))
                print("sujet : " + str(sujet))

def AnalyserGraphe(graphe, NRI, relation):#spécifique
    """
    Fonction analyse un graphe en fonction de sa relation, trouve les sujets et en fonction de leurs relations avec les autres sommets ajoute au graphe rdf les triplets
    Prend en paramètre un graphe rdflib, un dictionnaire NRIn une relation (str)
    Analyse les éléments et relations du graphe et ajoute les triplets au graphe rdf
    """
    global ace
    global ElementToID

    relation = relation.lower() #on met en minuscule car on veut pas de problèmes liées au maj
    dico = NRI["Graphe"]
    items = dico.items()
    if relation == "citationsp" : 
        for sommet, valeurs in items :
            sujet = NRI["Objets"][int(sommet)]
            prefixeS = AnalyserSommet(sujet)
            for valeur in valeurs :
                objet = NRI["Objets"][int(valeur)]
                prefixeO = AnalyserSommet(objet)
                if prefixeS == "PAPE" and prefixeO == "PAPE":
                    idS = ElementToID[ValeurSommet(sujet)]
                    idO = ElementToID[ValeurSommet(objet)]
                    AjouterTriplet(graphe, URIRef(idS), ace.paper_cit_paper, URIRef(idO))
                else :
                    print("incohérence sommets et relation")
                    print("relation : " + relation + " | sommets : " + str(sujet) + "/" + str(objet))

    elif relation == "pubaut" : 
        for sommet, valeurs in items :
            sujet = NRI["Objets"][int(sommet)]
            prefixeS = AnalyserSommet(sujet)
            if prefixeS == "PAPE" : 
                for valeur in valeurs :
                    objet = NRI["Objets"][int(valeur)]
                    prefixeO = AnalyserSommet(objet)
                    if prefixeO == "AUTH":
                        idS = ElementToID[ValeurSommet(sujet)]
                        idO = ElementToID[ValeurSommet(objet)]
                        AjouterTriplet(graphe, URIRef(idS), ace.paper_is_written_by, URIRef(idO))
                    else :
                        print("incohérence sommets et relation")
                        print("relation : " + relation + " | sommets : " + str(sujet) + "/" + str(objet))
            elif prefixeS == "FALSE" or prefixeS == "Year" or prefixeS == "CONC":
                print("incohérence sommet et relation")
                print("relation : " + relation + " | sommet : " + str(sujet))

    elif relation == "coauteurs" or relation == "citations" or relation == "copublications" or relation == "cooccurrences" or relation == "citationse" or relation == "autpubcitees" or relation == "pubautcites" :
        print("aucune propriété aceKG n'est extrayable de ce graphe : " + relation)
    else :
        print("erreur relation inconnue : veuillez verifier l'ortographe")

def AnalyserNRI(graphe, NRI, relation, IDToAuthor=None, IDToField=None, IDToPaper=None, AuthorToID=None, FieldToID=None) :#spécifique car utilise des fonctions spécifiques
    """
    Fonction qui analyse un dictionnaire NRI et ajoute tous les triplets necessaire au grgaphe rdflib
    prend en paramètre un graphe rdflib, un dictionnaire NRI, et la relation que représente le dictionnaire NRI
    """
    AnalyserElements(graphe, NRI, IDToAuthor=IDToAuthor, IDToField=IDToField, IDToPaper=IDToPaper, AuthorToID=AuthorToID, FieldToID=FieldToID)
    AnalyserItemsets(graphe, NRI)
    AnalyserGraphe(graphe, NRI, relation)