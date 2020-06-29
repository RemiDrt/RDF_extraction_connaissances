from Extractors import *

if __name__ == "__main__":
    graphe = Graph()
    ###parsing de tout aceKG dans le graphe 
    print("parsing de aceKG en cours veuillez patienter ...")
    """
    graphe.parse(location = "sampleAceKG/acemap.ttl", format = "turtle")
    graphe.parse(location = "sampleAceKG/affiliation.ttl", format = "turtle")
    graphe.parse(location = "sampleAceKG/author.ttl", format = "turtle")
    graphe.parse(location = "sampleAceKG/conference.ttl", format = "turtle")
    graphe.parse(location = "sampleAceKG/field.ttl", format = "turtle")
    graphe.parse(location = "sampleAceKG/institute.ttl", format = "turtle")
    graphe.parse(location = "sampleAceKG/journal.ttl", format = "turtle")
    graphe.parse(location = "sampleAceKG/paper.ttl", format = "turtle")
    """

    graphe.parse(location = "XKG_sample/sample_ace.ttl", format = "turtle")

    """
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
    """
    ###
    print("parsing terminé")

    print("extraction et serialisations des données en cours ...")
    d = "JSON_struct/"
    imp = ImportFromJSONStruc

    ###Extraction des données et serialization en json
    print("Authors")
    ExportToJSON(ExtraireAuteurs(graphe), d+"Authors.json") 

    print("Papers")
    ExportToJSON(ExtrairePublications(graphe), d+"Papers.json")

    print("Fields")
    ExportToJSON(ExtraireConceptes(graphe), d+"Fields.json")

    print("IDToAuthors")
    ExportToJSON(IDToAuthor(graphe, imp(d+"Authors.json")), d+"IDToAuthor.json")

    print("IDToField")
    ExportToJSON(IDToField(graphe, imp(d+"Fields.json")), d+"IDToField.json")

    print("IDToPaper")
    ExportToJSON(IDToPaper(graphe, imp(d+"Papers.json")), d+"IDToPaper.json")

    print("AuthorToID")
    ExportToJSON(InverserDicoSimple(d+"IDToAuthor.json"), d+"AuthorToID.json")

    print("PaperToID")
    ExportToJSON(InverserDicoSimple(d+"IDToPaper.json"), d+"PaperToID.json")

    print("FieldToID")
    ExportToJSON(InverserDicoSimple(d+"IDToField.json"), d+"FieldToID.json")

    print("PaperToYear")
    ExportToJSON(PaperToYear(graphe, imp(d+"Papers.json")), d+"PaperToYear.json")

    print("PaperToField")
    ExportToJSON(PaperToField(graphe, imp(d+"Papers.json")), d+"PaperToField.json")

    print("AuthorToFields")
    ExportToJSON(AuthorToField(graphe, imp(d+"Authors.json")), d+"AuthorToField.json")

    print("AuthorToPaper")
    ExportToJSON(AuthorToPaper(graphe, imp(d+"Authors.json")), d+"AuthorToPaper.json")

    print("AuthorToYear")
    ExportToJSON(AuthorToYear(graphe, imp(d+"Authors.json"), imp(d+"AuthorToPaper.json")), d+"AuthorToYear.json")

    print("PaperToAuthor")
    ExportToJSON(PaperToAuthor(graphe, imp(d+"Papers.json")), d+"PaperToAuthor.json")

    print("PaperCitPaper")
    ExportToJSON(PaperCitPaper(graphe, imp(d+"Papers.json")), d+"PaperCitPaper.json")

    print("PaperCitAuthor")
    ExportToJSON(PaperCitAuthor(imp(d+"Papers.json"), imp(d+"PaperToAuthor.json"), imp(d+"PaperCitPaper.json")), d+"PaperCitAuthor.json")

    print("AuthorCitPaper")
    ExportToJSON(AuthorCitPaper(imp(d+"Authors.json"), imp(d+"Papers.json"), imp(d+"PaperToAuthor.json"), imp(d+"PaperCitPaper.json")), d+"AuthorCitPaper.json")

    print("FieldToPaper")
    ExportToJSON(FieldToPaper(graphe, imp(d+"Fields.json")), d+"FieldToPaper.json")

    print("FieldToAuthor")
    ExportToJSON(FieldToAuthor(graphe, imp(d+"Fields.json")), d+"FieldToAuthors.json")

    print("FieldToYear")
    ExportToJSON(FieldToYear(imp(d+"Fields.json"), imp(d+"FieldToPaper.json"), imp(d+"PaperToYear.json")), d+"FieldToYear.json")

    print("PaperCitField")
    ExportToJSON(PaperCitField(imp(d+"Papers.json"), imp(d+"PaperToField.json"), imp(d+"PaperCitPaper.json")), d+"PaperCitField.json")

    print("FieldCitPaper")
    ExportToJSON(FieldCitPaper(imp(d+"Fields.json"), imp(d+"FieldToPaper.json"), imp(d+"PaperCitPaper.json")), d+"FieldCitPaper.json")

    print("Coauteurs")
    ExportToJSON(Coauteurs(imp(d+"Authors.json"), imp(d+"PaperToAuthor.json"), imp(d+"AuthorToPaper.json")), d+"Coauteurs.json")

    print("Citation")
    ExportToJSON(Citation(imp(d+"Authors.json"), imp(d+"PaperToAuthor.json"), imp(d+"AuthorCitPaper.json")), d+"Citation.json")

    print("Copublication")
    ExportToJSON(Copublication(imp(d+"Papers.json"), imp(d+"PaperToAuthor.json"), imp(d+"AuthorToPaper.json")), d+"Copublication.json")

    print("Cooccurrences")
    ExportToJSON(CoOccurrences(imp(d+"Fields.json"), imp(d+"paperToField.json"), imp(d+"FieldToPaper.json")), d+"CoOccurrences.json")

    print("CitationE")
    ExportToJSON(CitationE(imp(d+"fields.json"), imp(d+"PaperToField.json"), imp(d+"FieldCitPaper.json")), d+"CitationE.json")

    print("PublicationsAuteurs")
    ExportToJSON(PublicationsAuteurs(imp(d+"AuthorToPaper.json"), imp(d+"PaperToAuthor.json")), d+"PublicationAuteurs.json")

    print("AuteurPublicationCitees")
    ExportToJSON(AuteurPublicationCitees(imp(d+"Papers.json"), imp(d+"AuthorCitPaper.json")), d+"AuteurPublicationCitees.json")

    print("PublicationAuteurCites")
    ExportToJSON(PublicationAuteurCites(imp(d+"Authors.json"), imp(d+"PaperCitAuthor.json")), d+"PublicationAuteurCites.json")

    print("Exportation terminée !")
