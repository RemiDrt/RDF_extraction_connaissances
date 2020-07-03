from NRI_Creator import *

def ConvertToNRI(destination, NRI):
    """
    Fonction qui pred en dictionnaire NRI et crée un fichier NRI associé
    Prend en paramètres un fichier de destination et un dictionnaire type d'une structure NRI
    """
    contenu = "#généré par le stagiaire\n" 

    #d'abord les sommets
    sommets = NRI['Objets']
    ln = len(sommets)
    i = 0
    while i < ln :
        if i != 0 :
            contenu += " | "
        contenu += sommets[i]
        i +=  1
    contenu += "\n"

    #ensuite les attributs
    i = 0
    attributs = NRI['Items']
    ln = len(attributs)
    while i < ln :
        if i != 0 :
            contenu += " | "
        contenu += attributs[i]
        i +=  1
    contenu += "\n"

    #ensuite l'itemsets
    i = 0
    itemsets = NRI["Itemsets"]
    keys = itemsets.keys()
    ln = len(keys)
    while i < ln :
        contenu += str(i) + " "
        tab = itemsets[i]
        lnTab = len(tab)
        j = 0
        while j < lnTab :
            if j != 0 :
                contenu += ","
            contenu += str(tab[j])
            j += 1
        contenu += "\n"
        i += 1

    contenu += "#\n"

    #enfin le graphe
    i = 0
    graphe = NRI["Graphe"]
    keys = graphe.keys()
    ln = len(keys)
    while i < ln :
        contenu += str(i) + " "
        tab = graphe[i]
        lnTab = len(tab)
        j = 0
        while j < lnTab :
            if j != 0 :
                contenu += ","
            contenu += str(tab[j])
            j += 1
        contenu += "\n"
        i += 1

    file = open(destination, "w", encoding="utf-8")
    file.write(contenu)
    file.close()



if __name__ == "__main__":
    
    ##bloc pour de selection des fichier a upload dans le graphe graphe.parse(file, format)
    """
    graphe = Graph()
    graphe.parse(location = "TTLFiles/acemap.ttl", format = "turtle")
    graphe.parse(location = "TTLFiles/affiliation.ttl", format = "turtle")
    graphe.parse(location = "TTLFiles/author.ttl", format = "turtle")
    graphe.parse(location = "TTLFiles/conference.ttl", format = "turtle")
    graphe.parse(location = "TTLFiles/field.ttl", format = "turtle")
    graphe.parse(location = "TTLFiles/institute.ttl", format = "turtle")
    graphe.parse(location = "TTLFiles/journal.ttl", format = "turtle")
    graphe.parse(location = "TTLFiles/paper.ttl", format = "turtle")
    """
    #Selection du graphe à produire :
    print("creation coauteurs")
    NRI = CreerCoauteurs()
    print("conversion NRI")
    #ConvertToNRI("NRI_generate/CoAuteurs_XP1.nri", NRI)
    ConvertToNRI("../Data/TestsSampleXKG/CoAuteurs_XP1.nri", NRI)
    print("creation Citations")
    NRI = CreerCitations()
    print("conversion NRI")
    #ConvertToNRI("NRI_generate/Citations_XP2.nri", NRI)
    ConvertToNRI("../Data/TestsSampleXKG/Citations_XP2.nri", NRI)
    print("creation copublications")
    NRI = CreerCopublications()
    print("conversion NRI")
    #ConvertToNRI("NRI_generate/Copublications_XP3.nri", NRI)
    ConvertToNRI("../Data/TestsSampleXKG/Copublications_XP3.nri", NRI)
    print("creation Citations P")
    NRI = CreerCitationsP()
    print("conversion NRI")
    #ConvertToNRI("NRI_generate/CitationsP_XP4.nri", NRI)
    ConvertToNRI("../Data/TestsSampleXKG/CitationsP_XP4.nri", NRI)
    print("creation Cooccurrences")
    NRI = CreerCooccurrences()
    print("conversion NRI")
    #ConvertToNRI("NRI_generate/Cooccurrences_XP5.nri", NRI)
    ConvertToNRI("../Data/TestsSampleXKG/Cooccurrences_XP5.nri", NRI)
    print("creation Citations E")
    NRI = CreerCitationsE()
    print("conversion NRI")
    #ConvertToNRI("NRI_generate/CitationsE_XP6.nri", NRI)
    ConvertToNRI("../Data/TestsSampleXKG/CitationsE_XP6.nri", NRI)
    print("creation Pub Aut")
    NRI = CreerPubAut()
    print("conversion NRI")
    #ConvertToNRI("NRI_generate/PubAut_bi_XP7.nri", NRI)
    ConvertToNRI("../Data/TestsSampleXKG/PubAut_bi_XP7.nri", NRI)
    print("creation Aut Pub citees")
    NRI = CreerAutPubCitees()
    print("conversion NRI")
    #ConvertToNRI("NRI_generate/AutPubCitees_bi_XP8.nri", NRI)
    ConvertToNRI("../Data/TestsSampleXKG/AutPubCitees_bi_XP8.nri", NRI)
    print("creation Pub Aut cites")
    NRI = CreerPubAutCites()
    print("conversion NRI")
    #ConvertToNRI("NRI_generate/PubAutCites_bi_XP9.nri", NRI)
    ConvertToNRI("../Data/TestsSampleXKG/PubAutCites_bi_XP9.nri", NRI)

    print("done !\n----------------------------")





