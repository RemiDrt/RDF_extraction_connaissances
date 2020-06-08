#!/usr/bin/python
#coding=utf-8
from rdflib import Graph, RDF, URIRef
from rdflib.namespace import XSD , FOAF, Namespace

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
    Pas besoin de représenté les liaisons qui n'y sont pas donc c'est la même forme que l'itemsets
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


def AjouterPrefixe(prefixe, chaine) :
    """
    Fonction qui ajouter un préfixe à une chaine de caractère et remplace les " " par des "_"
    retourne une chaine de caractères avec le préfixe placé devant
    exemple : AjouterPrefixe("AUTH", "Albert Einstein") retourne "AUTH_Albert_Einstein"
    """
    pref = prefixe + "_"
    new_chaine = pref + chaine.replace(" ", "_")
    return new_chaine

def YearFromDate(date) :
    """
    Extrait l'année d'un date qui est au format xsd.date (YYYY-MM-DD)
    Retourne la chaine de caractère correspondant à l'année de la date
    """
    return date[:4]  


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


def ExtraireNomAuteurs(graphe, auteurs) :
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


def ExtraireNomConceptes(graphe, conceptes) :
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


def PaperToYear(graphe, publications) :
    """
    Extrait les dates et les associ a leurs publication
    prend en paramètre un graphe rdflib et la liste des publication
    retourne un dicitonnaire associant publicationID à sa date de publication (jespere qu'il en a qu'une seul)
    exemple : { paperID : date, paperID : date ....... }
    """
    paperToYear = dict()
    for publication in publications :
        dates = graphe.objects(publication, ace.paper_publish_date)
        for date in dates :
            paperToYear[publication] = date
    return paperToYear


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


def AuthorWritePaper(graphe, auteurs):
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

def ExtrairesDate(graphe, authorWritePaper, auteurs):
    """
    Extrait les dates de publication d'un auteur.
    prend en paramètre un graphe rdf une liste d'authorID sous forme d'URI et un dictionnaire qui associe un auteurs a ces publication
    retourne un dictionnaire associant des authorID à des dates de publication 
    { authorID : [date, date, date], authorID : [date, ...] ... }
    """
    authIDToYears = dict()
    for auteur in auteurs :
        authIDToYears[auteur] = []
        #on va générer la liste de toutes les publication qui ont été ecrite par l'auteur en question
        for publication in authorWritePaper[auteur] :
            dates = graphe.objects(publication, ace.paper_publish_date)
            for date in dates :
                authIDToYears[auteur].append(date)
    return authIDToYears

def ExtraireAuteursPubli(graphe, publications) :
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


def ExtrairePubliCit(graphe, publications) :
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

def AuthToPaperCit(paperCitPaper, paperToAuthor, publications, auteurs) :
    """
    Crée un dictionnaire associant un auteur au publication qu'il a cité
    prend en paramètres le dictionnaire avec les publication et leur citation, le dictionnaire des publication et de leurs auteurs, le tableau des publications
    renvoit un dictionnaire des auteurs et de leur citation
    { authorID : [paperID, paperID, ...] , ... }
    """
    authToPaperCit = dict()
    for auteur in auteurs :
        authToPaperCit[auteur] = []
    for publication in publications :
        paperCits = paperCitPaper[publication]
        for paperCit in paperCits :
            authors = paperToAuthor[publication]
            for author in authors :
                if not (paperCit in authToPaperCit[author]) :
                    authToPaperCit[author].append(paperCit)
    return authToPaperCit


def Coauteurs(paperToAuthor, auteurs, authorToPaper):
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

def Citation(authorCitPaper, auteurs, paperToAuthor) :
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


def Copublication(publications, paperToAuthor, authToPaper) :
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
            for paper in authToPaper[author] :
                if (paper != publication) and not (paper in copubli[publication])   :
                    copubli[publication].append(paper)
                    if not publication in copubli[paper] :
                        copubli[paper].append(publication)
    return copubli

    


