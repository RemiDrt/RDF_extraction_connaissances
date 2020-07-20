# RDF_extraction_connaissances

Stage au sein de LIPN<br>
Extraction de connaissances dans les graphes RDF pour la recherche d’experts<br> 
Le but est la conversion d'un graphe rdf (format turtle) au format NRI (exploitable par le LIPN) et inversement<br>

## Utilisation

Cet outil est prévu pour être utilisé avec le graphe RDF de AceKG et les graphes attribués des travaux de Mme Stella ZEVIO.<br>
Il est également capable de gérer les graphes NRI tirés de l'anthology ACL. <br>
L'utilisation de la bibliothèque RDFLib est nécessaire. Vous pouvez l'installer avec `pip install rdflib` <br>

### Convertir un fichier RDF en NRI

Dans un premier temps, il faut créer les fichiers JSON intermédiaires qui vont représenter les différentes relations du graphes RDF <br>

Dans le fichier AceKGToJSON : <br>
    -Entrer la localisation du fichier turtle à parser <br>
    -Entrer le chemin de destination des fichiers JSON <br>
    -Executer le programme <br>

Dans le fichier NRI_to_RDF : <br>
    -Si vous avez modifier le chemin de destination des fichiers JSON : <br>
        -Aller dans le fichier NRI_Creator et modifier tous les chemins qui vont chercher les fichiers JSON <br>
    -Choisir la destination des fichiers NRI <br>
    -Executer le programme <br>

### Convertir les fichiers NRI en RDF

Vous pouvez créer un fichier RDF à partir de plusieurs graphes NRI <br>
Il faut entrer le chemin des différents fichiers dans la variable `dicoFichiers` en tant que clé et la valeur doit être la relation du graphe <br>
Cet outil prend en charge les 8 graphes de recherche d'experts, il faut bien les écrire (ne pas tenir compte des majuscules): <br>
    - coauteurs <br>
    - citations <br>
    - copublications <br>
    - citationsp <br>
    - cooccurrences <br>
    - citationse <br>
    - pubaut <br>
    - autpubcitees <br>
    - pubautcites <br>

Executer le programme <br>