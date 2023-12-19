import os
import shutil
import string
import math
from api import utils


def list_of_files(directory, extension):
    """
    Récupère la liste des fichiers dans le répertoire avec une certaine extension.

    :param directory: Le chemin du répertoire.
    :param extension: L'extension des fichiers à rechercher.
    :return: Liste des noms de fichiers avec l'extension spécifiée.
    """
    return utils.create_table_files_directory(directory, extension)


def display_names(table_files_names):
    """
    Affiche la liste unique des noms extraits des fichiers.

    :param table_files_names: Liste des noms extraits des fichiers.
    """
    table_names_presidents = utils.recover_names_presidents(table_files_names)
    new_list = []
    for names in table_names_presidents:
        if names not in new_list:
            new_list.append(names)
    print(new_list)


def cleaned(directory):
    """
    Copie le contenu du répertoire spécifié dans un nouveau répertoire nommé "cleaned".
    Les fichiers texte dans le nouveau répertoire sont convertis en minuscules et dépourvus d'accents.

    :param directory: Le chemin du répertoire source.
    """
    name_file = "cleaned"
    if not utils.directory_exist(name_file):
        # Crée le répertoire "cleaned" s'il n'existe pas.
        shutil.copytree(directory, name_file)
        for filename in os.listdir(name_file):
            if filename.endswith("txt"):
                file_path = os.path.join(name_file, filename)
                content = utils.recover_string_file(directory, filename)
                # Conversion en minuscules.
                content_lower = content.lower()
                # Suppression des accents.
                content_final = utils.remove_accents(content_lower)
                with open(file_path, 'w') as cleaned_file:
                    cleaned_file.write(content_final)


def remove_punctuation_character_file(name_file):
    """
    Supprime les caractères de ponctuation des fichiers texte dans le répertoire spécifié.

    :param name_file: Le nom du répertoire contenant les fichiers texte.
    """
    if utils.directory_exist(name_file):
        # Obtient la liste des noms de fichiers texte dans le répertoire.
        files_names = utils.create_table_files_directory(name_file, ".txt")
        for files in files_names:
            file_path = os.path.join(name_file, files)
            content = utils.recover_string_file(name_file, files)
            # Remplace chaque caractère de ponctuation par un espace.
            for char in string.punctuation:
                content = content.replace(char, ' ')
            with open(file_path, 'w') as cleaned_text:
                cleaned_text.write(content)
    else:
        print("Le répertoire spécifié n'existe pas. Utilisez la fonction 'cleaned' d'abord.")


def TF(string_content):
    """
    Calcule la fréquence des termes (TF) d'une chaîne de caractères.

    :param string_content: La chaîne de caractères à traiter.
    :return: Un dictionnaire contenant la fréquence des termes.
    """
    dict_tf = {}
    string_world = string_content.split()
    for word in string_world:
        if word not in dict_tf:
            dict_tf[word] = 1
        else:
            dict_tf[word] = dict_tf[word] + 1
    return dict_tf


# Fonction pour calculer le TF pour chaque fichier dans un répertoire
def tffile(directory):
    file_list = list_of_files(directory, '.txt')
    dict_tf = {}
    for files in file_list:
        file_path = os.path.join(directory, files)
        with open(file_path, "r") as text:
            content = text.read()
            n = TF(content)
            dict_tf[files] = n
    return dict_tf


def IDF(directory):
    """
    Calcule le score IDF (Inverse Document Frequency) pour chaque terme dans un répertoire de fichiers.

    :param directory: Le répertoire contenant les fichiers.
    :return: Un dictionnaire contenant le score IDF pour chaque terme.
    """
    file_list = utils.create_table_files_directory(directory, '.txt')
    document_frequency = {}
    total_documents = len(file_list)

    for file_name in file_list:
        content = utils.recover_string_file(directory, file_name)
        unique_words = set(content.split())
        for word in unique_words:
            if word in document_frequency:
                document_frequency[word] += 1
            else:
                document_frequency[word] = 1

    idf_scores = {}
    for word in document_frequency:
        idf_scores[word] = math.log10(total_documents / (document_frequency.get(word)))

    return idf_scores


def calculate_tf_idf(directory):
    """
    Calcule la matrice TF-IDF pour tous les fichiers d'un répertoire.

    :param directory: Le répertoire contenant les fichiers.
    :return: Un dictionnaire contenant la matrice TF-IDF.
    """
    # Dictionnaire pour la matrice TF-IDF.
    tf_idf_matrice = {}
    # Calcul des scores IDF.
    idf_scores = IDF(directory)
    # Liste des fichiers.
    files = os.listdir(directory)
    for filename in files:
        if filename.endswith('.txt'):
            # Calcul des scores TF pour le fichier actuel.
            tf_scores = TF(utils.recover_string_file(directory, filename))
            for mot, tf in tf_scores.items():
                # Calcul du score TF-IDF.
                tf_idf = tf * idf_scores[mot]
                if mot in tf_idf_matrice:
                    tf_idf_matrice[mot].append(tf_idf)
                else:
                    tf_idf_matrice[mot] = [tf_idf]

    return tf_idf_matrice


# Fonction pour tokenizer une question
def tokenize_question(question):
    """
    Tokenize une question en la normalisant.

    :param question: La question à tokeniser.
    :return: Une liste de mots après le traitement.
    """
    content = question.lower()
    content = utils.remove_accents(content)
    for char in string.punctuation:
        content = content.replace(char, ' ')
    content = utils.remove_accents(content)
    content = utils.remove_digits(content)
    return content.split()


def search_words_in_corpus(question):
    """
    Recherche les mots de la question dans le corpus après la tokenisation.

    :param question: La question à traiter.
    :return: Une liste des mots de la question présents dans le corpus.
    """
    word_list = tokenize_question(question)
    corpus_word_list = []
    matrix = calculate_tf_idf("cleaned")
    for key in matrix.keys():
        if key in word_list:
            if key not in corpus_word_list:
                corpus_word_list.append(key)
    return corpus_word_list


# Fonction mettant le tf des mots peu importants à 0
def remove_useless_words(liste_common_terms, dict_words):
    for mot in dict_words.keys():
        if mot not in liste_common_terms:
            dict_words[mot] = 0
    return dict_words


# Fonction qui crée une matrice représentant le vecteur de la question
def f_vecteurs_question(dict_mots, dict_tf_idf, matrice):
    for mot, num_colonne in dict_mots.items():
        if mot in dict_tf_idf["question"].keys():
            for i in range(len(matrice)):
                matrice[i][num_colonne] = dict_tf_idf["question"][mot]
    return matrice


# Fonction qui fait le calcule du produit scalaire entre le vecteur d'un texte et le vecteur d'une question
def produit_scalaire(tf_idf_txt, tf_idf_question):
    produit_scalaire_txt_question = 0
    for i in range(len(tf_idf_txt)):
        produit_scalaire_txt_question += tf_idf_txt[i] * tf_idf_question[i]
    return produit_scalaire_txt_question


# Fonction créant un dictionnaire avec les produits scalaires
def dict_prod_scal(tf_idf_txts, tf_idf_question, dict_txt):
    dict_produit_scalaire = {}
    for txt, i in dict_txt.items():
        dict_produit_scalaire[txt] = produit_scalaire(tf_idf_txts[i], tf_idf_question[0])
    return dict_produit_scalaire


# Fonction calculant la norme d'un vecteur
def norme_vect(tf_idf_liste):
    norme_vecteur = 0
    for i in range(len(tf_idf_liste)):
        norme_vecteur += tf_idf_liste[i] ** 2
    return math.sqrt(norme_vecteur)


# Fonction calculant la similarité de la question avec les textes
def calcul_similarite(tf_idf_txts, tf_idf_question, dict_txt):
    dict_produit_scalaire = dict_prod_scal(tf_idf_txts, tf_idf_question, dict_txt)
    dict_simil = {}
    for txt in dict_produit_scalaire.keys():
        if (norme_vect(tf_idf_txts[dict_txt[txt]]) * norme_vect(tf_idf_question[0])) != 0:
            dict_simil[txt] = dict_produit_scalaire[txt] / (
                    norme_vect(tf_idf_txts[dict_txt[txt]]) * norme_vect(tf_idf_question[0]))
    return dict_produit_scalaire


# Fonction retournant la clef de la valeur la plus grande dans un dictionnaire avec des entiers en valeur.
def keys_max(dict):
    maximum = float('-inf')  # Initialiser à moins l'infini pour assurer que tout nombre sera plus grand
    txt_max = ''
    for txt, valeur in dict.items():
        if valeur > maximum:
            maximum = valeur
            txt_max = txt
    return txt_max


# Fonction retournant le texte avec le plus de similarité avec la question
def sim_max(tf_idf_txts, tf_idf_question, dict_txt):
    dict_sim = calcul_similarite(tf_idf_txts, tf_idf_question, dict_txt)
    return keys_max(dict_sim)


# Fonction tranformant la première lettre d'un mot en majuscule
def capitalize_first_letter(word):
    if len(word) > 0:
        return word[0].upper() + word[1:]
    else:
        return word


# Fonction trouvant la phrase contenat le mot avec le tf-idf le plus élevé
def trouver_phrase_reponse(mot, directory):
    # Renvoie la première phrase dans le document qui contient le mot donné.
    with open(directory, 'r', encoding='utf-8') as file:
        document = file.read()
    phrases = document.split('.')
    mot_maj = capitalize_first_letter(mot)
    for phrase in phrases:
        if mot in phrase:
            return phrase.strip()
        elif mot_maj in phrase:
            return phrase.strip()


# Fonction formulant la question
def phrase_reponse(question_type, fin_reponse):
    question_starters = {
        "comment": "Après analyse, ",
        "pourquoi": "Car, ",
        "peux": "Oui, bien sûr, ",
        "quand": "À ce moment-là, ",
        "ou": "Là où cela se passe, ",
        "quoi": "En fait, ",
        "qui": "En ce qui concerne la personne en question, ",
        "combien": "En quantité, ",
        "est": "Assurément, ",
        "pouvez": "Bien entendu, ",
        "quelle": "La réponse à cette question est : ",
        "explique": "Permettez-moi de vous expliquer que ",
        "décris": "Permettez-moi de vous décrire que ",
        "imagine": "Imaginez que ",
        "prevois": "Si l'on prévoit, ",
        "raconte": "Permettez-moi de vous raconter que ",
        "partage": "Permettez-moi de partager que ",
        "resume": "En résumé, ",
    }

    generic_response = "Voici la réponse à votre question. "
    response_type = ''
    if question_type in question_starters.keys():
        response_type = question_starters[question_type]
        if 65 <= ord(fin_reponse[0]) <= 90:
            fin_reponse = chr(ord(fin_reponse[0]) + 32) + fin_reponse[1:]
    return generic_response + '\n' + response_type + str(fin_reponse) + '.'


def matrice_TF_IDF(dict_txt, dict_mots, dict_tf_idf, matrice):
    """
    Remplit une matrice avec les valeurs TF-IDF des termes dans chaque document.
    """
    for nom_fichier, num_ligne in dict_txt.items():
        for mot, num_colonne in dict_mots.items():
            if nom_fichier in dict_tf_idf and mot in dict_tf_idf[nom_fichier]:
                matrice[num_ligne][num_colonne] = dict_tf_idf[nom_fichier][mot]
    return matrice



def tf_idf(dict_tf, idf):
    """
    Calcule le produit TF-IDF pour chaque terme dans un dictionnaire de TF (term frequency).
    """
    for document_tf in dict_tf.values():
        for term, tf in document_tf.items():
            if term in idf:
                document_tf[term] *= idf[term]
            else:
                # Si le terme n'a pas d'IDF, on le met à zéro.
                document_tf[term] = 0
    return dict_tf
