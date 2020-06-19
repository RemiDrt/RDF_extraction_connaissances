#!/usr/bin/python
#coding=utf-8
import json
import re
from rdflib import Graph, RDF, URIRef, Literal
from rdflib.namespace import XSD , FOAF, Namespace

ace = Namespace("http://www.semanticweb.org/acemap#")

def Sommets(texte) :
    """
    Fonction qui donne les sommets listés d'un fichier NRI
    Prend en paramètre la liste des lignes du fichier (créée avec readlines())
    Retourne un tableau des sommets
    """
    return texte[1].split("|")

def Attributs(texte) :
    """
    Fonction qui donne les attributs listés d'un fichier NRI
    Prend en paramètre la liste des lignes du fichier (créée avec readlines())
    Retourne un tableau des attributs
    """
    return texte[2].split("|")

def Itemsets(texte) :
    """
    Fonction qui donne l'itemsets d'un fichier NRI
    Prend en paramètre la liste des lignes du fichier (créée avec readlines())
    Retourne un tableau associatif/dictionnaire des sommet->attributs
    {sommet : [attribut, .., attribut], sommet : ...}
    """
    itemsets = dict()
    #on commence a la 4eme ligne
    i = 3
    # le diese marque la fin de l'itemsets dans le fichier mais comme il y peut-être un espace on vérifie le premier carac de la ligne
    while texte[i][0] != "#" :
        tab1 = texte[i].split() #on sépare avec l'espace pour avoir d'un coté le numéros de sommet et de l'autre les numéros d'attributs
        nSommet = int(tab1[0])
        if len(tab1) > 1 : #attention aussi si on se retrouve avec un sommet sans attribut la case tab[1] n'existe pas faudra la vérifier
            listAttributs = tab1[1].split(",") #attention listAttribut est un liste de numéros mais ce sont des String
        else :
            listAttributs = [] #un tableau vide
        itemsets[nSommet] = listAttributs
        i += 1
    return itemsets


def Graphe(texte) :
    """
    Fonction qui donne le graphe d'un fichier NRI
    Prend en paramètre la liste des lignes du fichier (créée avec readlines())
    Retourne un tableau associatif/dictionnaire des sommet->sommets liés
    Pas besoin de représenter les liaisons qui n'y sont pas donc c'est la même forme que l'itemsets
    {sommet : [sommet, .., sommet], sommet : ...}
    """
    #pour connaitre la ligne du début : c'est après le #
    #ligne 1 est un commentaire
    #ligne 2 : liste des sommets
    #ligne 3 : liste des Attributs
    #ligne 4 : début de l'itemsets, liste des attributs de chaque sommets
    #ligne <nb de sommet + 3> : le #
    #ligne <nb de sommet + 4> : le début du graphe
    graph = dict()
    nbSommets = len(Sommets(texte))
    lgDebGraphe = nbSommets + 4
    #on peut aussi calculer le nb total de ligne : 2*nbSommets + 4
    #on parcours 2 fois tous les sommets (pour le graphe et l'itemsets) et on ajoute la ligne # et les 3 lignes du débuts
    nbTot = (2 * nbSommets) + 4
    i = lgDebGraphe
    while i < nbTot:
        tab1 = texte[i].split() #on sépare avec l'espace pour avoir d'un coté le numéro du sommet concerné et de l'autre les numéros des sommets liés
        nSommet = int(tab1[0])
        if len(tab1) > 1 : #attention aussi si on se retrouve avec un sommet sans lien la case tab[1] n'existe pas faudra la vérifier
            listliens = tab1[1].split(",") #attention listAttribut est un liste de numéros mais ce sont des String
        else :
            listliens = [] #un tableau vide
        graph[nSommet] = listliens
        i += 1
    return graph

def NRI(texte) :
    """
    Fonction qui créer un dictionnaire au format NRI à partir d'un fichier NRI
    Prend en paramètre la liste des lignes du fichier (créée avec readlines())
    Retourne un dictionnaire qui associe à chaque élément NRI ses données
    """
    nri = dict()
    sommets = Sommets(texte)
    attributs = Attributs(texte)
    itemsets = Itemsets(texte)
    graphe = Graphe(texte)
    nri["Graphe"] = graphe
    nri["Objets"] = sommets
    nri["Items"] = attributs
    nri["Itemsets"] = itemsets
    return nri

def AfficherNRI(dico):
    """
    """
    print(dico)


def getGrapheRDF(ttlFile) :
    """
    Crée et retourne un objet graphe de la librairi rdflib à partir d'un fichier turtle
    cet objet contient tout les triplets du fichier
    """
    graphe = Graph()
    graphe.parse(location=ttlFile, format="turtle")
    return graphe

def AfficherTriplets(graphe):
    """
    """
    for sujet, predicat, objet in graphe :
        print("\n")
        print(sujet)
        print(predicat)
        print(objet)
        print("\n---------------------")

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

def ListerAnnees(dictionnaire) :
    """
    Fonction qui permet d'extraire les années associés à des sommets sans répétitions
    prend en paramètre un dictionnaire associatifs type { sommet : année/[année, ..], sommet :}
    retourne un liste de toutes les années des sommets sans répetition
    """
    attributs = []
    for key in dictionnaire.keys() :
        #si l'attributs n'est pas sous forme de list
        if not isinstance(dictionnaire[key], list) :
            #s'il est pas déjà dans le tableau :
            annee = YearFromDate(dictionnaire[key])
            if not annee in attributs :
                attributs.append(annee)
        else :
            for date in dictionnaire[key] :
                annee = YearFromDate(date)
                if not annee in attributs : 
                    attributs.append(annee)

    return attributs




def TabURI(tabs):
    """
    Corrige un tableau d'URI qui à été importé de JSON, change ces string en objets URIRef
    prend en paramètre la liste de string
    Retourne un liste d'URIRefs
    """
    tableau = []
    for author in tabs :
        tableau.append(URIRef(author))
    return tableau

def SimpleDictURI(dico_JSON):
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

def IsURI(texte):
    """
    Fonction pour repérer si un texte est une URI dans nos talbeau (il doit commencer par http:)
    prend en paramètre la chaine de caractère 
    retourne True si cest une URI false sinon 
    """
    x = re.search("^https?", texte)
    if x :
        return True
    return False   

def ImportFromJSONStruc(file) :
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
                print(key)
                print("isURI")
                cle = URIRef(key)
            else :
                cle = key
                print(cle)
                print("not URI")
            if isinstance(vals, list) :
                if IsURI(vals[0]) :
                    valeur = TabURI(vals)
            else :
                if IsURI(vals) :
                    valeur = URIRef(vals)
            objet[cle] = valeur
    return objet

def ExtraireAuteurs(graphe) :
    """
    Extrait tous les id d'auteurs dans un tableau
    prends un paramètre un graphe de rdflib
    retourne un tableau avec tous les id des auteurs
    """
    auteurs = []
    authors = graphe.subjects(RDF.type, ace.Author)
    for author in authors :
        auteurs.append(author)
    return auteurs



def ExtrairePublications(graphe) :
    """
    Extrait tous les id de publication dans un tableau
    prends un paramètre un graphe de rdflib
    retourne un tableau avec tous les id des publications
    """
    publi = []
    papers = graphe.subjects(RDF.type, ace.Paper)
    for paper in papers :
        publi.append(paper)
    return publi


def ExtraireConceptes(graphe) :
    """
    Extrait tous les id de thématiques dans un talbeau
    prend en paramètres un graphe de rdflib
    retourne un tableau avec tous les id des thématiques/field/domaines/concepts (CONC)
    """
    them = []
    fields = graphe.subjects(RDF.type, ace.Field)
    for field in fields : 
        them.append(field)
    return them


def IDToAuthor(graphe, auteurs) :
    """
    Extrait les identifiants des auteurs et leurs noms présents dans acemap
    prend en paramètre un objet graphe de la RDFlib
    retourne une dictionnaire qui associe authorID à son nom
    """

    IDToAuthors = dict()
    for auteur in auteurs :
        noms = graphe.objects(auteur, ace.author_name)
        for nom in noms :
            IDToAuthors[auteur] = nom
    return IDToAuthors


def IDToField(graphe, conceptes) :
    """
    Extrait les nom des différents conceptes/domaines/field et les associes à leurs ID
    prend en parametre un gaphe rdflib et la liste des id des conceptes
    retourne un dictionnaire associant un fieldid a son nom
    """
    IDToField = dict()
    for concepte in conceptes :
        noms = graphe.objects(concepte, ace.field_name)
        for nom in noms : 
            IDToField[concepte] = nom
    return IDToField

def IDToPaper(graphe, publications) :
    """
    Extrait les titres des publications
    prend en paramètre un objet graphe de la RDFlib et la liste des publications
    retourne une dictionnaire qui associe paperID à son tite
    """

    IDToPaper = dict()
    for paper in publications :
        titres = graphe.objects(paper, ace.paper_title)
        for titre in titres :
            IDToPaper[paper] = titre
    return IDToPaper


def PaperToYear(graphe, publications) :
    """
    Extrait les années et les associe a leurs publications
    prend en paramètre un graphe rdflib et la liste des publication
    retourne un dicitonnaire associant publicationID à son année de publication (jespere qu'il en a qu'une seul)
    exemple : { paperID : year, paperID : year ....... }
    """
    PaperToYear = dict()
    for publication in publications :
        dates = graphe.objects(publication, ace.paper_publish_date)
        for date in dates :
            year = YearFromDate(date)
            PaperToYear[publication] = year
    return PaperToYear


def PaperToField(graphe, publications) :
    """
    Extrait les domaines des publications
    prend en paramètre un objet graphe de rdflib et un liste d'id de publication sous forme d'URI
    retourne un dictionnaire associant à un paperID tous les FieldID auxquelles il est rataché
    { paperID : [fieldID, fieldID, fieldID], paperID : [fieldID, ...] ... }
    """
    paperToField = dict()
    for publication in publications :
        domaines = graphe.objects(publication, ace.paper_is_in_field)
        paperToField[publication] = []
        for domaine in domaines :
            paperToField[publication].append(domaine)
    return paperToField


def AuthorToField(graphe, auteurs):
    """
    Extrait les domaines des auteurs
    prend en paramètre un objet graphe de rdflib et un liste d'id d'autheurs sous forme d'URI
    retourne un dictionnaire associant à un authorID tous les FieldID auxquelles il est rataché
    { authorID : [fieldID, fieldID, fieldID], authorID : [fieldID, ...] ... }
    """
    authIDToFieldID = dict()
    for auteur in auteurs :
        domaines = graphe.objects(auteur, ace.author_is_in_field)
        authIDToFieldID[auteur] = []
        for domaine in domaines :
            authIDToFieldID[auteur].append(domaine)
    return authIDToFieldID


def AuthorToPaper(graphe, auteurs):
    """
    Extrait les papiers qu'un auteur a écrit
    prend en paramètre la liste des auteurs et le graphe de rdflib
    retourne un dictionnaire associant un auteur a toutes ces publication
    { authorID : [paperID, paperID, paperID], authorID : [paperID, ...] ... }
    """
    authWritePaper = dict()
    for auteur in auteurs :
        authWritePaper[auteur] = []
        papers = graphe.subjects(ace.paper_is_written_by, auteur) 
        for paper in papers :
            authWritePaper[auteur].append(paper)
    return authWritePaper

def AuthorToYear(graphe, auteurs, authorToPaper):
    """
    Extrait les années de publication d'un auteur.
    prend en paramètre un graphe rdf une liste d'authorID sous forme d'URI et un dictionnaire qui associe un auteurs a ces publication
    retourne un dictionnaire associant des authorID à des années de publication 
    { authorID : [year, year, year], authorID : [year, ...] ... }
    """
    authIDToYears = dict()
    for auteur in auteurs :
        authIDToYears[auteur] = []
        #on va générer la liste de toutes les publication qui ont été ecrite par l'auteur en question
        for publication in authorToPaper[auteur] :
            dates = graphe.objects(publication, ace.paper_publish_date)
            for date in dates :
                year = YearFromDate(date)
                if not year in authIDToYears[auteur] :
                    authIDToYears[auteur].append(year)
    return authIDToYears

def PaperToAuthor(graphe, publications) :
    """
    Extrait les auteurs pour toutes les publication
    prend en parametre un graphe rdf
    retourne un dictionnaire qui associe les paperID a tous ses authorID
    { paperID : [authorID, authoID, authorID], paperID : [authorID, ...] ... }
    """
    paperIDToAuthorID = dict()
    for publication in publications :
        auteurs = graphe.objects(publication, ace.paper_is_written_by)
        paperIDToAuthorID[publication] = []
        for auteur in auteurs :
            paperIDToAuthorID[publication].append(auteur)
    return paperIDToAuthorID


def PaperCitPaper(graphe, publications) :
    """
    Extrait les publication cités par des publciation
    prend en paramètre la liste des publication
    retourne un dictionnaire associé un publication a toutes les publication qu'elle cite
    { paperID : [paperID, paperID ...] , paperID : ......}
    """
    paperCit = dict()
    for publication in publications :
        paperCit[publication] = []
        cites = graphe.objects(publication, ace.paper_cit_paper)
        for cite in cites :
            paperCit[publication].append(cite)
    return paperCit

def PaperCitAuthor(publications, paperToAuthor, paperCitpaper) :
    """ 
    Crée un dictionnaire associant une publications aux auteurs qu'elle a cité
    prend en paramètres la lsite des publication, un dictionnaire associant une publications aux publications qu'elle cite, un dictionnaire associant une publications à ses auteurs
    retourne un dictionnaire associant es publications aux auteurs qu'elles citent
    { paperID : [authID, authID ...] , paperID : ......}
    """
    paperCitAuthor = dict()
    for publication in publications :
        paperCitAuthor[publication] = []
        for paperCited in paperCitpaper[publication] :
            for authCited in paperToAuthor[paperCited] :
                if not authCited in paperCitAuthor[publication] :
                    paperCitAuthor[publication].append(authCited)
    return paperCitAuthor

def AuthorCitPaper(auteurs, publications, paperToAuthor, paperCitPaper) :
    """
    Crée un dictionnaire associant un auteur au publication qu'il a cité
    prend en paramètres le dictionnaire avec les publication et leur citation, le dictionnaire des publication et de leurs auteurs, le tableau des publications
    renvoit un dictionnaire des auteurs et de leur citation
    { authorID : [paperID, paperID, ...] , ... }
    """
    authorCitPaper = dict()
    for auteur in auteurs :
        authorCitPaper[auteur] = []
    for publication in publications :
        paperCits = paperCitPaper[publication]
        for paperCit in paperCits :
            authors = paperToAuthor[publication]
            for author in authors :
                if not (paperCit in authorCitPaper[author]) :
                    authorCitPaper[author].append(paperCit)
    return authorCitPaper


def FieldToPaper(graphe, domaines) :
    """
    Crée  un dictionnaire associant chaque domaine les publications de celui-ci
    prend un parametre un graphe de rdflib, et la liste des domaines
    retourne un dictionnaire associant un domaines au publications qui s'y rapportent 
    { fieldID : [paperID, paperID ...] , fieldID : ......}
    """
    fieldToPaper = dict()
    for domaine in domaines :
        fieldToPaper[domaine] = []
        publications = graphe.subjects(ace.paper_is_in_field, domaine)
        for publication in publications : 
            fieldToPaper[domaine].append(publication)
    return fieldToPaper

def FieldToAuthor(graphe, domaines) :
    """
    Crée un dictionnaire associant un domaines aux auteurs qui sont dans celui-ci
    prend en paramètres un graphe rdflib et la listes des domaines
    retourne un dictionnaire associant un domaines à ses auteurs 
    { fieldID : [authorID, authorID ...] , fieldID : ......}
    """
    fieldToAuth = dict()
    for domaine in domaines : 
        fieldToAuth[domaine] = []
        auteurs = graphe.subjects(ace.author_is_in_field, domaine)
        for auteur in auteurs : 
            fieldToAuth[domaine].append(auteur)
    return fieldToAuth

def FieldToYear(domaines, fieldToPaper, PaperToYear) :
    """
    Crée un dictionnaire associant un domaines aux années de publications des publications qui sont dans ce domaine
    prend en paramètres la liste des domaine, un dictionnaire associant un domaine à ces publication, un dictionnaire associant une publication à son année de publication
    retourne un dictionnaire associant un domaines à ses années de publications
    { fieldID : [year, year ...] , fieldID : ......}
    """
    FieldToYear = dict()
    for domaine in domaines : 
        FieldToYear[domaine] = []
        for publication in fieldToPaper[domaine] :
            if not PaperToYear[publication] in FieldToYear[domaine] :
                FieldToYear[domaine].append(PaperToYear[publication])
    return FieldToYear

def PaperCitField(publications, paperToField, paperCitPaper) :
    """
    Crée un dictionnaire associant une publication au domaine des publication quelle cite
    prend en paramètre un dictionnaire associant publication aux publications qu'il cite, un dictionnaire associant une publication a ces domaines
    retourne un dictionnaire associant une publication aux domaines des publications qu'elle cite
    { paperID : [fieldID, fielID ...] , paperID : ......}
    """
    paperCitField = dict()
    for publication in publications :
        paperCitField[publication] = []
        for paperCited in paperCitPaper[publication] :
            for field in paperToField[paperCited] :
                if field not in paperCitField[publication] :
                    paperCitField[publication].append(field)
    return paperCitField

def FieldCitPaper(domaines, fieldToPaper, paperCitPaper) :
    """
    Crée un dictionnaire associant un domaines aux papier qui sont cités dans ce domaine
    prend en paramètres la liste des domaines, un dictionnaire associant les domaines et ses publications associés, un dictionnaire associant des publications et les pulications quelle à cité
    retourne un dictionnaire associant domaine et ses publications cités
    { fieldID : [paperID, paperID ...] , fieldID : ......}
    """
    fieldCitPaper = dict()
    for domaine in domaines :
        fieldCitPaper[domaine] = []
        for paper in fieldToPaper[domaine] :
            for paperCit in paperCitPaper[paper] :
                if not paperCit in fieldCitPaper[domaine] :
                    fieldCitPaper[domaine].append(paperCit)
    return fieldCitPaper


def Coauteurs(auteurs, paperToAuthor, authorToPaper):
    """
    Crée  un dictionnaire associant chaque auteur à ses coauteurs
    prend en paramètre un dictionnaire associant les publication à leurs auteurs (cf ExtraireAuteursPubli), un tableau des auteurs et un dictionnaire associant les auteurs a leurs publication
    retourne un dictionnaire sous la forme { authID : [authID, authID ...] , authID : ......}
    """
    coaut = dict()
    for auteur in auteurs :
        coaut[auteur] = []
    for auteur in auteurs :
        for publication in authorToPaper[auteur] :
            for aut in paperToAuthor[publication] :
                if (aut != auteur) and (not (aut in coaut[auteur])) :
                    coaut[auteur].append(aut)
                    if( not auteur in coaut[aut]) :
                        coaut[aut].append(auteur)
    return coaut


def Citation(auteurs, paperToAuthor, authorCitPaper) :
    """
    Crée un dictionnaire associant chaque auteur aux auteurs qu'il a cité
    prend en parametres un dictionnaire associant un auteur aux publication qu'il a cité, un talbeau d'auteurs, un dictionnaire associant des publications à leurs auteurs
    retourne un dictionnaire associant un auteur aux auteurs qu'il a cité
    exemple : { authID : [authID, authID ...] , authID : ......}
    """
    citAuteur = dict()
    for auteur in auteurs :
        citAuteur[auteur] = []
        for publiCit in authorCitPaper[auteur] :
            for authorCit in paperToAuthor[publiCit] :
                if not authorCit in citAuteur[auteur] :
                    citAuteur[auteur].append(authorCit)
    return citAuteur                


def Copublication(publications, paperToAuthor, authorToPaper) :
    """
    Crée un dictionnaire associant une publication aux autres publication ayant été écrite par le même auteurs
    prend en paramètre la liste des publicaiton, un dictionnaire associant un auteur à ces publication, un dictionnaire associant une publication à ces auteurs
    retourne un dictionnaire qui associe une publication aux publications écrites par le même auteur
    { paperID : [paperID, paperID ...] , paperID : ......}
    """
    copubli = dict()
    for publication in publications :
        copubli[publication] = []
    for publication in publications :
        for author in paperToAuthor[publication] :
            for paper in authorToPaper[author] :
                if (paper != publication) and not (paper in copubli[publication])   :
                    copubli[publication].append(paper)
                    if not publication in copubli[paper] :
                        copubli[paper].append(publication)
    return copubli

    
def CoOccurrence(domaines, paperToField, fieldToPaper) :
    """
    crée un dictionnaire associant une domaine aux domaines avec lesquelles il a des publications en commun
    prend en paramètres la liste des domaines, un dictionnaire associant une publications à ces domaines, un dictionnaire associant un domaine aux publication qui sont dans celui-ci
    retourne un dictionnaire associant un domaines aux domaines qui ont des publications communes avec lui
    { fieldID : [fieldID, fieldID ...] , fieldID : ......}
    """
    coOccurrence = dict()
    for domaine in domaines :
        coOccurrence[domaine] = []
    for domaine in domaines :
        publications = fieldToPaper[domaine]
        for publication in publications :
            for commonField in paperToField[publication] :
                if commonField != domaine and not commonField in coOccurrence[domaine] :
                    coOccurrence[domaine].append(commonField)
                    if not domaine in coOccurrence[commonField] :
                        coOccurrence[commonField].append(domaine)
    return coOccurrence


def CitationE(domaines, paperToField, fieldCitPaper):
    """
    Crée un dictionnaire associant un domaines au domaines qu'il cite
    prend en paramètres la liste des domaines, un dictionnaire associant domaine et ses publication, un dictionnaire associant une publication aux publications qu'elle cite
    renvoit un dictionnaire associant un domaine avec les domaines qu'il cite
    { fieldID : [fieldID, fieldID ...] , fieldID : ......}
    """
    citationE = dict()
    for domaine in domaines :
        citationE[domaine] = []
        for paperCited in fieldCitPaper[domaine] :
            for fieldCited in paperToField[paperCited] :
                if not fieldCited in citationE[domaine] : 
                    citationE[domaine].append(fieldCited)
    return citationE

def PublicationsAuteurs(authorToPaper, paperToAuth):
    """
    Crée un dictionnaire associant des auteurs à leurs oeuvre et des oeuvres à leurs auteurs (on essaye de représenter les liens d'un graphe bipartis)
    prend en paramètre un dictionnaire associant les auteurs à leurs oeuvres, un dictionnaire associant les oeuvres à leurs auteurs
    retourne un dictionnaire composé des 2 dictionnaires en paramètres 
    {
        "authorToPaper" : { authorID : [paperID, paperID, ...], authorID : ... },
        "paperToAuth" : { paperID : [authorID, authoID, ...], paperID : ... }
    }
    """
    publications_Auteurs = dict()
    publications_Auteurs.update(authorToPaper)
    publications_Auteurs.update(paperToAuth)
    return publications_Auteurs

def AuteurPublicationCitees(publications, authorCitPaper) :
    """
    Crée un dictionnaire associant des auteurs aux publications qu'ils ont citées (graphe bi parti orienté aut->pubCitées)
    prend en paramètre un tableau associant les auteurs aux publications qu'ils ont citées, une listes des publications
    retourne dictionnaire associant des auteurs aux publications et liste les publications
    {
        "authorCitPaper" : { authorID : [paperID, paperID, ...], authorID : ... },
        "papers" : [paperID, ..., .....]
    }
    """
    auteurPublicationCitees = dict()
    for publication in publications : 
        auteurPublicationCitees[publication] = []
    auteurPublicationCitees.update(authorCitPaper)

    return auteurPublicationCitees

def PublicationAuteurCites(auteurs, paperCitAuthor) :
    """
    Crée un dictionnaire associant des publications aux auteurs qu'elles ont cités (graphe bi parti orienté pub->auteurCit)
    prend en paramètre un dictionnaire associant les publications aux auteurs qu'elles ont cités, une listes des auteurs
    retourne dictionnaire associant des publications aux auteurs et la liste les auteurs
    {
        "paperCitAuthor" : { paperID : [authorID, authorID, ...], paperID : ... },
        "authors" : [authID, ..., .....]
    }
    """
    publicationAuteurCites = dict()
    publicationAuteurCites.update(paperCitAuthor)
    for auteur in auteurs :
        publicationAuteurCites[auteur] = []
    return publicationAuteurCites


def AjouterPrefixe(prefixe, chaine) :
    """
    Fonction qui ajoute un préfixe à une chaine de caractère et remplace les " " par des "_"
    retourne une chaine de caractères avec le préfixe placé devant
    exemple : AjouterPrefixe("AUTH", "Albert Einstein") retourne "AUTH_Albert_Einstein"
    """
    pref = prefixe + "_"
    new_chaine = pref + chaine.replace(" ", "_")
    return new_chaine

def AjouterPrefixes(prefixe, liste) :
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


def ListerAttributs(dictionnaire):
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

def IndexerElements(index, listeElements) :
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

def CreerGrapheIndex(listeSommets, graphe, index) :
    """
    Crée un dictionnaire ne contenant que des index liée à d'autres index
    prend en parametres la liste des sommets du graphe, un dictionnaire représentant le graphe, un dictionnaire avec les index des dfférents élements.
    Retourne le dictionnaire du graphe composé des index
    """
    grapheIndex = dict()
    for element in listeSommets :
        indexElement = index[element]
        grapheIndex[indexElement] = []
        for lien in graphe[element] :
            grapheIndex[indexElement].append(index[lien])
    return grapheIndex

def CreerItemsetsIndex(listeSommets, itemsets, index) :
    """
    Crée un dictionnaire ne contenant que des index liées à d'autres index.
    Prend en paramètres la liste des sommets d'un graphe, un dictionnaire représentant l'itemsets, un dictionnaire des index des éléments.
    Retourne le dictionnaire de l'itemsets composé des index
    """
    itemsetsIndex = dict()
    for sommet in listeSommets :
        indexSommet = index[sommet]
        itemsetsIndex[indexSommet] = []
        for lien in itemsets[sommet] :
            itemsetsIndex[indexSommet].append(index[lien])
    return itemsetsIndex

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

def IDFromURI(URI):
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

def Union(lst1, lst2):
    """
    Fait l'union entre 2 liste (union mathématique U).
    Prend en paramètres 2 listes.
    Retourne l'union des 2 listes dans un liste
    exemple : Union([a, b], [b, c]) = [a, b, c]
    """
    lst = list(set(lst1) | set(lst2))
    return lst

def CreerCoauteurs(graphe) :
    """
    Crée la structure NRI du graphe des coauteurs.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    nri = dict()
    itemsets = dict()
    index = dict()

    IDAuthors = ExtraireAuteurs(graphe)
    IDPapers = ExtrairePublications(graphe)
    IDField = ExtraireConceptes(graphe)
    paperToAuthor = PaperToAuthor(graphe, IDPapers)
    authorToPaper = AuthorToPaper(graphe, IDAuthors)
    authorToField = AuthorToField(graphe, IDAuthors)
    authorToYear = AuthorToYear(graphe, IDAuthors, authorToPaper)
    nomAuteurs = IDToAuthor(graphe, IDAuthors)
    nomField = IDToField(graphe, IDField)
    grapheCoauteurs = Coauteurs(IDAuthors, paperToAuthor, authorToPaper)

    years = ListerAnnees(authorToYear)
    fields = ListerAttributs(authorToField)
    items = years + fields
    
    listeNomAuteurs = ListerNoms(IDAuthors, nomAuteurs)
    listeNomField = ListerNoms(IDField, nomField)

    IndexerElements(index, IDAuthors)
    IndexerElements(index, items)

    AjouterPrefixes("AUTH", listeNomAuteurs)
    AjouterPrefixes("Year", years)
    AjouterPrefixes("CONC", listeNomField)

    items = years + listeNomField

    #construire l'itemset :
    i = 0
    lgListe = len(IDAuthors)
    while i < lgListe :
        auteur = IDAuthors[i]
        itemsets[auteur] = authorToYear[auteur] + authorToField[auteur] #on sait que ce sont 2 tableaux donc on peut les concatener
        i += 1

    nri["Objets"] = listeNomAuteurs
    nri["Items"] = items
    nri["Itemsets"] = CreerItemsetsIndex(IDAuthors, itemsets, index)
    nri["Graphe"] = CreerGrapheIndex(IDAuthors, grapheCoauteurs, index)
     
    return nri

def CreerCitations(graphe) :
    """
    Crée la structure NRI du graphe des citations (entre auteurs).
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    nri = dict()
    itemsets = dict()
    index = dict()

    IDAuthors = ExtraireAuteurs(graphe)
    IDPapers = ExtrairePublications(graphe)
    IDField = ExtraireConceptes(graphe)
    
    paperToAuthor = PaperToAuthor(graphe, IDPapers)
    paperCitPaper = PaperCitPaper(graphe, IDPapers)
    authorCitPaper = AuthorCitPaper(IDAuthors, IDPapers, paperToAuthor, paperCitPaper)
    citations = Citation(IDAuthors, paperToAuthor, authorCitPaper)

    authorToField = AuthorToField(graphe, IDAuthors)
    authorToYear = AuthorToYear(graphe, IDAuthors, AuthorToPaper(graphe, IDAuthors))

    nomAuteurs = IDToAuthor(graphe, IDAuthors)
    nomField = IDToField(graphe, IDField)

    years = ListerAnnees(authorToYear)
    fields = ListerAttributs(authorToField)
    items = years + fields
    
    listeNomAuteurs = ListerNoms(IDAuthors, nomAuteurs)
    listeNomField = ListerNoms(IDField, nomField)

    IndexerElements(index, IDAuthors)
    IndexerElements(index, items)

    AjouterPrefixes("AUTH", listeNomAuteurs)
    AjouterPrefixes("Year", years)
    AjouterPrefixes("CONC", listeNomField)

    items = years + listeNomField

    #construire l'itemset :
    i = 0
    lgListe = len(IDAuthors)
    while i < lgListe :
        auteur = IDAuthors[i]
        itemsets[auteur] = authorToYear[auteur] + authorToField[auteur] #on sait que ce sont 2 tableaux donc on peut les concatener
        i += 1

    nri["Objets"] = listeNomAuteurs
    nri["Items"] = items
    nri["Itemsets"] = CreerItemsetsIndex(IDAuthors, itemsets, index)
    nri["Graphe"] = CreerGrapheIndex(IDAuthors, citations, index)

    return nri

def CreerCopublications(graphe) :
    """
    Crée la structure NRI du graphe des copublications.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    nri = dict()
    itemsets = dict()
    index = dict()

    IDAuthors = ExtraireAuteurs(graphe)
    IDPapers = ExtrairePublications(graphe)

    paperToAuthor = PaperToAuthor(graphe, IDPapers)
    authorToPaper = AuthorToPaper(graphe, IDAuthors)
    copublications = Copublication(IDPapers, paperToAuthor, authorToPaper)

    paperToYear = PaperToYear(graphe, IDPapers)
    paperToField = PaperToField(graphe, IDPapers)

    years = ListerAnnees(paperToYear)
    fields = ListerAttributs(paperToField)
    authors = ListerAttributs(paperToAuthor)

    items = authors + years + fields
    listeNomsAuteurs = ListerNoms(authors, IDToAuthor(graphe, authors))
    listeNomsFields = ListerNoms(fields, IDToField(graphe, fields))
    listeIDPapers = ListerID(IDPapers)

    IndexerElements(index, items)
    IndexerElements(index, IDPapers)

    AjouterPrefixes("AUTH", listeNomsAuteurs)
    AjouterPrefixes("Year", years)
    AjouterPrefixes("CONC", listeNomsFields)
    AjouterPrefixes("PAPE", listeIDPapers)

    items = listeNomsAuteurs + years + listeNomsFields

    #construire l'itemset :
    i = 0
    lgListe = len(IDPapers)
    while i < lgListe :
        paper = IDPapers[i]
        #paperToYeaur[paper] n'est pas un tableau on peut pas le concatener comme ca
        year = []
        year.append(paperToYear[paper])
        itemsets[paper] = paperToAuthor[paper] + year + paperToField[paper]
        i += 1
    
    nri["Objets"] = listeIDPapers
    nri["Items"] = items
    nri["Itemsets"] = CreerItemsetsIndex(IDPapers, itemsets, index)
    nri["Graphe"] = CreerGrapheIndex(IDPapers, copublications, index)

    return nri


def CreerCitationsP(graphe):
    """
    Crée la structure NRI du graphe des citation (entre publications).
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    nri = dict()
    itemsets = dict()
    index = dict()

    IDPapers = ExtrairePublications(graphe)
    paperCitPaper = PaperCitPaper(graphe, IDPapers)

    paperToAuthor = PaperToAuthor(graphe, IDPapers)
    paperToYear = PaperToYear(graphe, IDPapers)
    paperToField = PaperToField(graphe, IDPapers)

    auteurs = ListerAttributs(paperToAuthor)
    fields = ListerAttributs(paperToField)
    years = ListerAnnees(paperToYear)

    items = auteurs + years + fields

    listeNomsAuteurs = ListerNoms(auteurs, IDToAuthor(graphe, auteurs))
    listeNomsFields = ListerNoms(fields, IDToField(graphe, fields))
    listeIDPapers = ListerID(IDPapers)

    IndexerElements(index, items)
    IndexerElements(index, IDPapers)

    AjouterPrefixes("AUTH", listeNomsAuteurs)
    AjouterPrefixes("Year", years)
    AjouterPrefixes("CONC", listeNomsFields)
    AjouterPrefixes("PAPE", listeIDPapers)

    items = listeNomsAuteurs + years + listeNomsFields

    #construire l'itemset :
    i = 0
    lgListe = len(IDPapers)
    while i < lgListe :
        paper = IDPapers[i]
        #paperToYear[paper] n'est pas un tableau on peut pas le concatener comme ca
        year = []
        year.append(paperToYear[paper])
        itemsets[paper] = paperToAuthor[paper] + year + paperToField[paper]
        i += 1
    
    nri["Objets"] = listeIDPapers
    nri["Items"] = items
    nri["Itemsets"] = CreerItemsetsIndex(IDPapers, itemsets, index)
    nri["Graphe"] = CreerGrapheIndex(IDPapers, paperCitPaper, index)

    return nri

def CreerCooccurence(graphe) :
    """
    Crée la structure NRI du graphe de cooccurence.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    nri = dict()
    itemsets = dict()
    index = dict()   

    IDField = ExtraireConceptes(graphe)
    IDPaper = ExtrairePublications(graphe)

    paperToField = PaperToField(graphe, IDPaper)
    fieldToPaper = FieldToPaper(graphe, IDField)
    coocurrence = CoOccurrence(IDField, paperToField, fieldToPaper)


    fieldToAuthor = FieldToAuthor(graphe, IDField)
    paperToYear = PaperToYear(graphe, IDPaper)
    fieldToYear = FieldToYear(IDField, fieldToPaper, paperToYear)

    auteurs = ListerAttributs(fieldToAuthor)
    years = ListerAnnees(fieldToYear)

    items = auteurs + years

    listeNomAuteurs = ListerNoms(auteurs, IDToAuthor(graphe, auteurs))
    listeNomFields = ListerNoms(IDField, IDToField(graphe, IDField))

    IndexerElements(index, items)
    IndexerElements(index, IDField)

    AjouterPrefixes("AUTH", listeNomAuteurs)
    AjouterPrefixes("Year", years)
    AjouterPrefixes("CONC", listeNomFields)

    items = listeNomAuteurs + years

    #construire l'itemset :
    i = 0
    lgListe = len(IDField)
    while i < lgListe :
        field = IDField[i]
        itemsets[field] = fieldToAuthor[field] + fieldToYear[field]
        i += 1
    
    nri["Objets"] = listeNomFields
    nri["Items"] = items
    nri["Itemsets"] = CreerItemsetsIndex(IDField, itemsets, index)
    nri["Graphe"] = CreerGrapheIndex(IDField, coocurrence, index)

    return nri

def CreerCitationsE(graphe) :
    """
    Crée la structure NRI du graphe de citation (entre les thématiques).
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    nri = dict()
    itemsets = dict()
    index = dict()   

    IDField = ExtraireConceptes(graphe)
    IDPaper = ExtrairePublications(graphe)

    paperToField = PaperToField(graphe, IDPaper)
    fieldToPaper = FieldToPaper(graphe, IDField)
    paperCitPaper = PaperCitPaper(graphe, IDPaper)
    fieldCitPaper = FieldCitPaper(IDField, fieldToPaper, paperCitPaper)
    citationsE = CitationE(IDField, paperToField, fieldCitPaper)

    fieldToAuthor = FieldToAuthor(graphe, IDField)
    paperToYear = PaperToYear(graphe, IDPaper)
    fieldToYear = FieldToYear(IDField, fieldToPaper, paperToYear)

    auteurs = ListerAttributs(fieldToAuthor)
    years = ListerAnnees(fieldToYear)

    items = auteurs + years

    listeNomAuteurs = ListerNoms(auteurs, IDToAuthor(graphe, auteurs))
    listeNomFields = ListerNoms(IDField, IDToField(graphe, IDField))

    IndexerElements(index, items)
    IndexerElements(index, IDField)

    AjouterPrefixes("AUTH", listeNomAuteurs)
    AjouterPrefixes("Year", years)
    AjouterPrefixes("CONC", listeNomFields)

    items = listeNomAuteurs + years

    #construire l'itemset :
    i = 0
    lgListe = len(IDField)
    while i < lgListe :
        field = IDField[i]
        itemsets[field] = fieldToAuthor[field] + fieldToYear[field]
        i += 1
    
    nri["Objets"] = listeNomFields
    nri["Items"] = items
    nri["Itemsets"] = CreerItemsetsIndex(IDField, itemsets, index)
    nri["Graphe"] = CreerGrapheIndex(IDField, citationsE, index)

    return nri

def CreerPubAut(graphe) :
    """
    Crée la structure NRI du graphe bipartis entre les auteurs et leurs publications.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    nri = dict()
    itemsets = dict()
    index = dict() 


    IDAuthors = ExtraireAuteurs(graphe)
    IDPapers = ExtrairePublications(graphe)
    authToPaper = AuthorToPaper(graphe, IDAuthors)
    paperToAuth = PaperToAuthor(graphe, IDPapers)
    publicationsAuteurs = PublicationsAuteurs(authToPaper, paperToAuth)

    #attributs
    authorToYear = AuthorToYear(graphe, IDAuthors, authToPaper)
    authorToField = AuthorToField(graphe, IDAuthors)
    paperToYear = PaperToYear(graphe, IDPapers)
    paperToField = PaperToField(graphe, IDPapers)

    aYears = ListerAnnees(authorToYear)
    pYears = ListerAnnees(paperToYear)
    aField = ListerAttributs(authorToField)
    pField = ListerAttributs(paperToField)

    fields = Union(aField, pField)

    sommets = IDPapers + IDAuthors

    listeNomAuteurs = ListerNoms(IDAuthors, IDToAuthor(graphe, IDAuthors))
    listeIDPapers = ListerID(IDPapers)
    listeNomFields = ListerNoms(fields, IDToField(graphe, fields))

    AjouterPrefixes("A_Year", aYears)
    AjouterPrefixes("P_Year", pYears)

    items = aYears + pYears + fields

    IndexerElements(index, sommets)
    IndexerElements(index, items)

    AjouterPrefixes("AUTH", listeNomAuteurs)
    AjouterPrefixes("PAPE", listeIDPapers)
    AjouterPrefixes("CONC", listeNomFields)

    items = aYears + pYears + listeNomFields
    NomSommets = listeIDPapers + listeNomAuteurs

    #construire l'itemsets partie publications :
    i = 0
    lgListe = len(IDPapers)
    while i < lgListe :
        publi = IDPapers[i]
        year = []
        year.append(AjouterPrefixe("P_Year", paperToYear[publi]))
        itemsets[publi] = year + paperToField[publi]
        i += 1
    #construire l'itemsets partie auteurs :
    i = 0
    lgListe = len(IDAuthors)
    while i < lgListe :
        auteur = IDAuthors[i]
        AjouterPrefixes("A_Year", authorToYear[auteur])
        itemsets[auteur] = authorToYear[auteur] + authorToField[auteur]
        i += 1
    #print(publicationsAuteurs)
    nri["Objets"] = NomSommets
    nri["Items"] = items
    nri["Itemsets"] = CreerItemsetsIndex(sommets, itemsets, index)
    nri["Graphe"] = CreerGrapheIndex(sommets, publicationsAuteurs, index)
    return nri


def CreerAutPubCitees(graphe) :
    """
    Crée la structure NRI du graphe bipartis des auteurs vers les publications qu'ils citent.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    nri = dict()
    itemsets = dict()
    index = dict() 


    IDAuthors = ExtraireAuteurs(graphe)
    IDPapers = ExtrairePublications(graphe)
    authToPaper = AuthorToPaper(graphe, IDAuthors)


    paperToAuthor = PaperToAuthor(graphe, IDPapers)
    paperCitPaper = PaperCitPaper(graphe, IDPapers)
    authorCitPaper = AuthorCitPaper(IDAuthors, IDPapers, paperToAuthor, paperCitPaper)
    auteurPublicationCitees = AuteurPublicationCitees(IDPapers, authorCitPaper)

    #attributs
    authorToYear = AuthorToYear(graphe, IDAuthors, authToPaper)
    authorToField = AuthorToField(graphe, IDAuthors)
    paperToYear = PaperToYear(graphe, IDPapers)
    paperToField = PaperToField(graphe, IDPapers)

    aYears = ListerAnnees(authorToYear)
    pYears = ListerAnnees(paperToYear)
    aField = ListerAttributs(authorToField)
    pField = ListerAttributs(paperToField)

    fields = Union(aField, pField)

    sommets = IDPapers + IDAuthors

    listeNomAuteurs = ListerNoms(IDAuthors, IDToAuthor(graphe, IDAuthors))
    listeIDPapers = ListerID(IDPapers)
    listeNomFields = ListerNoms(fields, IDToField(graphe, fields))

    AjouterPrefixes("A_Year", aYears)
    AjouterPrefixes("P_Year", pYears)

    items = aYears + pYears + fields

    IndexerElements(index, sommets)
    IndexerElements(index, items)

    AjouterPrefixes("AUTH", listeNomAuteurs)
    AjouterPrefixes("PAPE", listeIDPapers)
    AjouterPrefixes("CONC", listeNomFields)

    items = aYears + pYears + listeNomFields
    NomSommets = listeIDPapers + listeNomAuteurs

    #construire l'itemsets partie publications :
    i = 0
    lgListe = len(IDPapers)
    while i < lgListe :
        publi = IDPapers[i]
        year = []
        year.append(AjouterPrefixe("P_Year", paperToYear[publi]))
        itemsets[publi] = year + paperToField[publi]
        i += 1
    #construire l'itemsets partie auteurs :
    i = 0
    lgListe = len(IDAuthors)
    while i < lgListe :
        auteur = IDAuthors[i]
        AjouterPrefixes("A_Year", authorToYear[auteur])
        itemsets[auteur] = authorToYear[auteur] + authorToField[auteur]
        i += 1

    nri["Objets"] = NomSommets
    nri["Items"] = items
    nri["Itemsets"] = CreerItemsetsIndex(sommets, itemsets, index)
    nri["Graphe"] = CreerGrapheIndex(sommets, auteurPublicationCitees, index)
    return nri

def CreerPubAutCites(graphe) :
    """
    Crée la structure NRI du graphe bipartis des publications vers les auteurs qu'elles citent.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    nri = dict()
    itemsets = dict()
    index = dict() 


    IDAuthors = ExtraireAuteurs(graphe)
    IDPapers = ExtrairePublications(graphe)
    authToPaper = AuthorToPaper(graphe, IDAuthors)

    paperToAuthor = PaperToAuthor(graphe, IDPapers)
    paperCitPaper = PaperCitPaper(graphe, IDPapers)
    paperCitAuthor = PaperCitAuthor(IDPapers, paperToAuthor, paperCitPaper)
    pubAuteursCites = PublicationAuteurCites(IDAuthors, paperCitAuthor)

    #attributs
    authorToYear = AuthorToYear(graphe, IDAuthors, authToPaper)
    authorToField = AuthorToField(graphe, IDAuthors)
    paperToYear = PaperToYear(graphe, IDPapers)
    paperToField = PaperToField(graphe, IDPapers)

    aYears = ListerAnnees(authorToYear)
    pYears = ListerAnnees(paperToYear)
    aField = ListerAttributs(authorToField)
    pField = ListerAttributs(paperToField)

    fields = Union(aField, pField)

    sommets = IDPapers + IDAuthors

    listeNomAuteurs = ListerNoms(IDAuthors, IDToAuthor(graphe, IDAuthors))
    listeIDPapers = ListerID(IDPapers)
    listeNomFields = ListerNoms(fields, IDToField(graphe, fields))

    AjouterPrefixes("A_Year", aYears)
    AjouterPrefixes("P_Year", pYears)

    items = aYears + pYears + fields

    IndexerElements(index, sommets)
    IndexerElements(index, items)

    AjouterPrefixes("AUTH", listeNomAuteurs)
    AjouterPrefixes("PAPE", listeIDPapers)
    AjouterPrefixes("CONC", listeNomFields)

    items = aYears + pYears + listeNomFields
    NomSommets = listeIDPapers + listeNomAuteurs

    #construire l'itemsets partie publications :
    i = 0
    lgListe = len(IDPapers)
    while i < lgListe :
        publi = IDPapers[i]
        year = []
        year.append(AjouterPrefixe("P_Year", paperToYear[publi]))
        itemsets[publi] = year + paperToField[publi]
        i += 1
    #construire l'itemsets partie auteurs :
    i = 0
    lgListe = len(IDAuthors)
    while i < lgListe :
        auteur = IDAuthors[i]
        AjouterPrefixes("A_Year", authorToYear[auteur])
        itemsets[auteur] = authorToYear[auteur] + authorToField[auteur]
        i += 1

    nri["Objets"] = NomSommets
    nri["Items"] = items
    nri["Itemsets"] = CreerItemsetsIndex(sommets, itemsets, index)
    nri["Graphe"] = CreerGrapheIndex(sommets, pubAuteursCites, index)
    return nri