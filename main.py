from os import listdir, mkdir
from fonctions import *

#Création du dossier "cleaned"
if "cleaned" not in listdir():
    mkdir('cleaned')


matrix = matrice_TF_IDF("cleaned")

print(matrix)









