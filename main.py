from os import listdir, mkdir
from fonctions import *

if __name__ == "__main__":
    #Création du dossier "cleaned"
    rep = "cleaned"
    if rep not in listdir():
        mkdir(rep)

    least_important_w(rep)












