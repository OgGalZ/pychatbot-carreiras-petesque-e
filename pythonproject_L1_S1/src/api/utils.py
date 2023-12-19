import math
import os
import string

from pythonproject_L1_S1.src.functions import TF


def remove_digits(string):
    # supprime les chiffres
    new_string = ""
    for character in string:
        if not character.isdigit():
            new_string += character
    return new_string


def directory_exist(chemin_repertoire):
    # vérifie si un dossier existe
    return os.path.exists(chemin_repertoire) and os.path.isdir(chemin_repertoire)


def recover_names_presidents(table_files_speeches):
    # récupère le nom des présidents
    names_presidents = []
    for names in table_files_speeches:
        var = names.split("_")[1]
        final_var = var.split(".")[0]
        names_presidents.append(remove_digits(final_var))
    return names_presidents


def create_table_files_directory(directory, extension):
    # récupère le nom des fichiers txt d'un répertoire
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


def recover_string_file(directory, file):
    # récupére le string d'un file
    file_path = os.path.join(directory, file)
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def remove_accents(texte):
    """
     remplace les lettres accentuées d'un texte par leur équivalent sans accent.
    """
    # Dictionnaire de correspondance des accents.
    correspondances = {
        'à': 'a', 'â': 'a', 'ä': 'a',
        'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
        'î': 'i', 'ï': 'i',
        'ô': 'o', 'ö': 'o',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c',
    }
    # Remplacement des caractères accentués.
    return ''.join(correspondances.get(c, c) for c in texte)


def table_is_nul(table):
    # vérifie si un tableau est nul renvoie true or false
    return all(element == 0.0 for element in table)


def dict_names(name_file):
    noms = {"Chirac": "Nomination_Chirac1.txt", "Chirac": "Nomination_Chirac2.txt",
            "Giscard dEstaing": "Nomination_Giscard dEstaing.txt", "Hollande": "Nomination_Hollande.txt",
            "Macron": "Nomination_Macron.txt", "Mitterand": "Nomination_Mitterrand1.txt",
            "Mitterand": "Nomination_Mitterrand2.txt", "Sarkozy": "Nomination_Sarkozy.txt"}

    # Parcourir chaque élément du dictionnaire
    for nom, fichier in noms.items():
        # Vérifier si le nom de fichier correspond à la valeur recherchée
        if fichier == name_file:
            # Retourner le nom correspondant à la valeur
            return nom
    # Si la valeur n'est pas trouvée, retourner None ou une valeur par défaut
    return None


# 4 - Similarity Calculation
def dot_product(vector1, vector2):
    # produit scalaire
    if len(vector1) != len(vector2):
        return "Les vecteurs ne sont pas de la même longueur, on ne peut pas calculer le produit scalaire."
    summation = 0
    for i in range(len(vector1)):
        summation += vector1[i] * vector2[i]
    return summation


def vector_norm(vector):
    # calcul la norme du vecteur
    summation = 0
    for i in range(len(vector)):
        summation += (vector[i]) ** 2
    result = math.sqrt(summation)
    return result


def key_associee_a_var_max_dict(dict):
    # Fonction qui renvoie la clé associée à la plus grande valeur du dictionnnaire
    max = 0
    document = ""
    for cle, val in dict.items():
        if max < val:
            max = val
            document = cle
    return document


# Associe un nombre unique à chaque mots dans une liste de mot
def dict_string_nbr(liste):
    dict = {}
    for i in range(0, len(liste)):
        dict[liste[i]] = i
    return dict


def list_mots_uniques_corpus(directory):
    liste = []
    files = os.listdir(directory)
    for filename in files:
        if filename.endswith('.txt'):
            tf_scores = TF(recover_string_file(directory, filename))
            for mot, tf in tf_scores.items():
                if mot not in liste:
                    liste.append(mot)
    return liste


# Fonction pour créer une matrice de zéros
def matrice_0(dict1, dict2):
    M = []
    for i in range(0, len(dict1)):
        L = []
        for j in range(0, len(dict2)):
            L.append(0)
        M.append(L)
    return M


def remove_useless_tokens(tokens):
    stop_words_francais = [
        'au', 'aux', 'avec', 'ce', 'ces', 'dans', 'de', 'des', 'du', 'elle', 'en',
        'et', 'eux', 'il', 'je', 'la', 'le', 'les', 'leur', 'lui', 'ma', 'mais', 'me', 'même',
        'mes', 'moi', 'mon', 'ne', 'nos', 'notre', 'nous', 'on', 'ou', 'par', 'pas',
        'pour', 'qu', 'que', 'qui', 'sa', 'se', 'ses', 'son', 'sur', 'ta', 'te', 'tes',
        'toi', 'ton', 'tu', 'un', 'une', 'vos', 'votre', 'vous', 'c', 'd', 'j', 'l',
        'à', 'm', 'n', 's', 't', 'y', 'été', 'étée', 'étées', 'étés', 'étant', 'étante',
        'étants', 'étantes', 'suis', 'es', 'est', 'sommes', 'êtes', 'sont', 'serai',
        'seras', 'sera', 'serons', 'serez', 'seront', 'serais', 'serait', 'serions',
        'seriez', 'seraient', 'étais', 'était', 'étions', 'étiez', 'étaient', 'fus',
        'fut', 'fûmes', 'fûtes', 'furent', 'sois', 'soit', 'soyons', 'soyez', 'soient',
        'fusse', 'fusses', 'fût', 'fussions', 'fussiez', 'fussent', 'ayant', 'ayante',
        'ayantes', 'ayants', 'eu', 'eue', 'eues', 'eus', 'ai', 'as', 'avons', 'avez',
        'ont', 'aurai', 'auras', 'aura', 'aurons', 'aurez', 'auront', 'aurais', 'aurait',
        'aurions', 'auriez', 'auraient', 'avais', 'avait', 'avions', 'aviez', 'avaient',
        'eut', 'eûmes', 'eûtes', 'eurent', 'aie', 'aies', 'ait', 'ayons', 'ayez', 'aient',
        'eusse', 'eusses', 'eût', 'eussions', 'eussiez', 'eussent'
    ]
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

    stop_words_francais_question = stop_words_francais
    for i in question_starters.keys():
        stop_words_francais_question.append(i)
    words = [word for word in tokens if word not in stop_words_francais_question]
    return words


def find_common_terms(tokens, directory):
    # Obtient l'ensemble des mots uniques dans le corpus de textes
    liste_mots_uniques = list_mots_uniques_corpus(directory)

    # Liste des mots communs à la question et au corpus
    liste = []

    for mot in tokens:
        if mot in liste_mots_uniques and mot not in liste:
            liste.append(mot)
    return liste


# Fonction permettant de transformer un chaîne de caractères
# en une chaîne de caractères uniquement avec des mots en minuscule
def clean_str(ch):
    # Convertir en minuscules
    ch = ch.lower()

    # Supprimer la ponctuation
    for char in string.punctuation:
        ch = ch.replace(char, ' ')
    return ch