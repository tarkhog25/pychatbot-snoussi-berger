#################################################################

# Importation des modules nécessaires pour certaines fonctions
from math import log
from os import listdir


#################################################################

# Toutes les fonctions de bases
def repertoire_fichiers(r):
    """
    Fonction qui récupére tous les fichiers présents d'un certain répertoire
    :param r: chaine de caractère représentant le répertoire où les fichiers du corpus sont présent
    :return: renvoie une liste contenant les noms de chaque fichiers présent dans le répertoire r
    """
    return [f for f in listdir(f"{r}")]
    # liste en compréhension qui s'occupe de prendre chaque element du répertoire r


def exctraction_nom(f):
    """

    :param f: Fichiers sous forme de liste
    :return: renvoie les noms des présidents sous forme de liste
    """
    nom_president = []
    for fichier in f:
        president = ""
        for lettre in fichier[11:]:
            if (48 <= ord(lettre) <= 57) or (lettre == "."):
                break
            else:
                president += lettre
        if president not in nom_president:
            nom_president.append(president)
    return nom_president


def conversion_mini(f):
    """
    Fonction qui convertit le texte des fichiers en miniscules
    dans de nouveaux fichier dans le dossier cleaned
    :param f: noms des fichiers sous forme de liste
    :return: renvoie rien et créer les noueaux fichiers dans le dossier cleaned
    """
    for fichiers in f:
        with open(f"speeches/{fichiers}", "r") as fichier:
            contenu = fichier.readlines()
        fichier_new = open(f"cleaned/{fichiers}", "w")  # Creation du nouveau fichier dans le dossier 'cleaned'
        for ligne in contenu:
            fichier_new.write(ligne.lower())
        fichier_new.close()
    return None


def clean_fichier(f):
    """
    Fonction qui "clean" les fichiers afin de supprimer tous les caractéres spéciaux laissant qu'un fichier
    contenant des mots séparé par des espaces
    :param f: Nom des fichiers sous forme de list
    :return: Renvoie rien, change le contenue des fichiers
    """
    for fichiers in f:
        with open(f"cleaned/{fichiers}", "r") as fichier:
            contenu = fichier.readlines()
        fichier = open(f"cleaned/{fichiers}",
                       "w")  # Réécriture du fichier apres avoir récupérer le contenue (d'où le "w")
        for ligne in contenu:
            new_ligne = ""
            for caractere in ligne:
                if caractere in "'-":
                    new_ligne += " "
                elif caractere not in ',;!.?:"':
                    new_ligne += caractere
            fichier.write(new_ligne)
        fichier.close()

    return None


#################################################################

# La méthode TF-IDF
def occ_mots(c):
    """
    Fonction qui compte l'occurence d'un mots dans une chaine de caractere et renvoie un dictionnaire
    associant à chaque mot le nombre de fois qu’il apparait dans la chaine de caractères.
    :param c: chaine de caractères
    :return: dictionnaire {chaque mots : occurence du mots}
    """
    dic = {}
    mots = c.split()  # création d'une liste correspondant au mots de la chaine de caractères
    for i in mots:
        occ = 0
        if i not in dic.keys():  # Afin d'éviter de faire des boucles inutiles si le mots a déjà été traité
            for j in mots:
                if j == i:
                    occ += 1
            dic[i] = occ
    return dic


def idf_mots(r):
    """
    Fonction qui calclule le score IDF de chaque mot des fichiers d'un corpus
    :param r: chaine de caractère représentant le répertoire où les fichiers du corpus sont présent
    :return: un dictionnaire {mot : score IDF}
    """
    idf_dic = {}
    nb_fichiers = len(repertoire_fichiers(r))  # Récuparation du nombre de fichiers dans le répertoire r
    mots_fichier_list = mots_fichiers(r)
    for mot in mots_fichier_list:
        proportion = 0
        for liste_mots in mots_par_fichiers(r).values():
            if mot in liste_mots:
                proportion += 1
        idf_dic[mot] = log(nb_fichiers / proportion)  # Calcule de l'IDF du mots à l'aide de la fonction log
    return idf_dic


def mots_par_fichiers(r):
    """
    fonction qui récupére chaque mots d'un fichier les mettant dans une liste et les renvoyant
    sous forme d'un dic
    :param r: chaine de caractère représentant le répertoire où les fichiers du corpus sont présent
    :return: un dictionnaire {  fichier : [tous les mots du fichiers sous forme de liste] }
    """

    fichiers = repertoire_fichiers(r)
    # Récupération des noms de chaque fichiers dans le répertoire r

    dic = {}

    for fichier in fichiers:  # Pour chaque fichier dans le répertoire
        with open(f"{r}/{fichier}", "r") as f1:
            mots = []
            contenues = f1.readlines()
            for ligne in contenues:
                mots = mots + ligne.split()
            dic[fichier] = mots

    return dic


def mots_fichiers(r):
    """
    fonction qui récupére chaque mots de tous les fichiers présent dans le répertoire,
    il récupére une fois chaque mots !!
    :param r: chaine de caractère représentant le répertoire où les fichiers du corpus sont présent
    :return: une liste contenant tous les mots UNIQUES (sans doublons) présent dans tous les fichiers
    """
    fichiers = repertoire_fichiers(r)
    # Récupération des fichiers dans le répertoire r
    mots = []
    for fichier in fichiers:
        with open(f"{r}/{fichier}", "r") as f1:
            contenues = f1.readlines()
        for ligne in contenues:
            for mot in ligne.split():  # séparation de chaque mots à l'aide de la method .split()
                if mot not in mots:
                    mots.append(mot)
    return mots


def matrice_TF_IDF(r):
    """
    Fonction qui créer la matrice TF-IDF où chaque ligne représente un mot
    et chaque colonne représente un document
    :param r: chaine de caractère représentant le répertoire où les fichiers du corpus sont présent
    :return: La matrice TF-IDF.
    """
    fichiers = repertoire_fichiers(r)
    mots_idf = idf_mots(r)
    matrix = []
    for fichier in fichiers:
        with open(f"{r}/{fichier}", "r") as f1:
            contenue = f1.read()
        tf = occ_mots(contenue)
        tf_idf_fichiers = []
        for mot in mots_idf:
            if mot in tf:
                if mots_idf[mot] or tf[mot]:
                    tf_idf_fichiers.append(tf[mot] * mots_idf[mot])
                else:
                    tf_idf_fichiers.append(0.0)
            else:
                tf_idf_fichiers.append(0.0)
        matrix.append(tf_idf_fichiers)

    return transpose_matrix(matrix)  # To have the matrix which a row is a word and a column is a file


def transpose_matrix(matrix):
    """
    Function that compute the transpose of a matrix
    :param m: The matrix
    :return: The transpose of the matrix m
    """
    rows = len(matrix)
    columns = len(matrix[0])
    new_matrix = [[0 for _ in range(rows)] for _ in range(columns)]  # Creation of the new matrix with empty values
    for i in range(rows):
        for j in range(columns):
            new_matrix[j][i] = matrix[i][j]

    return new_matrix
