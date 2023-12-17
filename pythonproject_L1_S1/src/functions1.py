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
        idf_scores[word] = math.log(total_documents / (document_frequency.get(word)))

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
