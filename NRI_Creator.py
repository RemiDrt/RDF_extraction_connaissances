#librairi des fonctions pour la création des structures NRI
from Utilities import *
from Extractors import CreerNRI
def CreerItemsetsIndex(listeSommets, itemsets, index) : #dossier creation des nri ?
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


def CreerGrapheIndex(listeSommets, graphe, index) : #dossier de creation des nri ?
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


def CreerCoauteurs() :#dossier creaer nri ?
    """
    Crée la structure NRI du graphe des coauteurs.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    itemsets = dict()
    index = dict()

    IDAuthors = ImportFromJSONStruc("../Data/JSON_struct/Authors.json")
    IDField = ImportFromJSONStruc("../Data/JSON_struct/Fields.json")
    authorToField = ImportFromJSONStruc("../Data/JSON_struct/AuthorToField.json")
    authorToYear = ImportFromJSONStruc("../Data/JSON_struct/AuthorToYear.json")
    nomAuteurs = ImportFromJSONStruc("../Data/JSON_struct/IDToAuthor.json")
    nomField = ImportFromJSONStruc("../Data/JSON_struct/IDToField.json")
    grapheCoauteurs = ImportFromJSONStruc("../Data/JSON_struct/Coauteurs.json")

    years = ListerAnnees(authorToYear)
    fields = ListerAttributs(authorToField)
    items = years + fields
    
    listeNomAuteurs = ListerID(IDAuthors)
    listeNomField = ListerID(IDField)

    IndexerElements(index, IDAuthors)
    IndexerElements(index, items)

    AjouterPrefixes("AUTH", listeNomAuteurs)
    AjouterPrefixes("Year", years)
    AjouterPrefixes("CONC", listeNomField)

    items = years + listeNomField
    #fonction pour creer itemsets ??
    #construire l'itemset :
    i = 0
    lgListe = len(IDAuthors)
    while i < lgListe :
        auteur = IDAuthors[i]
        itemsets[auteur] = authorToYear[auteur] + authorToField[auteur] #on sait que ce sont 2 tableaux donc on peut les concatener
        i += 1
     
    return CreerNRI(listeNomAuteurs, items, CreerItemsetsIndex(IDAuthors, itemsets, index), CreerGrapheIndex(IDAuthors, grapheCoauteurs, index))


def CreerCitations() :
    """
    Crée la structure NRI du graphe des citations (entre auteurs).
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    itemsets = dict()
    index = dict()

    IDAuthors = ImportFromJSONStruc("../Data/JSON_struct/Authors.json")
    IDField = ImportFromJSONStruc("../Data/JSON_struct/Fields.json")
    
    citations = ImportFromJSONStruc("../Data/JSON_struct/Citation.json")

    authorToField = ImportFromJSONStruc("../Data/JSON_struct/AuthorToField.json")
    authorToYear = ImportFromJSONStruc("../Data/JSON_struct/AuthorToYear.json")

    nomAuteurs = ImportFromJSONStruc("../Data/JSON_struct/IDToAuthor.json")
    nomField = ImportFromJSONStruc("../Data/JSON_struct/IDToField.json")

    years = ListerAnnees(authorToYear)
    fields = ListerAttributs(authorToField)
    items = years + fields
    
    listeNomAuteurs = ListerID(IDAuthors)
    listeNomField = ListerID(IDField)

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

    return CreerNRI(listeNomAuteurs, items, CreerItemsetsIndex(IDAuthors, itemsets, index), CreerGrapheIndex(IDAuthors, citations, index))



def CreerCopublications() :
    """
    Crée la structure NRI du graphe des copublications.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    itemsets = dict()
    index = dict()

    IDPapers = ImportFromJSONStruc("../Data/JSON_struct/Papers.json")

    paperToAuthor = ImportFromJSONStruc("../Data/JSON_struct/PaperToAuthor.json")
    copublications = ImportFromJSONStruc("../Data/JSON_struct/Copublication.json")

    paperToYear = ImportFromJSONStruc("../Data/JSON_struct/PaperToYear.json")
    paperToField = ImportFromJSONStruc("../Data/JSON_struct/PaperToField.json")

    years = ListerAnnees(paperToYear)
    fields = ListerAttributs(paperToField)
    authors = ListerAttributs(paperToAuthor)

    items = authors + years + fields
    listeNomsAuteurs = ListerID(authors)
    listeNomsFields = ListerID(fields)
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

    return CreerNRI(listeIDPapers, items, CreerItemsetsIndex(IDPapers, itemsets, index), CreerGrapheIndex(IDPapers, copublications, index))


def CreerCitationsP():
    """
    Crée la structure NRI du graphe des citation (entre publications).
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    itemsets = dict()
    index = dict()

    IDPapers = ImportFromJSONStruc("../Data/JSON_struct/Papers.json")
    paperCitPaper = ImportFromJSONStruc("../Data/JSON_struct/PaperCitPaper.json")

    paperToAuthor = ImportFromJSONStruc("../Data/JSON_struct/PaperToAuthor.json")
    paperToYear = ImportFromJSONStruc("../Data/JSON_struct/PaperToYear.json")
    paperToField = ImportFromJSONStruc("../Data/JSON_struct/PaperToField.json")

    auteurs = ListerAttributs(paperToAuthor)
    fields = ListerAttributs(paperToField)
    years = ListerAnnees(paperToYear)

    items = auteurs + years + fields

    listeNomsAuteurs = ListerID(auteurs)
    listeNomsFields = ListerID(fields)
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

    return CreerNRI(listeIDPapers, items, CreerItemsetsIndex(IDPapers, itemsets, index), CreerGrapheIndex(IDPapers, paperCitPaper, index))



def CreerCooccurrences() :
    """
    Crée la structure NRI du graphe de cooccurrences.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    itemsets = dict()
    index = dict()   

    IDField = ImportFromJSONStruc("../Data/JSON_struct/Fields.json")

    coocurrence = ImportFromJSONStruc("../Data/JSON_struct/CoOccurrences.json")


    fieldToAuthor = ImportFromJSONStruc("../Data/JSON_struct/FieldToAuthors.json")
    fieldToYear = ImportFromJSONStruc("../Data/JSON_struct/FieldToYear.json")

    auteurs = ListerAttributs(fieldToAuthor)
    years = ListerAnnees(fieldToYear)

    items = auteurs + years

    listeNomAuteurs = ListerID(auteurs)
    listeNomFields = ListerID(IDField)

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
    return CreerNRI(listeNomFields, items, CreerItemsetsIndex(IDField, itemsets, index), CreerGrapheIndex(IDField, coocurrence, index))


def CreerCitationsE() :
    """
    Crée la structure NRI du graphe de citation (entre les thématiques).
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    itemsets = dict()
    index = dict()   

    IDField = ImportFromJSONStruc("../Data/JSON_struct/Fields.json")

    citationsE = ImportFromJSONStruc("../Data/JSON_struct/CitationE.json")

    fieldToAuthor = ImportFromJSONStruc("../Data/JSON_struct/FieldToAuthors.json")
    fieldToYear = ImportFromJSONStruc("../Data/JSON_struct/FieldToYear.json")

    auteurs = ListerAttributs(fieldToAuthor)
    years = ListerAnnees(fieldToYear)

    items = auteurs + years

    listeNomAuteurs = ListerID(auteurs)
    listeNomFields = ListerID(IDField)

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

    return CreerNRI(listeNomFields, items, CreerItemsetsIndex(IDField, itemsets, index), CreerGrapheIndex(IDField, citationsE, index))


def CreerPubAut() :
    """
    Crée la structure NRI du graphe bipartis entre les auteurs et leurs publications.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    itemsets = dict()
    index = dict() 


    IDAuthors = ImportFromJSONStruc("../Data/JSON_struct/Authors.json")
    IDPapers = ImportFromJSONStruc("../Data/JSON_struct/Papers.json")
    publicationsAuteurs = ImportFromJSONStruc("../Data/JSON_struct/PublicationAuteurs.json")

    #attributs
    authorToYear = ImportFromJSONStruc("../Data/JSON_struct/AuthorToYear.json")
    authorToField = ImportFromJSONStruc("../Data/JSON_struct/AuthorToField.json")
    paperToYear = ImportFromJSONStruc("../Data/JSON_struct/PaperToYear.json")
    paperToField = ImportFromJSONStruc("../Data/JSON_struct/PaperToField.json")

    aYears = ListerAnnees(authorToYear)
    pYears = ListerAnnees(paperToYear)
    aField = ListerAttributs(authorToField)
    pField = ListerAttributs(paperToField)

    fields = Union(aField, pField)

    sommets = IDPapers + IDAuthors

    listeNomAuteurs = ListerID(IDAuthors)
    listeIDPapers = ListerID(IDPapers)
    listeNomFields = ListerID(fields)

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
    return CreerNRI(NomSommets, items, CreerItemsetsIndex(sommets, itemsets, index), CreerGrapheIndex(sommets, publicationsAuteurs, index))


def CreerAutPubCitees() :
    """
    Crée la structure NRI du graphe bipartis des auteurs vers les publications qu'ils citent.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    itemsets = dict()
    index = dict() 


    IDAuthors = ImportFromJSONStruc("../Data/JSON_struct/Authors.json")
    IDPapers = ImportFromJSONStruc("../Data/JSON_struct/Papers.json")

    auteurPublicationCitees = ImportFromJSONStruc("../Data/JSON_struct/AuteurPublicationCitees.json")

    #attributs
    authorToYear = ImportFromJSONStruc("../Data/JSON_struct/AuthorToYear.json")
    authorToField = ImportFromJSONStruc("../Data/JSON_struct/AuthorToField.json")
    paperToYear = ImportFromJSONStruc("../Data/JSON_struct/PaperToYear.json")
    paperToField = ImportFromJSONStruc("../Data/JSON_struct/PaperToField.json")

    aYears = ListerAnnees(authorToYear)
    pYears = ListerAnnees(paperToYear)
    aField = ListerAttributs(authorToField)
    pField = ListerAttributs(paperToField)

    fields = Union(aField, pField)

    sommets = IDPapers + IDAuthors

    listeNomAuteurs = ListerID(IDAuthors)
    listeIDPapers = ListerID(IDPapers)
    listeNomFields = ListerID(fields)

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

    return CreerNRI(NomSommets, items, CreerItemsetsIndex(sommets, itemsets, index), CreerGrapheIndex(sommets, auteurPublicationCitees, index))


def CreerPubAutCites() :
    """
    Crée la structure NRI du graphe bipartis des publications vers les auteurs qu'elles citent.
    Prend en paramètres un graphe.
    Retourne un dictionnaire NRI avec les sommets, les items, itemsets et graphe.
    """
    itemsets = dict()
    index = dict() 


    IDAuthors = ImportFromJSONStruc("../Data/JSON_struct/Authors.json")
    IDPapers = ImportFromJSONStruc("../Data/JSON_struct/Papers.json")

    pubAuteursCites = ImportFromJSONStruc("../Data/JSON_struct/PublicationAuteurCites.json")

    #attributs
    authorToYear = ImportFromJSONStruc("../Data/JSON_struct/AuthorToYear.json")
    authorToField = ImportFromJSONStruc("../Data/JSON_struct/AuthorToField.json")
    paperToYear = ImportFromJSONStruc("../Data/JSON_struct/PaperToYear.json")
    paperToField = ImportFromJSONStruc("../Data/JSON_struct/PaperToField.json")

    aYears = ListerAnnees(authorToYear)
    pYears = ListerAnnees(paperToYear)
    aField = ListerAttributs(authorToField)
    pField = ListerAttributs(paperToField)

    fields = Union(aField, pField)

    sommets = IDPapers + IDAuthors

    listeNomAuteurs = ListerID(IDAuthors)
    listeIDPapers = ListerID(IDPapers)
    listeNomFields = ListerID(fields)

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
    return CreerNRI(NomSommets, items, CreerItemsetsIndex(sommets, itemsets, index), CreerGrapheIndex(sommets, pubAuteursCites, index))
    