from Extractors import *


graphe = Graph()
##bloc pour de selection des fichier a upload dans le graphe graphe.parse(file, format)
"""
graphe.parse(location = "TTLFiles/acemap.ttl", format = "turtle")
graphe.parse(location = "TTLFiles/affiliation.ttl", format = "turtle")
graphe.parse(location = "TTLFiles/author.ttl", format = "turtle")
graphe.parse(location = "TTLFiles/conference.ttl", format = "turtle")
graphe.parse(location = "TTLFiles/field.ttl", format = "turtle")
graphe.parse(location = "TTLFiles/institute.ttl", format = "turtle")
graphe.parse(location = "TTLFiles/journal.ttl", format = "turtle")
graphe.parse(location = "TTLFiles/paper.ttl", format = "turtle")
"""


graphe = Graph()
auteur1 = URIRef("http://www.semanticweb.org/acemap#001")
auteur2 = URIRef("http://www.semanticweb.org/acemap#002")
auteur3 = URIRef("http://www.semanticweb.org/acemap#003")
paper1 = URIRef("http://www.semanticweb.org/acemap#010")
paper2 = URIRef("http://www.semanticweb.org/acemap#020")
paper3 = URIRef("http://www.semanticweb.org/acemap#030")
field1 = URIRef("http://www.semanticweb.org/acemap#100")
field2 = URIRef("http://www.semanticweb.org/acemap#200")
graphe.add((auteur1, RDF.type, ace.Author))
graphe.add((auteur2, RDF.type, ace.Author))
graphe.add((auteur3, RDF.type, ace.Author))
graphe.add((paper1, RDF.type, ace.Paper))
graphe.add((paper2, RDF.type, ace.Paper))
graphe.add((paper3, RDF.type, ace.Paper))
graphe.add((field1, RDF.type, ace.Field))
graphe.add((field2, RDF.type, ace.Field))
graphe.add((auteur1, ace.author_name, Literal("Remi DURET", datatype=XSD.string)))
graphe.add((auteur2, ace.author_name, Literal("Waris RADJI", datatype=XSD.string)))
graphe.add((auteur3, ace.author_name, Literal("Colin ESPINAS", datatype=XSD.string)))
graphe.add((field1, ace.field_name, Literal("Genie Logiciel", datatype=XSD.string)))
graphe.add((field2, ace.field_name, Literal("Data Science", datatype=XSD.string)))
graphe.add((paper1, ace.paper_title, Literal("Optisimation des applications de bureau", datatype=XSD.string)))
graphe.add((paper2, ace.paper_title, Literal("Les algorithmes de data mining", datatype=XSD.string)))
graphe.add((paper3, ace.paper_title, Literal("Faire un framework complet", datatype=XSD.string)))
graphe.add((auteur1, ace.author_is_in_field, field1))
graphe.add((auteur2, ace.author_is_in_field, field1))
graphe.add((auteur2, ace.author_is_in_field, field2))
graphe.add((auteur3, ace.author_is_in_field, field1))
graphe.add((auteur3, ace.author_is_in_field, field2))
graphe.add((paper1, ace.paper_is_in_field, field1))
graphe.add((paper2, ace.paper_is_in_field, field1))
graphe.add((paper2, ace.paper_is_in_field, field2))
graphe.add((paper3, ace.paper_is_in_field, field1))
graphe.add((paper3, ace.paper_is_in_field, field2))
graphe.add((paper1, ace.paper_is_written_by, auteur1))
graphe.add((paper2, ace.paper_is_written_by, auteur2))
graphe.add((paper2, ace.paper_is_written_by, auteur3))
graphe.add((paper3, ace.paper_is_written_by, auteur3))
graphe.add((paper2, ace.paper_cit_paper, paper1))
graphe.add((paper3, ace.paper_cit_paper, paper1))
graphe.add((paper3, ace.paper_cit_paper, paper2))
graphe.add((paper1, ace.paper_publish_date, Literal("2015-03-26", datatype=XSD.date)))
graphe.add((paper2, ace.paper_publish_date, Literal("2018-05-12", datatype=XSD.date)))
graphe.add((paper3, ace.paper_publish_date, Literal("2020-02-07", datatype=XSD.date)))
#Selection du graphe à produire :

NRI = CreerAutPubCitees(graphe)
print(NRI)


print("done !\n----------------------------")





