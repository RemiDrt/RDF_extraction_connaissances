from Extractors import *

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

def AnalyserSommets(graphe, NRI):
    """
    Fonction qui analyse les sommets (objets) d'un dictionnaire NRI et les ajoutes au graphe.
    Prend en paramètre un dictionnaire NRI et un graphe rdflib.
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
    sommets = NRI["Objets"]
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
            AjouterTriplet(graphe, URIRef(id), ace.field_name, Literal(nom, datatype=XSD.string))
        elif pref == "PAPE" :
            id = ace + ValeurSommet(sommet)
            nom = IDToPaper[id]
            AjouterTriplet(graphe, URIRef(id), RDF.type, ace.Paper)
            AjouterTriplet(graphe, URIRef(id), ace.paper_title, Literal(nom, datatype=XSD.string))
        else :
            #ca veut dire que le sommet est une année, rappel : cette function est utilisé pour le tableau "Objets" mais aussi "Items" qui contient des année, celle ci ne necessite pas de traitement préalable
            print("cest une année ?")
            print(sommet)



