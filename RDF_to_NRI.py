from Extractors import *

#dictionnaire d'association pour les 9 graphes de recherche d'expert
expertGraphe = dict()
expertGraphe["coauteurs"] = {"sommets" : ["auteurs"], "relation": "publication communes", "attributs": ["thématiques", "année"] }
expertGraphe["citations"] = {"sommets" : ["auteurs"], "relation": "publication communes", "attributs": ["thématiques", "année"] }
expertGraphe["copublications"] = {"sommets" : ["publications"], "relation": "publication communes", "attributs": ["thématiques", "année"] }
expertGraphe["citationsP"] = {"sommets" : ["publications"], "relation": "publication communes", "attributs": ["thématiques", "année"] }
expertGraphe["co-occurences"] = {"sommets" : ["thematiques"], "relation": "publication communes", "attributs": ["auteurs", "année"] }
expertGraphe["citationsE"] = {"sommets" : ["thematiques"], "relation": "publication communes", "attributs": ["auteurs", "année"] }
expertGraphe["pub-aut"] = {"sommets" : ["publication", "auteurs"], "relation": "publication communes", "attributs": ["thématiques", "année"] }
expertGraphe["aut-pubCitees"] = {"sommets" : ["publication", "auteurs"], "relation": "publication communes", "attributs": ["thématiques", "année"] }
expertGraphe["pub-autcites"] = {"sommets" : ["publication", "auteurs"], "relation": "publication communes", "attributs": ["thématiques", "année"] }
