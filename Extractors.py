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
    publications_Auteurs["authorToPaper"] = authorToPaper
    publications_Auteurs["paperToAuth"] = paperToAuth
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
    auteurPublicationCitees["authorCitPaper"] = authorCitPaper
    auteurPublicationCitees["papers"] = publications
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
    publicationAuteurCites["paperCitAuthor"] = paperCitAuthor
    publicationAuteurCites["authors"] = auteurs
    return publicationAuteurCites


def CréerCoauteurs(graphe) :
    """
    Crée la structure NRI du graphe des coauteurs.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    NRICoauteurs = dict()
    itemsets = dict()
    index = dict()

    IDAuthors = ExtraireAuteurs(graphe)
    IDPapers = ExtrairePublications(graphe)
    IDField = ExtraireConceptes(graphe)
    paperToAuthor = PaperToAuthor(graphe, IDPapers)
    authorToPaper = AuthorToPaper(graphe, IDAuthors)
    authorToField = AuthorToField(graphe, IDAuthors)
    AuthorToYear = AuthorToYear(graphe, IDAuthors, authorToPaper)
    nomAuteurs = IDToAuthor(graphe, IDAuthors)
    nomField = IDToField(graphe, IDField)
    grapheCoauteurs = Coauteurs(IDAuthors, paperToAuthor, authorToPaper)

    years = ListerAnnees(AuthorToYear)
    fields = ListerAttributs(authorToField)
    items = dates + fields
    
    listeNomAuteurs = []
    listeNomField = []


    #construction de l'itemSet (on en profite tant qu'on boucles pour retenir l'index des différents élements et les nom des auteurs  )
    i = 0
    lgItems = len(items)
    while i < lgItems :
        item = items[i]
        index[item] = i
        i += 1

    i = 0
    lgAuteurs = len(IDAuthors)
    while i < lgAuteurs :
        auteur = IDAuthors[i]
        index[auteur] = i
        listeNomAuteurs.append(nomAuteurs[auteur])
        itemsets[auteur] = AuthorToYear[auteur] + authorToField[auteur]
        i += 1


    i = 0
    lgFields = len(fields)
    while i < lgFields :
        field = fields[i]
        listeNomField.append(nomField[field])
        i += 1
    #pour aller chercher le nom du doaine on fait son index - longueur de years

    NRICoauteurs["Objets"] = IDAuthors
    NRICoauteurs["Items"] = items
    NRICoauteurs["Itemsets"] = itemsets
    NRICoauteurs["Graphe"] = grapheCoauteurs
     
    # a ce moment on a un dico avec des objets composé de la liste des ID d'auteurs
    # des items la liste des years concaténé a la liste des ID fields
    # un itemsets avec un Id auteurs associés à 

    #il faudrait mtn changé objets par leurs nom et pareil pour item
    #et changer pour itemsets et graphe les id par les indices
    return NRICoauteurs



