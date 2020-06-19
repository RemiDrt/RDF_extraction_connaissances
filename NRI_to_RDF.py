from Extractors import *

sujets = dict()
sujets["AUTH"] = 

citations = open("CitationsP_XP4.nri", encoding="utf-8")
contenu = citations.readlines()
NRICitations = NRI(contenu)
print(NRICitations)