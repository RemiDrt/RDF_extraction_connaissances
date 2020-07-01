from rdflib import Graph
from Utilities import *
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
