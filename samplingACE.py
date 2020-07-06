#!/usr/bin/python
#coding=utf-8
def AjouterElements(source, destination, tableau, compte, element, predicat_nom, prefixe=False) :
    """
    Fonction pour ajouter les elements necessaires de aceKG dans le fichier de sample
    prend en paramètre un fichier source, un fichier destination, un tableau représentant la liste des élements, le compte représentant le nombre d'éléments a avoir,
    l'element qui est la nature de l'element (auteur, domaine, ou publication) le predicat_nom qui est le predicat qui permet d'ajouter le nom d'un auteur et d'un domaine ou la date d'une publication
    le prefixe pour savoir si nous devons copier les prefixes de début de document.
    la fonction va parcourir le fichier source et ajouter au besoin les lignes dans le fichier de destination s'il y en a besoin, elle ajoute aussi
    les id des elements dans leur tableau
    """
    ligne = source.readline()
    i = 0 #représente le compte des éléments ajoutés au tableau
    while i < compte :
        if ligne[0] == "@" and prefixe :#c'est pour les @prefixe il faut les copier
            destination.write(ligne)
        else :#c'est une ligne basique pour analyser la ligne il faut séparer grace aux espaces
            tab = ligne.split(" ")
            tab_predicat = tab[1].split(":")
            tab_element = tab[2].split(":")
            tab_id = tab[0].split(":")
            id = tab_id[1]
            if tab_predicat[1] == "type" and tab_element[1] == element :
                #il faut copier la ligne, ajouter l'element au tableau et augmenter i (le nombre d'elements ajoutés au tableau)
                destination.write(ligne)
                tableau.append(id)
                i += 1
            elif tab_predicat[1] == predicat_nom:
                #si cest un ligne pour un nom ou une date, il faut vérifier que le nom ou la date appartient a un element déja ajouté donc que c'est dans la liste des elements
                if id in tableau :
                    destination.write(ligne)
        ligne = source.readline()
        #cette methode donnera surement lieu a un problème : le dernier auteur ajouté n'aura pas de nom

def ChercherElements(source, destination, tab_sujet, tab_objet, predicat_test) :
    """
    Fonction qui va chercher dans le fichier source les elements qui correspondent au predicat indiqué et qui sont présent dans les tableau sujet et objet pour les ajouter au fichier destination.
    Source est le fichier qui à analyser, destination le fichier dans lequel on ecrit, le tab_sujet contient la liste des sujet, tab_objet la liste des objets et predicat_test est le predicat recherché
    si une ligne contient le predicat, que sont sujet est present dans tab_sujet et son objet dans tab_objet on ajoute la ligne au fichier de destination
    """
    for ligne in source :
        if ligne[0] != "@" :
            tab = ligne.split(" ")
            tab_ids = tab[0].split(":")
            ids = tab_ids[1]
            tab_predicat = tab[1].split(":")
            predicat = tab_predicat[1]
            tab_ido = tab[2].split(":")
            ido = tab_ido[1]
            if predicat == predicat_test and ids in tab_sujet and ido in tab_objet :
                destination.write(ligne)

if __name__ == "__main__":
    auteurs = []
    domaines =  []
    publications = []
    nb_auteurs = 8000
    nb_domaines = 3000
    nb_publications = 10000
    with open("../Fichier_ttl_aceKG/sample.ttl", "w", encoding="utf-8") as dest :
        with open("../Fichier_ttl_aceKG/dump_author.ttl", encoding="utf-8") as source :
            #ajouter les auteurs et leurs noms
            AjouterElements(source, dest, auteurs, nb_auteurs, "Author", "author_name", prefixe=True)
        with open("../Fichier_ttl_aceKG/field.ttl", encoding="utf-8") as source :
            #ajouter les domaines et leurs noms
            AjouterElements(source, dest, domaines, nb_domaines, "Field", "field_name")
        with open("../Fichier_ttl_aceKG/dump_paper.ttl", encoding="utf-8") as source :
            #ajouter les publication et leur date de publi
            AjouterElements(source, dest, publications, nb_publications, "Paper", "paper_publish_date")

        with open("../Fichier_ttl_aceKG/dump_title.ttl", encoding="utf-8") as source :
            #ajouter les titres des publication
            i = 0 #compte du nombre de noms ajouter
            for ligne in source :
                if ligne[0] != "@" :
                    tab = ligne.split(" ")
                    tab_predicat = tab[1].split(":")
                    predicat = tab_predicat[1]
                    tab_id = tab[0].split(":")
                    id = tab_id[1]
                    if predicat == 'paper_title' and id in publications :
                        dest.write(ligne)
                        i += 1
                if i >= nb_publications :
                    break #si on a ajouté autant de titre qu'on a de publication on a fini sinon faut aller jusqua la fin du ficher

        with open("../Fichier_ttl_aceKG/dump_paperrelation.ttl", encoding="utf-8") as source :
            #ajout des paper_is_in field
            #dans ce cas si on est obligé de parcourir tout le fichier
            ChercherElements(source, dest, publications, domaines, "paper_is_in_field")
        
        with open("../Fichier_ttl_aceKG/dump_ref.ttl", encoding="utf-8") as source :
            #ajout des paper_cit_paper
            #dans ce cas si on est obligé de parcourir tout le fichier
            ChercherElements(source, dest, publications, publications, "paper_cit_paper")
            
        with open("../Fichier_ttl_aceKG/dump_author.ttl", encoding="utf-8") as source :
            #ajout des author is in field
            #dans ce cas si on est obligé de parcourir tout le fichier
            ChercherElements(source, dest, auteurs, domaines, "author_is_in_field")

        with open("../Fichier_ttl_aceKG/dump_paperauthoraffiliations.ttl", encoding="utf-8") as source :
            #ajout des paper_is_written_by
            #dans ce cas si on est obligé de parcourir tout le fichier
            ChercherElements(source, dest, publications, auteurs, "paper_is_written_by")



