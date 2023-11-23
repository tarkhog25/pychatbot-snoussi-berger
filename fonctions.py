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
    for mot in mots_fichiers(r):
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
        tf = tf_fichiers(r)[fichier]
        tf_idf_fichiers = []
        for mot in mots_idf:
            if mot in tf:
                if mots_idf[mot] or tf[mot]:
                    tf_idf_fichiers.append(tf[mot] * mots_idf[mot] )
                else:
                    tf_idf_fichiers.append(0.0)
            else:
                tf_idf_fichiers.append(0.0)
        matrix.append(tf_idf_fichiers)
    return matrix


def tf_fichiers(r):
    """
    Fonction qui calcule l'idf de chaque mot dans chaque fichiers
    :param r: chaine de caractère représentant le répertoire où les fichiers du corpus sont présent
    :return: dictionnaire { fichier : { mot : tf } }
    """
    dic = {}
    mot_par_fichiers_dic = mots_par_fichiers(r)
    for fichier in mot_par_fichiers_dic:
        dic_mot_tf = {}
        for mot in mot_par_fichiers_dic[fichier]:
            occ = 0
            if mot not in dic_mot_tf: #Afin de ne recalculer l'occ d'un mot déjà calculer et gagner en optimisation
                for mot2 in mot_par_fichiers_dic[fichier]:
                    if mot == mot2:
                        occ += 1
                dic_mot_tf[mot] = occ
        dic[fichier] = dic_mot_tf

    return dic


def least_important_w(r):
    """
    Display the list of least important words in the document corpus
    :param r: Directory of the document corpus
    :return: None
    """
    list_least_imp = []
    dic_idf_mot = idf_mots(r)
    for mot in dic_idf_mot:
        if dic_idf_mot[mot] == 0.0 :
            list_least_imp.append(mot)
    dic_tf_files = tf_fichiers(r)
    for file in dic_tf_files :
        for word in dic_tf_files[file]:
            if word not in list_least_imp and dic_tf_files[file][word] == 0.0 :
                list_least_imp.append(word)

    print(list_least_imp)








