#librairi de fonction utiles diverses et variées
import json
import re
from rdflib import URIRef

def ExportToJSON(dictionnaire, file) :
    """
    Fonction qui exporte un dictionnaire dans un fichier JSON.
    Prend en paramètres le dictionnaire et le fichier/son chemin si on veut le mettre dans un endroit en particulier.
    On pourrait utiliser cette fonction avec n'importe quelle structure supportée par le module json de python, lais de base on l'utilisera pour des dictionnaire.
    """
    with open(file, "w", encoding = "utf-8") as JSON_File :
        json.dump(dictionnaire, JSON_File, indent=2)


def ImportFromJSON(file) :
    """
    Fonction qui importe un objet d'un fichier JSON, pour voir les différents types possible à importer, se référer a la doc json de python
    prend en paramètres un fichier/son chemon
    retourne l'objet importé (de préférence un dictionnaire)
    """
    with open(file, encoding="utf-8") as JSON_File :
        objet = json.load(JSON_File)
    return objet


def TabURI(tabs) :
    """
    Corrige un tableau d'URI a partir d'un tableau qui à été importé de JSON, change ces string en objets URIRef
    prend en paramètre la liste de string
    Retourne un liste d'URIRefs
    """
    tableau = []
    for author in tabs :
        tableau.append(URIRef(author))
    return tableau


def SimpleDictURI(dico_JSON) :
    """
    Fonction qui change les String d'un dictionnaire en URIRef
    prend en paramètre un dictionnaire
    Retourne un dictionnaire avec les clé changé en URIRef et les valeurs changés en URIRefs
    """
    dico = {}
    items = dico_JSON.items()
    for key, val in items :
        dico[URIRef(key)] = URIRef(val)
    return dico


def ComplexDictURI(dico_JSON):
    """
    Fonction qui change les String d'un dictionnaire en URIRef
    prend en paramètre un dictionnaire
    Retourne un dictionnaire avec les clé changé en URIRef et les tableaux changés en URIRefs
    """
    dico = {}
    items = dico_JSON.items()
    for key, vals in items :
        tab = []
        for val in vals :
            tab.append(URIRef(val))
        dico[URIRef(key)] = tab
    return dico


def IsURI(texte):#dossier utilitaire
    """
    Fonction pour repérer si un texte est une URI dans nos talbeau (il doit commencer par http:)
    prend en paramètre la chaine de caractère 
    retourne True si cest une URI false sinon 
    """
    x = re.search("^https?", texte)
    if x :
        return True
    return False 


def ImportFromJSONStruc(file) :#dossier utilitaire
    """
    Fonction qui importe un objet JSON d'un fichier et le corrige le changement de type avec les URI
    Si la structure devait contenir des uri qui sont devenu des str, elles seront changés (ne change pas les year et les literal xsd.string car ce n'est pas utilisés comme des clés par la suite)
    retourne la structure json (dictionnaire ou liste) avec des objets urirefs s'il y en avait avant l'export
    """
    objet = ImportFromJSON(file)
    if isinstance(objet, list) :
        objet = TabURI(objet)
    else :
        items = objet.items()
        objet = dict()
        for key, vals in items :
            valeur = vals
            if IsURI(key) :
                cle = URIRef(key)
            else :
                cle = key
            if isinstance(vals, list) :
                if len(vals) > 0 and IsURI(vals[0]) :
                    valeur = TabURI(vals)
            else :
                if IsURI(vals) :
                    valeur = URIRef(vals)
            objet[cle] = valeur
    return objet



def InverserDicoSimple(file):#dossier utilitaire ? vraiment besoin ???
    """
    Fonction qui inverse les clé et les valeurs d'un dictionnaire.
    Prend le dictionnaire importé dans le fichier en paramètre et inverse les clés et les valeurs
    Retourne un dictionnaire (utilisé pour associé les noms avec les id, les clés deviennent les noms)
    """
    dicoS = ImportFromJSON(file)
    items = dicoS.items()
    dicoR = dict()
    for cle, val in items :
        dicoR[val] = cle
    return dicoR



def AjouterPrefixe(prefixe, chaine) : #dossier utilitaire ?
    """
    Fonction qui ajoute un préfixe à une chaine de caractère et remplace les " " par des "_"
    retourne une chaine de caractères avec le préfixe placé devant
    exemple : AjouterPrefixe("AUTH", "Albert Einstein") retourne "AUTH_Albert_Einstein"
    """
    pref = prefixe + "_"
    new_chaine = pref + chaine.replace(" ", "_")
    return new_chaine


def AjouterPrefixes(prefixe, liste) : #dossier utilitaire ?
    """
    Fonction qui ajouter un prefixe à chaque elements d'un liste de str (remplace les " " par des "_").
    Prend en paramètre un préfixe et une liste
    modifie chaque élements de la liste
    """
    i = 0
    lgListe = len(liste)
    while i < lgListe :
        liste[i] = AjouterPrefixe(prefixe, liste[i])
        i += 1


def YearFromDate(date) :
    """
    Extrait l'année d'un date qui est au format xsd.date (YYYY-MM-DD)
    Retourne la chaine de caractère correspondant à l'année de la date
    """
    return date[:4]

def ListerAnnees(dictionnaire) :#dossier utilitaire  ou creer nri ??
    """
    Fonction qui permet d'extraire les années associés à des sommets sans répétitions
    prend en paramètre un dictionnaire associatifs type { sommet : année/[année, ..], sommet :}
    retourne un liste de toutes les années des sommets sans répetition
    """
    attributs = []
    for key in dictionnaire.keys() :
        #si l'attributs n'est pas sous forme de list
        if not isinstance(dictionnaire[key], list) :
            annee = YearFromDate(dictionnaire[key])
            #s'il est pas déjà dans le tableau :
            if not annee in attributs :
                attributs.append(annee)
        else :
            for date in dictionnaire[key] :
                annee = YearFromDate(date)
                if not annee in attributs : 
                    attributs.append(annee)

    return attributs

def ListerAttributs(dictionnaire):#dossier utilitiare ?
    """
    Fonction qui permet d'extraire les attributs associés à des sommets sans répétitions
    prend en paramètre un dictionnaire associatifs type { sommet : attribut/[attribut, ..], sommet :}
    retourne un liste de tous les attributs des sommets sans répetition
    """
    attributs = []
    for key in dictionnaire.keys() :
        #si l'attributs n'est pas sous forme de list
        if not isinstance(dictionnaire[key], list) :
            #s'il est pas déjà dans le tableau :
            if not dictionnaire[key] in attributs :
                attributs.append(dictionnaire[key])
        else :
            for attribut in dictionnaire[key] :
                if not attribut in attributs : 
                    attributs.append(attribut)

    return attributs


def IndexerElements(index, listeElements) : #dossier utilitaire ?
    """
    Fonction qui répertorie/associe l'index d'un élement d'une liste dans un dictionnaire.
    Prend en paremètres le dictionnaire qui répertorie les index et une liste d'élements.
    Ajouter les index des éléments de la liste au dictionnaire des index
    """
    i = 0
    lgListe = len(listeElements)
    while i < lgListe :
        index[listeElements[i]] = i 
        i += 1


def IDFromURI(URI) :
    """
    Extrait l'id de l'uri d'un element
    prend en paramètre l'uri
    retourne l'id de l'uri (le numéro de fin) sous forme de str
    exemple IDFromURI("http://www.semanticweb.org/acemap#001")=>001
    """
    return URI.split("#")[1]


def ListerID(listeID) : 
    """
    Crée un liste avec seulement l'id de l'URI pour chaque URI de la liste
    prend en paramètres une liste
    retourne une liste de numéros ID
    """
    liste = []
    for element in listeID :
        liste.append(IDFromURI(element))
    return liste


def ListerNoms(listeID, dico) : 
    """
    Crée un liste de nom à partir d'une liste d'id et d'un dictionnaire associant ID et nom
    prend en paramètres un liste d'ID et le dictionnaire associatif
    retourne une liste de nom qui sont dans le même ordre que les ID (le nom 1 correspond à l'ID 1 etcetc)
    """
    listeNom = []
    i = 0
    lgListe = len(listeID)
    while i < lgListe :
        listeNom.append(dico[listeID[i]])
        i += 1
    return listeNom


def Union(lst1, lst2) :
    """
    Fait l'union entre 2 liste (union mathématique U).
    Prend en paramètres 2 listes.
    Retourne l'union des 2 listes dans un liste
    exemple : Union([a, b], [b, c]) = [a, b, c]
    """
    lst = list(set(lst1) | set(lst2))
    return lst