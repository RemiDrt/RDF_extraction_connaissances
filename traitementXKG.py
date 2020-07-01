#!/usr/bin/python
#coding=utf-8
from rdflib import Graph, RDF
from Extractors import ace, ExtraireAuteurs, ExtraireConceptes, ExtrairePublications
if __name__ == "__main__":
    graphe = Graph()
    print("parsing de XKG")
    graphe.parse(location = "XKG_sample/schema.ttl", format = "turtle")
    graphe.parse(location = "XKG_sample/sample_author.ttl", format = "turtle")
    graphe.parse(location = "XKG_sample/sample_field.ttl", format = "turtle")
    graphe.parse(location = "XKG_sample/sample_paper.ttl", format = "turtle")
    graphe.parse(location = "XKG_sample/sample_relation.ttl", format = "turtle")
    graphe.parse(location = "XKG_sample/sample_institute.ttl", format = "turtle")
    graphe.parse(location = "XKG_sample/sample_venue.ttl", format = "turtle")
    print("parsing terminé !")
    auteurs = ExtraireAuteurs(graphe)
    papers = ExtrairePublications(graphe)
    fields = ExtraireConceptes(graphe)
    #traitement préléminaire (ajout des données manquantes)
    #on va procéder par predicat grace a la methode subject_objects(predicate) de rdflib
    print("traitement des données ")
    for suj, obj in graphe.subject_objects(ace.paper_cit_paper) :
        if not suj in papers :
            papers.append(suj)
            graphe.add((suj, RDF.type, ace.Paper))
        if not obj in papers :
            papers.append(obj)
            graphe.add((obj, RDF.type, ace.Paper))

    for suj, obj in graphe.subject_objects(ace.paper_publish_date) :
        if not suj in papers :
            papers.append(suj)
            graphe.add((suj, RDF.type, ace.Paper))

    for suj, obj in graphe.subject_objects(ace.paper_title) :
        if not suj in papers :
            papers.append(suj)
            graphe.add((suj, RDF.type, ace.Paper))

    for suj, obj in graphe.subject_objects(ace.paper_is_written_by) :
        if not suj in papers :
            papers.append(suj)
            graphe.add((suj, RDF.type, ace.Paper))
        if not obj in auteurs :
            auteurs.append(obj)
            graphe.add((obj, RDF.type, ace.Author))

    for suj, obj in graphe.subject_objects(ace.paper_is_in_field) :
        if not suj in papers :
            papers.append(suj)
            graphe.add((suj, RDF.type, ace.Paper))
        if not obj in fields :
            fields.append(obj)
            graphe.add((obj, RDF.type, ace.Field))

    for suj, obj in graphe.subject_objects(ace.author_name) :
        if not suj in auteurs :
            auteurs.append(suj)
            graphe.add((suj, RDF.type, ace.Author))
    
    for suj, obj in graphe.subject_objects(ace.author_is_in_field) :
        if not suj in auteurs :
            auteurs.append(suj)
            graphe.add((suj, RDF.type, ace.Author))
        if not obj in fields :
            fields.append(obj)
            graphe.add((obj, RDF.type, ace.Field))

    for suj, obj in graphe.subject_objects(ace.field_name) :
        if not suj in fields :
            fields.append(suj)
            graphe.add((suj, RDF.type, ace.Field))

    print("traitement terminé !")
    ##création du tout dans 1 seul fichier
    print("creation du fichier sample propre !")
    graphe.bind("XKG", ace)
    graphe.serialize(destination="XKG_sample/sample_ace.ttl", format="turtle", encoding="utf-8")
    print("fichier créé")

