#################################################################

# Importation des modules nécessaires pour certaines fonctions
from math import log10, sqrt
from os import listdir
from tkinter import *
from tkinter import scrolledtext


#############################     Basic Functions     ####################################


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


def association_name(f):
    """
    Associate name of the president with their files
    :param f: All files in the repository
    :return: dictinnary {name of president : [files]}
    """
    List = exctraction_nom(f)
    L_aux = ["Emanuel", "Jack", "Valéry", "François", "Nicolas", ""]
    dic = {}

    for i in range(len(List)):
        if List[i] == "Macron":
            L_aux[0] = L_aux[0] + ' ' + List[i]

        elif List[i] == "Chirac":
            L_aux[1] = L_aux[1] + ' ' + List[i]

        elif List[i] == "Giscard dEstaing":
            L_aux[2] = L_aux[2] + ' ' + List[i]

        elif List[i] == "Sarkozy":
            L_aux[4] = L_aux[4] + ' ' + List[i]

        elif List[i] == "Hollande":
            L_aux[3] = L_aux[3] + ' ' + List[i]

        elif List[i] == "Mitterrand":
            L_aux[5] = L_aux[3] + ' ' + List[i]

    for i in L_aux:
        dic[i] = []
    for name in List:
        for file in f:
            for name_m in L_aux:
                if name in file and name in name_m:
                    dic[name_m].append(file)
    return (dic)


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
                elif caractere not in ',;!.?:"_':
                    new_ligne += caractere
            fichier.write(new_ligne)
        fichier.close()

    return None


def list_word(text):
    """
    function that takes the text of the question as a parameter, and returns the list of words that make up the question.
    :param text: string that represents a sentence and more precisely in our case the question asked
    :return: list of word that make up the sentence without any punctuation
    """
    liste = text.split()
    new_liste = []
    for word in liste:
        # If the word is not a punctuation
        if word not in "?!":
            new_word = ""
            for letter in word:
                # If there is separator like - or ' create 2 word ex: 'eux-meme' --> 'eux' and 'meme'
                if letter in "-'":
                    new_liste.append(new_word)
                    new_word = ""
                # Delete all non letter character
                elif letter not in ",.":
                    new_word += letter.lower()
            new_liste.append(new_word)
    return new_liste


def words_corpus(list_words):
    """
    Look for terms that form the intersection between the set of words
    in the corpus and the set of words in the question.
    :param list_words: list of words that make up the question without any
    punctuation (list from the return of list_words)
    :return: list that represents that are present in the document corpus
    """
    files = repertoire_fichiers("cleaned")
    words_present = []
    for word in list_words:
        check = True
        i = 0
        # Using a while with a check to not make useless loop
        while check and i < len(files):
            with open(f"cleaned/{files[i]}", "r") as f1:
                contenue = f1.readlines()
            for line in contenue:
                # Checking if the word is in the list of word of the line
                if word in line.split():
                    # If it is present stop the loop of the while and of the for
                    check = False
                    words_present.append(word)
                    break
            i += 1
    return words_present


#############################      TF_IDF Functions      ####################################


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


def idf_mots(rep):
    """
    Compute IDF of all words
    :param rep: string that is the directory
    :return: dictionnary {word : IDF}
    """
    dic = {}
    nb_doc = len(repertoire_fichiers(rep))
    for i in repertoire_fichiers(rep):
        with open(f"{rep}/{i}", 'r') as F:
            L = set(F.read().split())
        for i in L:
            if i not in dic.keys():
                dic[i] = 1
            else:
                dic[i] += 1
    for i in dic:
        dic[i] = log10(nb_doc / dic[i])
    return (dic)


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
                    tf_idf_fichiers.append(0.0)  # If idf or tf is equal to 0.0 just put a 0.0
            else:
                tf_idf_fichiers.append(0.0)  # If the word is not present just put a 0.0
        matrix.append(tf_idf_fichiers)

    return transpose_matrix(matrix)  # To have the matrix which a row is a word and a column is a file


def transpose_matrix(matrix):
    """
    Function that compute the transpose of a matrix
    :param matrix: The matrix
    :return: Transpose of the matrix
    """
    rows = len(matrix)
    columns = len(matrix[0])
    new_matrix = [[0 for i in range(rows)] for i in range(columns)]  # Creation of the new matrix with empty values
    for i in range(rows):
        for j in range(columns):
            new_matrix[j][i] = matrix[i][j]

    return new_matrix


def TF_IDF(repertory, show=False):
    '''
    Function that compute the matrix TF-IDF not as a list but as a dictionnary
    :param show: If display the matrix or not
    :param repertory: string(the path to the directory)
    :return: Dictionnary which represent the matrix {word : [TF_IDF for each file]}
    '''
    D_word_IDF = idf_mots(repertory)
    dico = {}
    for words in D_word_IDF.keys():
        dico[words] = []
    for files in repertoire_fichiers(repertory):
        with open((repertory + '/' + files), 'r') as file:
            string = file.read()
            D_word_TF = occ_mots(string)
        for words in D_word_IDF.keys():
            if words in D_word_TF.keys():
                dico[words].append(D_word_TF[words] * D_word_IDF[words])
            else:
                dico[words].append(0)
    if show:
        show_display(dico)
    return (dico)



def show_display(dic):
    '''
    function that display a dic of the form (word  :  [........]
                                             word2 :  [........]
                                             ...................)
    :param dic: a dictionary of the form (key : value .....)
    :return: none just a diplay
    '''
    maxi = max([len(i) for i in dic.keys()])
    for i in dic.keys():
        print(i, ' ' * (maxi - len(i)), ':', ' ', dic[i])


def vector(question, rep):
    """
    function that return the TF-IDF vector of the question and a dictionary of
    the words in the question associate to their index in the vector.
    :param question: string  (the question)
    :return: tuple ( list [TF-IDF vector], dic {index in the list : word of the question} )
    """
    words = words_corpus(list_word(question))
    # The function "occ_mots" can be only used by giving it a string so transform the list into
    # a sentence separated by space to use correctly the function "occ_mots"
    word_into_string = ''
    for word in words:
        word_into_string += word + ' '
    frequency_words = occ_mots(word_into_string)
    idf_corpus = idf_mots(rep)
    word_index = {}  # dic --> Index in 'list_vector associate to the word'
    list_vector = []
    index = 0
    for word in idf_corpus:
        if word in frequency_words:
            list_vector.append((frequency_words[word] / len(words)) * idf_corpus[word])
            word_index[index] = word
        else:
            list_vector.append(0.0)
        index += 1
    return list_vector, word_index

#######################      Features      #########################


def higher_word(rep):
    '''
    function that display words with the highest TF-IDF
    :param rep: directory
    :return: None
    '''
    dico = TF_IDF(rep)
    dic = dico.copy()
    big = [max(i) for i in dic.values()]
    n = int(input("Enter the number of word that you want : "))
    for i in range(n):
        M = []
        for j in dic:
            if max(big) in dic[j]:
                print(j, " : ", dic[j])
                M.append(j)
        big.remove(max(big))
        for i in M:
            del dic[i]


def least_important_word(rep, recup=False, show=True):
    """
    Display the list of least important words in the document corpus
    :param rep: directory
    :param recup: if we return the list or not
    :param show: if we show the list or not
    :return: By default None, if recup is true --> return the list
    """
    list_lest_imp_word = []
    dic_idf_mots = idf_mots(rep)
    # I just need to check if idf = 0 to find if the score TF-IDF of a word is 0 in all files
    for word in dic_idf_mots:
        if dic_idf_mots[word] == 0.0:
            list_lest_imp_word.append(word)

    if show and not recup:
        print(list_lest_imp_word)
    elif show and recup:
        print(list_lest_imp_word)
        return list_lest_imp_word
    elif not show and recup:
        return list_lest_imp_word


def most_repeated_word(rep, show=False, min_letter=2):
    """
    Display the most repeated word of a prsident
    :param min_letter: The minimum of letter of words to display (by default 2)
    :param rep: directory
    :param show: Choose if only want to display the most repeated word(s) or only returning the list of them (by default)
    :return: By default : the list of the most repeated word(s) by a President ; if show True : None
    """
    least_important = least_important_word(rep, recup=True, show=False)

    president = input("Enter the name of the president : ").lower()
    files = [file.lower() for file in repertoire_fichiers(rep)]
    # Taking all name of files (in lower case to make easy the check)
    names = [name.lower() for name in exctraction_nom(files)]
    # Taking all name of president in files (in lower case to make easy the check)

    while president not in names:  # Verify if the word is present
        print("There isn't this president ")
        president = input("Enter the name of the president : ").lower()

    nb_words = int(input("How many words you want to see ? : "))  # display nb_words most repeated
    while nb_words <= 0:
        nb_words = int(input("Enter a positive non zero number : "))

    dic_occ_word = {}
    for file in files:
        if president in file:
            # Check if the name of file corresponding to the president because some president has 2 files
            with open(f"{rep}/{file}", "r") as f1:
                contenue = f1.read()
            dic_occ_word_temp = occ_mots(contenue)
            for key in dic_occ_word_temp:
                if key not in least_important:  # To exclude least important words
                    # To have a dic with all words in the 2 files and the occurence in the 2 files
                    if key in dic_occ_word:
                        dic_occ_word[key] = dic_occ_word[key] + dic_occ_word_temp[key]
                        # If the word was already in the previous file, taking the sum of the occ of both
                    else:
                        dic_occ_word[key] = dic_occ_word_temp[key]

    word_most_repeated = maxi_keys_dic(dic_occ_word)

    if show:
        print("=" * 50)
        print(f"The {nb_words} most repeated words of {president} : ", "\n")
        cpt = 1
        for word in word_most_repeated:  # To have only the nb_words most repeated words
            if len(word) >= min_letter and cpt <= nb_words:
                print(word, end=" ; ")
                cpt += 1
            elif cpt > nb_words:
                break  # No need to go further, all needed words were display
        print("\n")
        print("=" * 50)
    else:
        return word_most_repeated


def maxi_keys_dic(dic):
    """
    Function that sorting keys from the highest value to the smallest one
    :param dic: dictionnary with integer values
    :return: sorted list (from the highest to the smallest)
    """
    sorted_list = []
    new_dic = dic

    for j in range(len(new_dic)):
        maxi_val = [i for i in new_dic.values()][0]  # Récupération d'une valeur dans le dic
        maxi_key = [i for i in new_dic.keys()][0]  # Récupération d'une valeur dans le dic
        for i in new_dic:
            if new_dic[i] > maxi_val:
                maxi_val = new_dic[i]
                maxi_key = i
        sorted_list.append(maxi_key)
        del new_dic[maxi_key]

    return sorted_list


def president_word(rep):
    '''
    function that alow the user to enter a word and know all the president
    that said the word and also the president that said it the most
    :param rep: directory
    :return: none ( only display )
    '''
    List_name = association_name(repertoire_fichiers(rep))
    word = input("Enter the word that president talk about : ")
    if word.lower() in TF_IDF(rep):
        List = TF_IDF(rep)[word.lower()]
        fichiers = repertoire_fichiers(rep)
        seto = set()
        for name in List_name:
            n = 0
            for file in List_name[name]:
                n += List[fichiers.index(file)]
            List_name[name] = n

        if List == [0] * len(List):
            print("all the president in the repertory said it !")
            seto = List_name
        else:
            for i in List_name:
                if List_name[i] != 0:
                    seto.add(i)

        maximum = max(List_name.values())
        for i in seto:
            print(i, " said ", word)
            if List_name[i] == maximum:
                winner = i
        print("The president that said the most ", word, " is ", winner)
    else:
        print(f"No one talked about {word} ")


def mention_all(rep, max_occ=3, min_letter=6):
    '''
    functionlity that display all the important word that presidents said
    :param rep: repertory of files
    :param max_occ: integer of the number of maximum occurency that the user allow
    :param min_letter: integer of the minimum number of letter that the user allow
    :return:
    '''
    dic = idf_mots(rep)
    fichiers = repertoire_fichiers(rep)
    for i in dic.copy():
        if dic[i] != 0:
            del dic[i]
        else:
            dic[i] = []
    for file in fichiers:
        with open(f"cleaned/{file}", 'r') as f1:
            TF = occ_mots(f1.read())
        for i in dic:
            dic[i].append(TF[i])
    List_word = []
    for i in dic:
        valid = 0
        for j in dic[i]:
            if j >= 10:
                valid += 1
        if valid <= max_occ and len(i) >= min_letter:
            List_word.append(i)
    print("The word(s) that all presidents mention : ")
    for i in List_word:
        print(i)


def first_president(rep, nb_words=1):
    """
    Identify the first president to talk about a word
    :param nb_words: The numbers of words want to know which president said it first
    :param rep: directory
    :return: None
    """
    words = [input("The word : ") for i in range(nb_words)]
    ordered_president = ["Giscard", "Mitterrand", "Chirac", "Sarkozy", "Hollande", "Macron"]
    # List of president from the first one to the last one
    for word in words:
        word_find = False  # To check if the word was found and don't repeat useless loop
        for president in ordered_president:
            for file in repertoire_fichiers(rep):
                if president in file:
                    with open(f"{rep}/{file}", "r") as f1:
                        contenue = f1.read()
                    if word in contenue:
                        print(f"The first president who talked about '{word}' is {president}\n")
                        word_find = True
                        break
            if word_find:
                break
        if not word_find:
            print(f"No one talked about '{word}'\n")


#######################  Calculating similarity  #########################

def scalar_product(vec_a, vec_b):
    """
    function that takes as parameters two vectors A and B of the same
    dimension M (number of words in the corpus)
    and calculates and returns A.B = ∑i 𝐴i 𝐵i
    :param vec_a: List representing a vector with a dimension M
    :param vec_b: List representing another vector with a dimension M
    :return: Integer representing the sum
    """
    summ = 0
    # Considering the fact that a and b have the same dimension so no index error by going throw one
    for i in range(len(vec_a)):
        summ += vec_a[i] * vec_b[i]
    return summ


def norm_vector(vec_a):
    """
    Lenght of a vector. function takes a vector A as parameter,
    then calculates and returns the square root of
    the sum of the squares of its components. ||A||= sqrt(∑i 𝐴i^2)
    :param vec_a: List representing a vector with a dimension M
    :return: Float representing the square root of the sum
    """
    summ = 0
    # First compute the sum of the square element of the vector
    for element in vec_a:
        summ += element ** 2
    # Then compute his square root
    return sqrt(summ)


def score_similarity(vec_a, vec_b):
    """
    function that takes two vectors A and B as parameters
    and returns the result of the following score:
    Scalar product of A and B / (Norm of the vector A . Norm of the vector B)
    :param vec_a: List representing a vector with a dimension M
    :param vec_b: List representing another vector with a dimension M
    :return: Float representing the score similarity of the two vectors
    """
    # Let's take each number we need separately
    scalar_prod_a_b = scalar_product(vec_a, vec_b)
    norm_vec_a = norm_vector(vec_a)
    norm_vec_b = norm_vector(vec_b)
    return scalar_prod_a_b / (norm_vec_a * norm_vec_b)

def most_relevant_document(TF_IDF_corpus, TF_IDF_vector, name_of_files):
    '''
    function that return the ducument that has the most sens with the question
    :param TF_IDF_corpus: matrix TF-IDF of the corpus
    :param TF_IDF_vector: List of The TF-IDF vector of the question
    :param name_of_files: list of the file name
    :return: a string with the file name
    '''
    dic_word_vector = {}
    L_result = []
    for index in range(len(TF_IDF_vector)):
        if TF_IDF_vector[index] != 0:
            dic_word_vector[index] = TF_IDF_vector[index]
    for index in range(len(TF_IDF_corpus)):
        dif = 0
        for index_vector in dic_word_vector:
            if dic_word_vector[index_vector] > TF_IDF_corpus[index][index_vector]:
                dif += dic_word_vector[index_vector] - TF_IDF_corpus[index][index_vector]
            else:
                dif += TF_IDF_corpus[index][index_vector] - dic_word_vector[index_vector]
        L_result.append(dif)

    min_dif = min(L_result)
    return(name_of_files[L_result.index(min_dif)])

#######################  Menu  #########################

def menu(rep):
    """
    Propose a menu for the user
    :param rep: repository
    :return: None
    """
    while True:
        print("=" * 50)
        print("1) Matrix")
        print("2) Features")
        print("3) Exit")
        print("=" * 50)

        choice_1 = int(input("Enter a choice : "))

        if choice_1 == 1:
            print("=" * 50)
            print("1) Display The Matrix TF-IDF ")
            print("2) Display The Matrix TF-IDF word by word ")
            print("3) Back")
            print("=" * 50)

            choice_2 = int(input("Enter a choice : "))
            while not (0 < choice_2 <= 3):
                print("Invalid choice try again ")
                choice_2 = int(input("Enter a choice : "))

            if choice_2 == 1:
                print(matrice_TF_IDF(rep))
            elif choice_2 == 2:
                TF_IDF(rep, show=True)

        elif choice_1 == 2:
            print("=" * 50)
            print("1) Display The list of least important words in the document corpus ")
            print("2) Display the word(s) with the highest TD-IDF score ")
            print("3) Display the most repeated word(s) by a President ")
            print("4) Display the president that spoke about a word and the one who repeated it the most times ")
            print("5) Display the first president who talk about some words ")
            print("6) Display words that all president mention ")
            print("7) Back")
            print("=" * 50)

            choice_3 = int(input("Enter a choice : "))
            while not (0 < choice_3 <= 7):
                print("Invalid choice try again ")
                choice_3 = int(input("Enter a choice : "))

            if choice_3 == 1:
                least_important_word(rep)
            elif choice_3 == 2:
                higher_word(rep)
            elif choice_3 == 3:
                mini_letter = int(input("What is the minimum of letter of word that you want to display ? : "))
                while mini_letter <= 1:
                    print("Enter a positive value that is superior of 1 !! ")
                    mini_letter = int(input("What is the minimum of letter of word that you want to display ? : "))

                most_repeated_word(rep, min_letter=mini_letter, show=True)
            elif choice_3 == 4:
                president_word(rep)
            elif choice_3 == 5:
                nb_word = int(input("How many words you want to display ? : "))
                while nb_word <= 0:
                    print("Enter a positive non zeo value !!")
                    nb_word = int(input("How many words you want to display ? : "))

                first_president(rep, nb_words=nb_word)
            elif choice_3 == 6:
                mention_all(rep)

        elif choice_1 == 3:
            break

        else:
            print("Invalid Option. Try Again !")


def graphic_menu(rep):
    # Creation of the window
    window = Tk()

    # Personnalisation of the window
    window.title("My First Chat Bot")
    window.geometry("800x520")
    window.config(background='#3AA79F')

    # Creation of the frame
    frame = Frame(window, bg='#3AA79F')

    # Creation of text
    texte = Label(window, text="Chose one option ", font=("Courrier", 40), bg="#3AA79F")
    texte.pack()

    def new_window_matrix():
        """
        Create a new window for the button matrix
        :return: None
        """
        window_matrix = Toplevel(window)
        window_matrix.title("Matrix")
        window_matrix.geometry("1200x620")
        window_matrix.config(background='#3AA79F')

        frame = Frame(window_matrix, bg='#3AA79F')

        new_label = Label(frame, text="Chose one option")
        new_label.grid(row=0, column=0, sticky="ew")

        # Creation of button
        button_1 = Button(frame, text="Display The Matrix TF-IDF", command=lambda: option_matrix(1, text))
        button_1.grid(row=1, column=0, sticky="ew")

        button_2 = Button(frame, text="Display The Matrix TF-IDF word by word", command=lambda: option_matrix(2, text))
        button_2.grid(row=2, column=0, sticky="ew")

        button_3 = Button(frame, text="Back", command=window_matrix.destroy)
        button_3.grid(row=3, column=0, sticky="ew")

        # Creation of text
        text = scrolledtext.ScrolledText(window_matrix, wrap=WORD, width=150, height=20)
        text.pack(side=BOTTOM, pady=20)

        frame.pack(side=TOP, pady=20)

    def new_window_features():
        """
        Create a new window for the button features
        :return: None
        """
        window_features = Toplevel(window)
        window_features.title("Features")
        window_features.geometry("1120x600")
        window_features.config(background='#3AA79F')

        frame_features3 = Frame(window_features, bg="lightblue")
        frame_features = Frame(frame_features3, bg="lightblue")

        new_label = Label(frame_features3, text="Chose one option")
        new_label.grid(row=0, column=0, sticky="ew")

        button_1 = Button(frame_features,
                          text="Display The list of least important words in the document corpus",
                          command=lambda: option_features(1, text))
        button_1.grid(row=0, column=0, sticky="ew")

        button_2 = Button(frame_features,
                          text="Display the word(s) with the highest TD-IDF score",
                          command=lambda: option_features(2, text))
        button_2.grid(row=1, column=0, sticky="ew")

        button_3 = Button(frame_features,
                          text="Display the most repeated word(s) by a President",
                          command=lambda: option_features(3, text))
        button_3.grid(row=2, column=0, sticky="ew")

        button_4 = Button(frame_features,
                          text="Display the president that spoke about a word and the one who repeated it the most times",
                          command=lambda: option_features(4, text))
        button_4.grid(row=0, column=1, sticky="ew")

        button_5 = Button(frame_features,
                          text="Display the first president who talk about some words",
                          command=lambda: option_features(5, text))
        button_5.grid(row=1, column=1, sticky="ew")

        button_6 = Button(frame_features,
                          text="Display words that all president mention",
                          command=lambda: option_features(6, text))
        button_6.grid(row=2, column=1, sticky="ew")

        button_7 = Button(frame_features3, text="Back", command=window_features.destroy)
        button_7.grid(row=2, column=0, sticky="ew")

        text = scrolledtext.ScrolledText(window_features, wrap=WORD, width=150, height=20)
        text.pack(side=BOTTOM, pady=20)

        frame_features.grid(row=1, column=0)
        frame_features3.pack(side=TOP, pady=20)

    def option_matrix(button_nb, text):
        """
        Function that display text in fuction of what was press in the matrix window
        :param text: The text where it will display what the user want
        :param button_nb: The button number (integer)
        :return: None
        """
        if button_nb == 1:
            text.delete(1.0, END)  # To delete the text that previously here
            for word in matrice_TF_IDF(rep):
                text.insert(END, str(word) + '\n')
        elif button_nb == 2:
            text.delete(1.0, END)
            dic = TF_IDF(rep)
            maxi = max([len(i) for i in dic.keys()])
            for i in dic.keys():
                texte = i + ' ' * (maxi - len(i)) + ':' + ' ' + str(dic[i])
                text.insert(END, texte + '\n')

    def option_features(button_nb, text):
        """
        Function that display text in fuction of what was press in the features window
        :param text: The text where it will display what the user want
        :param button_nb: The button number (integer)
        :return: None
        """
        if button_nb == 1:
            text.delete(1.0, END)
            text.insert(END, str(least_important_word(rep, show=False, recup=True)))
        elif button_nb == 2:
            text.delete(1.0, END)
            dic = TF_IDF(rep)
            big = [max(i) for i in dic.values()]
            n = 5  # By default, will display the 5 word with the highest TF_IDF score
            for i in range(n):
                M = []
                for j in dic:
                    if max(big) in dic[j]:
                        new_texte = j + " : " + str(dic[j])
                        text.insert(END, new_texte + '\n')
                        M.append(j)
                big.remove(max(big))
                for i in M:
                    del dic[i]

        elif button_nb == 3:
            text.delete(1.0, END)
            text.insert(END, "Not Working Yet !! (sorry) (for the graphic menu, the console menu is working perfectly)")
            # For this one i have some issues so it will not working yet (for the graphic menu, the console menu is working perfectly)

        elif button_nb == 4:
            text.delete(1.0, END)
            text.insert(END, "Not Working Yet !! (sorry) (for the graphic menu, the console menu is working perfectly)")
            # For this one i have some issues so it will not working yet (for the graphic menu, the console menu is working perfectly)

        elif button_nb == 5:
            text.delete(1.0, END)
            text.insert(END,
                        "Not Working Yet !! (sorry) (for the graphic menu, the console menu is working perfectly) ")
            # For this one i have some issues so it will not working yet (for the graphic menu, the console menu is working perfectly

        elif button_nb == 6:
            text.delete(1.0, END)
            min_letter = 6
            max_occ = 3
            dic = idf_mots(rep)
            fichiers = repertoire_fichiers(rep)
            for i in dic.copy():
                if dic[i] != 0:
                    del dic[i]
                else:
                    dic[i] = []
            for file in fichiers:
                with open(f"cleaned/{file}", 'r') as f1:
                    TF = occ_mots(f1.read())
                for i in dic:
                    dic[i].append(TF[i])
            List_word = []
            for i in dic:
                valid = 0
                for j in dic[i]:
                    if j >= 10:
                        valid += 1
                if valid <= max_occ and len(i) >= min_letter:
                    List_word.append(i)
            text.insert(END, "The word(s) that all presidents mention ( with a minimum of letter of 6) : " + "\n")
            for i in List_word:
                text.insert(END, i + '\n')

    # Creation of Button
    button_1 = Button(frame, text='Matrix', font=("Courrier", 25), bg='white', fg="#3AA79F", command=new_window_matrix)
    button_1.grid(row=0, sticky="ew", pady=2)

    button_2 = Button(frame, text='Features', font=("Courrier", 25), bg='white', fg="#3AA79F",
                      command=new_window_features)
    button_2.grid(row=1, sticky="ew", pady=2)

    button_3 = Button(frame, text='Exit', font=("Courrier", 25), bg='white', fg="#3AA79F", command=window.destroy)
    # Pour fermer la fenetre
    button_3.grid(row=2, sticky="ew", pady=2)

    frame.pack(expand=True)
    window.mainloop()
