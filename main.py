from os import listdir, mkdir
from fonctions import *
from tkinter import *
from tkinter import scrolledtext

if __name__ == "__main__":
    #Création du dossier "cleaned"
    rep = "cleaned"
    if rep not in listdir():
        mkdir(rep)
        fichiers = repertoire_fichiers("speeches")
        conversion_mini(fichiers)
        clean_fichier(repertoire_fichiers(rep))

    menu_choice = int(input("Do you want a graphic menu ? or console menu ? \n0 for console menu  \n1 for graphic menu \n"))

    if menu_choice:
        graphic_menu(rep)
    else:
        menu(rep)
















