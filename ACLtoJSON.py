from Utilities import ExportToJSON

def ImportTSVPaperToDate(fichier) :
    paperToDate = dict()
    with open(fichier, encoding="utf-8") as f :
        line = f.readline()#sauter la ligne des tites
        line = f.readline()
        while line :
            tab = line.split("\t")
            idraw = tab[0]
            split = idraw.split("-")
            idclean = split[0] + split[1]
            paperToDate[idclean] = tab[4]
            line = f.readline()
    return paperToDate

if __name__ == "__main__":
    ExportToJSON(ImportTSVPaperToDate("Data/Graphes_attribués_NRI/acl.database.annot.tsv"), "Data/JSON_struct/ACLPaperToDate.json")