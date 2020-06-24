from Extractors import *
#en faisant importFromJSON à la place de importFromJSONstruct, les dico ne contiennent pas d'uri, juste ds chaines de caractère
AuthorToID = ImportFromJSON("JSON_struct/AuthorToID.json")
PaperToID = ImportFromJSON("JSON_struct/PaperToID.json")
FieldToID = ImportFromJSON("JSON_struct/FieldToID.json")
IDToPaper = ImportFromJSON("JSON_struct/IDToPaper.json")
print(ace)
print(type(ace))
x = ace + "119"
print(x)
print(type(x))

def AjouterTriplet(graphe, sujet, predicat, objet) :
    """
    Ajoute à un graphe un triplet avec les sujet predicats et objets mis en paramètres
    graphe est un objet graphe de rdflib, sujet et prédicat sont des objet URIRef et objet peut-être un objet URIef ou un objet Literal xsd.string/xsd.date
    """
    graphe.add((sujet, predicat, objet))

def AnalyserSommet(chaine) :
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
        elif len(tab[1]) == 4 :
            #dans le cas des graphes bipartis pour les années c'est possible
            prefixe = tab[1]
        else : 
            prefixe = "FALSE"
    else :
        prefixe = "FALSE"

    return prefixe

def ValeurSommet(chaine) :
    """
    Fonction qui va donner la valeur d'un sommet, si cest un auteur ou un concepte, ca donne son nom, si c'est une publication, ca donne son id.
    Prend en paramètres une chaine de caratères.
    Retourne la valeur du sommet (nom ou id) sous forme de str.
    """

    tab = chaine.split("_")
    chaine = ""
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
    return chaine

def AnalyserSommets(graphe, sommets):
    """
    Fonction qui analyse les sommets (objets) d'un dictionnaire NRI et les ajoutes au graphe.
    Prend en paramètre un tableaux NRI["Objets"] ou NRI["Sommets"] et un graphe rdflib.
    la fonction doit prendre en compte le préfixe des sommets pour ajouter les bonnes infos du graphe, 
    en fonction des sommets il peut aussi ajouter des noms/titre (dico JSON).
    Pour ajouter les bons id, il faut soit aller chercher dans les dictionnaires JSON.
    Cette fonction est spécifiques aux 9 graphes de recherche d'experts
    """
    global AuthorToID
    global FieldToID
    global IDToPaper
    global ace
    #dans ces 3 dicos il n'y a que des chaines de caractères

    for sommet in sommets :
        pref = AnalyserSommet(sommet)
        if pref == "AUTH" : #cest un auteur, il et on a son nom avec 
            nom = ValeurSommet(sommet)
            id = AuthorToID[nom]
            AjouterTriplet(graphe, URIRef(id), RDF.type, ace.Author)
            AjouterTriplet(graphe, URIRef(id), ace.author_name, Literal(nom, datatype=XSD.string))
        elif pref == "CONC":
            nom = ValeurSommet(sommet)
            id = FieldToID[nom]
            AjouterTriplet(graphe, URIRef(id), RDF.type, ace.Field)
            #pour l'instant on ajoute pas fieldname
            #AjouterTriplet(graphe, URIRef(id), ace.field_name, Literal(nom, datatype=XSD.string))
        elif pref == "PAPE" :
            id = ace + ValeurSommet(sommet)
            nom = IDToPaper[id]
            AjouterTriplet(graphe, URIRef(id), RDF.type, ace.Paper)
            AjouterTriplet(graphe, URIRef(id), ace.paper_title, Literal(nom, datatype=XSD.string))
        else :
            #ca veut dire que le sommet est une année, rappel : cette function est utilisé pour le tableau "Objets" mais aussi "Items" qui contient des année, celle ci ne necessite pas de traitement préalable
            print("cest une année ?")
            print(sommet)

def AnalyserElements(graphe, NRI) :
    """
    Fonctions qui analyse et ajoute les élements du tableau des objets et des items dans le graphe.
    Prend en paramètres un graphe rdflib et un dictionnaire NRI.
    Analyse et ajoute les différents élément des liste dans le graphe
    """
    print(NRI["Objets"])
    AnalyserSommets(graphe, NRI["Objets"])
    AnalyserSommets(graphe, NRI["Items"])


def AnalyserItemsets(graphe, NRI):
    """
    Fonction analyse un itemsets, trouve les sujets et en fonction de leurs relations avec les objets ajoute au graphe rdf les triplets
    Prend en paramètre un graphe rdflib et un dictionnaire NRI
    Analyse les éléments et relations de l'itemsets et ajoute les triplets au graphe
    """
    #on pourra opti le id/nom dans les if avec un truc genre valeur et en fonction des if ca sera un id/nom/année 
    global AuthorToID
    global FieldToID
    global IDToPaper
    global ace
    dico = NRI["Itemsets"]
    items = dico.items()
    for sommet, valeurs in items :
        #dans le dico itemsets il n'y a que des index pointant vers des elements de Objets ou Items (clé=>Objets Valeurs=>Items)
        sujet = NRI["Objets"][sommet]
        prefixeS = AnalyserSommet(sujet)
        for valeur in valeurs :
            objet = NRI["Items"][valeur]
            prefixeO = AnalyserSommet(objet)
            if prefixeS == "PAPE":#si c'est une publication :
                idS = ace + ValeurSommet(sujet)
                nomS = IDToPaper[idS]
                if prefixeO == "AUTH" :
                    nomO = ValeurSommet(objet)
                    idO = AuthorToID[nomO]
                    AjouterTriplet(graphe, URIRef(idS), ace.paper_is_written_by, URIRef(idO))
                elif prefixeO == "Year" :
                    annee = ValeurSommet(objet)
                    AjouterTriplet(graphe, URIRef(idS), ace.paper_publish_date, Literal(annee, datatype=XSD.date))
                elif prefixeO == "CONC" :
                    nomO = ValeurSommet(objet)
                    idO = FieldToID[nomO]
                    AjouterTriplet(graphe, URIRef(idS), ace.paper_is_in_field, URIRef(idO))
                else :
                    #dans les itemsets des graphes de recherches peut pas y avoir autre chose que des auteurs, des thématiques ou des années
                    print("problème dans l'itemsets")
                    print("objet : " + str(objet))
                    print("sujet : " + str(sujet))
            elif prefixeS == "AUTH":
                nomS = ValeurSommet(sujet)
                idS = AuthorToID[nomS]
                if prefixeO == "CONC":
                    #ca la seule propriété utilisable pour un itemsets d'un auteur : author_is_in_field
                    #c'est pas encore valider de le mettre donc on ecrit mais faudra peut etre l'
                    nomO = ValeurSommet(objet)
                    idO = FieldToID[nomO]
                    AjouterTriplet(graphe, URIRef(idS), ace.author_is_in_field, URIRef(idO))
                else : 
                    print("objet : " + str(objet) + " pas de propriété exploitable pour un auteur")
            elif prefixeS == "CONC" :
                nomS = ValeurSommet(sujet)
                idS = FieldToID[nomS]
                if prefixeO == "AUTH":
                    #c'est une relation entre un field et un auteur on peut ajouter un triplet avec author is in field faut juste inverser sujet et objet
                    #cette propriété n'est pas encore validé faudra peut-etre enlever
                    nomO = ValeurSommet(objet)
                    idO = AuthorToID[nomO]
                    AjouterTriplet(graphe, URIRef(idO), ace.author_is_in_field, URIRef(idS))
                else : 
                    print("objet : " + str(objet) + " pas de propriété exploitable pour un domaine")
            else :
                print("problème itemsets, sujet suspect")
                print("objet : " + str(objet))
                print("sujet : " + str(sujet))

def AnalyserGraphe(graphe, NRI, relation):
    """
    Fonction analyse un graphe en fonction de sa relation, trouve les sujets et en fonction de leurs relations avec les autres sommets ajoute au graphe rdf les triplets
    Prend en paramètre un graphe rdflib, un dictionnaire NRIn une relation (str)
    Analyse les éléments et relations du graphe et ajoute les triplets au graphe rdf
    """
    relation = relation.lower() #on met en minuscule car on veut pas de problèmes liées au maj
    global AuthorToID
    global ace
    dico = NRI["Graphe"]
    items = dico.items()
    if relation == "citationsp" : 
        for sommet, valeurs in items :
            sujet = NRI["Objets"][sommet]
            prefixeS = AnalyserSommet(sujet)
            for valeur in valeurs :
                objet = NRI["Objets"][valeur]
                prefixeO = AnalyserSommet(objet)
                if prefixeS == "PAPE" and prefixeO == "PAPE":
                    idS = ace + ValeurSommet(sujet)
                    idO = ace + ValeurSommet(objet)
                    AjouterTriplet(graphe, URIRef(idS), ace.paper_cit_paper, URIRef(idO))
                else :
                    print("incohérence sommets et relation")
                    print("relation : " + relation + " | sommets : " + str(sujet) + "/" + str(objet))

    elif relation == "pubaut" : 
        for sommet, valeurs in items :
            sujet = NRI["Objets"][sommet]
            prefixeS = AnalyserSommet(sujet)
            if prefixeS == "PAPE" : 
                for valeur in valeurs :
                    objet = NRI["Objets"][valeur]
                    prefixeO = AnalyserSommet(objet)
                    if prefixeO == "AUTH":
                        idS = ace + ValeurSommet(sujet)
                        nomO = ValeurSommet(objet)
                        idO = AuthorToID[nomO]
                        AjouterTriplet(graphe, URIRef(idS), ace.paper_is_written_by, URIRef(idO))
                    else :
                        print("incohérence sommets et relation")
                        print("relation : " + relation + " | sommets : " + str(sujet) + "/" + str(objet))
            elif prefixeS == "AUTH":
                print("je fais des economies")
            else :
                print("incohérence sommet et relation")
                print("relation : " + relation + " | sommet : " + str(sujet))

    elif relation == "coauteurs" or relation == "citation" or relation == "copublication" or relation == "cooccurrences" or relation == "citatione" or relation == "autpubcitees" or relation == "pubautcites" :
        print("aucune propriété aceKG n'est extrayable de ce graphe")
    else :
        print("erreur relation : veuillez verifier l'ortographe")

def AnalyserNRI(graphe, NRI, relation):
    """
    Fonction qui analyse un dictionnaire NRI et ajoute tous les triplets necessaire au grgaphe rdflib
    prend en paramètre un graphe rdflib, un dictionnaire NRI, et la relation que représente le dictionnaire NRI
    """
    AnalyserElements(graphe, NRI)
    AnalyserItemsets(graphe, NRI)
    AnalyserGraphe(graphe, NRI, relation)