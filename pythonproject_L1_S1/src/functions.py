import os
import shutil
import string
import math
from api import utils


def list_of_files(directory, extension):
    return utils.create_table_files_directory(directory, extension)


def display_names(table_files_names):
    table_names_presidents = utils.recover_names_presidents(table_files_names)
    new_list = []
    for names in table_names_presidents:
        if names not in new_list:
            new_list.append(names)
    print(new_list)


def cleaned(directory):
    name_file = "cleaned"
    if not utils.directory_exist(name_file):
        shutil.copytree(directory, name_file)
        for filename in os.listdir(name_file):
            if filename.endswith("txt"):
                file_path = os.path.join(name_file, filename)
                content = utils.recover_string_file(directory, filename)
                content_lower = content.lower()
                content_final = utils.remove_accents(content_lower)
                with open(file_path, 'w') as cleaned_file:
                    cleaned_file.write(content_final)


def remove_punctuation_character_file(name_file):
    if utils.directory_exist(name_file):
        files_names = utils.create_table_files_directory(name_file, ".txt")
        for files in files_names:
            file_path = os.path.join(name_file, files)
            content = utils.recover_string_file(name_file, files)
            for char in string.punctuation:
                content = content.replace(char, ' ')
            with open(file_path, 'w') as cleaned_text:
                cleaned_text.write(content)
    else:
        print("use cleaned")


def TF(string_content):
    dict_tf = {}
    string_world = string_content.split()
    for word in string_world:
        if word not in dict_tf:
            dict_tf[word] = 1
        else:
            dict_tf[word] = dict_tf[word] + 1
    return dict_tf


def IDF(directory):
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
     calcule la matrice TF-IDF pour tous les fichiers d'un répertoire.
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


def tokenize_question(question):
    content = question.lower()
    content = utils.remove_accents(content)
    for char in string.punctuation:
        content = content.replace(char, ' ')
    content = utils.remove_accents(content)
    content = utils.remove_digits(content)
    return content.split()


def search_words_in_corpus(question):
    word_list = tokenize_question(question)
    corpus_word_list = []
    matrix = calculate_tf_idf("cleaned")
    for key in matrix.keys():
        if key in word_list:
            if key not in corpus_word_list:
                corpus_word_list.append(key)
    return corpus_word_list


def vecteur_TF_IDF(question, dossier):
    liste = tokenize_question(question)
    idf = IDF(dossier)
    print(idf)
    tf_question = {}
    for mot in liste:  # Calcul du TF de chaque mot de la question
        score = 0
        for i in liste:
            if i == mot:
                score += 1
        tf_question[mot] = score
    liste_tf_idf_question = []
    for mot in idf:  # On créé le vecteur TF-IDF de la question
        if mot in liste:
            score = tf_question[mot] * idf[mot]
            liste_tf_idf_question.append(score)
        else:
            liste_tf_idf_question.append(0)
    return liste_tf_idf_question


def calculate_similarity(vector1, vector2):
    dot_product_v1v2 = utils.dot_product(vector1, vector2)
    norm1 = utils.vector_norm(vector1)
    norm2 = utils.vector_norm(vector2)
    result = dot_product_v1v2 / (norm1 * norm2)
    return result


def similarity_documents_et_vectors(matrice, vector, list):
    dictionnaire = {}
    for i in range(len(matrice)):
        resultat = calculate_similarity(matrice[i], vector)
        dictionnaire[list[i]] = resultat
    return utils.key_associee_a_var_max_dict(dictionnaire)
