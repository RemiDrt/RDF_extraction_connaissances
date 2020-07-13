#!/usr/bin/python
#coding=utf-8
if __name__ == "__main__":
    #on prend un fichier qui a les lignes avec 2 epaces d'affilés, on réecrit son contenu corrigé dans un autre fichier
    with open("../Fichier_ttl_aceKG/dump_author.ttl", encoding="utf-8") as source :
        with open("../Fichier_ttl_aceKG/dump_author2.ttl", "w", encoding="utf-8") as dest :
            for ligne in source :
                ligne_remplacement = ligne.replace("  ", " ") #on remplace les 2 espaces consécutifs par un seul espace
                dest.write(ligne_remplacement)#on ecit la nouvelle ligne qui est correct dans le nouveaux fichier
    
    with open("../Fichier_ttl_aceKG/dump_paperauthoraffiliations.ttl", encoding="utf-8") as source :
        with open("../Fichier_ttl_aceKG/dump_paperauthoraffiliations2.ttl", "w", encoding="utf-8") as dest :
            for ligne in source :
                ligne_remplacement = ligne.replace("  ", " ") #on remplace les 2 espaces consécutifs par un seul espace
                dest.write(ligne_remplacement)#on ecit la nouvelle ligne qui est correct dans le nouveaux fichier
