#!/usr/bin/python
#coding=utf-8
#import des fonctions d'extractions spécifiques aux fichier NRI
from Extractors import *
from tkinter import filedialog
from tkinter import *
import os
repCourant = os.getcwd()
root = Tk()
root.filename = filedialog.askopenfilename(initialdir=repCourant, title = "Selectionner le fichier nri", filetypes = (("nri files","*.nri"), ("all files","*.*")))
print(root.filename)
#opening the file in read only
NRI_File = open(root.filename, encoding="utf-8")
#creer une liste avec toutes les lignes
texte = NRI_File.readlines()
#fermer le fichier pour éviter les problèmes
NRI_File.close()
nri = NRI(texte)
AfficherNRI(nri)
