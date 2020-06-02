from Extractors import *

#dictionnaire d'association pour les 9 graphes de recherche d'expert
expertGraphe = dict()
expertGraphe["coauteurs"] = { "sommets" : ["aut"], "relations": "pub_communes", "attributs": ["an", "them"] }
expertGraphe["citation"] = { "sommets" : ["aut"], "relations": "citation", "attributs": ["an", "them"] }
expertGraphe["copublication"] = { "sommets" : ["pub"], "relations": "aut_commun", "attributs": ["aut", "an", "them"] }
expertGraphe["citation_p"] = { "sommets" : ["pub"], "relations": "citation", "attributs": ["aut", "an", "them"] }
expertGraphe["co_occurence"] = { "sommets" : ["them"], "relations": "pub_commune", "attributs": ["aut", "an"] }
expertGraphe["citation_e"] = { "sommets" : ["them"], "relations": "citation", "attributs": ["aut", "an"] }
expertGraphe["pub_aut"] = { "sommets" : ["pub", "aut"], "relations": "auteur", "attributs": ["an", "them"] }
expertGraphe["aut_pub_citees"] = { "sommets" : ["pub", "aut"], "relations": "citation", "attributs": ["an", "them"] }
expertGraphe["pub_aut_cites"] = { "sommets" : ["pub", "aut"], "relations": "citation", "attributs": ["an", "them"] }
print(expertGraphe)
#dictionnaire de acemap pour répertorier les différents types et prédicats qui nous interesse
acemap = dict()
acemap["coauteurs"]
acemap["citations"]
acemap["copublication"]
acemap["citations_p"]
acemap["co_ocurrence"]
acemap["citation_e"]
acemap["pub_aut"]
acemap["aut_pub_citees"]
acemap["pub_aut_cites"]
acemap["types"] = { "aut" : "ace:Author", "pub" : "ace:Paper", "an" : "xsd:date", "them" : "ace:Field" }
acemap["uri"] = { "ace" : "http://www.semanticweb.org/acemap#"}

ace = Namespace(acemap["uri"]["ace"])

def ExtraireAuteurs(graphe) :
    """
    Extrait les identifiants des auteurs des auteurs de acemap
    retourne un liste de tous les identifiants
    """

    auteurs = dict()
    auteurs = graphe.subjects(RDF.type, ace.Author)
    for auteur in auteurs :
        objet = graphe.objects(auteur, ace.author_name)
        id = auteur.split("#")[1]
        auteurs[id] = objet

