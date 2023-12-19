from os import listdir, mkdir
from fonctions import *
from tkinter import *
from tkinter import scrolledtext

if __name__ == "__main__":
    #Création du dossier "cleaned"
    rep = "cleaned"
    if rep not in listdir():
        mkdir(rep)
        files = files_corpus("speeches")
        conversion_mini(files)
        clean_file(files_corpus(rep))

    print("╔═══════════════════════════════════════════╗")
    print("║           𝕎𝕖𝕝𝕔𝕠𝕞𝕖 𝕥𝕠 ℂ𝕙𝕒𝕥𝔹𝕠𝕥              ║")
    print("╠═══════════════════════════════════════════╣")
    print("║            ℂ𝕙𝕠𝕠𝕤𝕖 𝕥𝕙𝕖 𝕞𝕖𝕟𝕦 𝕥𝕪𝕡𝕖           ║")
    print("║ 0)             ℂ𝕠𝕟𝕤𝕠𝕝𝕖 𝕞𝕖𝕟𝕦               ║")
    print("║ 1)             𝔾𝕣𝕒𝕡𝕙𝕚𝕔 𝕞𝕖𝕟𝕦               ║")
    print("╚═══════════════════════════════════════════╝")
    menu_choice = int(input())

    if menu_choice:
        graphic_menu(rep)
    else:
        menu(rep)
















