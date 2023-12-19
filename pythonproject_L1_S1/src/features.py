#Chatbot - Enzo C et Enzo P -Les fonctionnalités du projet

import functions as fn
from api import utils
from pythonproject_L1_S1.src.api.utils import remove_accents, clean_str, matrice_0, dict_string_nbr, \
    list_mots_uniques_corpus


def main(directory):
    files_names = fn.list_of_files(directory, '.txt')
    fn.display_names(files_names)
    fn.cleaned(directory)
    repertory = "cleaned"
    fn.remove_punctuation_character_file(repertory)
    print("1. Afficher les mots moins importants")
    print("2. Afficher les mots avec le plus grand TF-IDF")
    print("3. Afficher les mots les plus fréquents dans les discours de Chirac")
    print("4. Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété "
          "le plus defois")
    print("5. Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé du climat et/ou de l’écologie")
    print("6. Chatbot")
    print("0. Quitter")
    choice = input("Choisissez une option (0-6): ")

    if choice == "1":
        result = display_world_less_important(repertory)
        print("Mots moins importants:", result)

    elif choice == "2":
        result = words_most_repeated_chirac()
        print("Mots avec le plus grand TF-IDF:", result)

    elif choice == "3":
        result = words_most_repeated_chirac()
        print("Mots les plus fréquents dans les discours de Chirac:", result)

    elif choice == "4":
        presidents_nation(repertory)

    elif choice == "5":
        climate(repertory)
    elif choice == "6":
        chatbot()
    elif choice == "0":
        print("Au revoir!")
    else:
        print("Choix invalide. Veuillez choisir une option de 0 à 7.")


def display_world_less_important(directory):
    """
    Affiche les mots moins importants dans la matrice TF-IDF pour un répertoire donné.

    :param directory: Répertoire des fichiers source
    :return: Liste des mots moins importants
    """
    world_less_important = []
    dict_matrice = fn.calculate_tf_idf(directory)
    for key in dict_matrice.keys():
        value = dict_matrice[key]
        if utils.table_is_nul(value):
            world_less_important.append(key)
    return world_less_important


def display_worlds_more_tfidf(directory):
    """
    Affiche les mots ayant le plus grand score TF-IDF dans la matrice pour un répertoire donné.

    :param directory: Répertoire des fichiers source
    :return: Liste des mots avec le plus grand score TF-IDF
    """
    worlds_more_tfidf = []
    dict_matrice = fn.calculate_tf_idf(directory)
    value_max = max(dict_matrice.values())
    for key in dict_matrice.keys():
        if dict_matrice[key] == value_max:
            worlds_more_tfidf.append(key)
    return worlds_more_tfidf


def words_most_repeated_chirac():
    """
    Retourne la liste des mots les plus fréquents dans les fichiers "Nomination_Chirac1.txt" et "Nomination_Chirac2.txt"
    après le nettoyage.

    :return: Liste des mots les plus fréquents
    """
    words_most_repeated_chirac = []
    content_file1_chirac = utils.recover_string_file("cleaned", "Nomination_Chirac1.txt")
    content_file2_chirac = utils.recover_string_file("cleaned", "Nomination_Chirac2.txt")
    score_tf_file1 = fn.TF(content_file1_chirac)
    score_tf_file2 = fn.TF(content_file2_chirac)

    # Exclusion des mots avec un score TF-IDF nul
    score_tf_file1_without_null_tfidf = {key: value for key, value in score_tf_file1.items() if
                                         not utils.table_is_nul(fn.calculate_tf_idf("cleaned")[key])}

    score_tf_file2_without_null_tfidf = {key: value for key, value in score_tf_file2.items() if
                                         not utils.table_is_nul(fn.calculate_tf_idf("cleaned")[key])}

    # Recherche des mots ayant le score TF le plus élevé
    value_max_file1 = max(score_tf_file1_without_null_tfidf.values())
    value_max_file2 = max(score_tf_file2_without_null_tfidf.values())
    value_max = max(value_max_file1, value_max_file2)

    # Ajout des mots ayant le score TF le plus élevé à la liste
    for key in score_tf_file1:
        if score_tf_file1[key] == value_max:
            words_most_repeated_chirac.append(key)
    for key in score_tf_file2:
        if score_tf_file2[key] == value_max:
            words_most_repeated_chirac.append(key)

    return words_most_repeated_chirac


def presidents_nation(directory):
    """
    Affiche le président qui a le plus souvent utilisé le mot "nation" et le nombre de fois où ce mot a été répété.

    :param directory: Le répertoire contenant les fichiers texte des discours des présidents.
    :return: Liste des présidents ayant utilisé le mot "nation".
    """
    max_number = 1
    word = "nation"
    names_presidents = []
    content_files = fn.list_of_files(directory, ".txt")
    president_most_nation = {}

    for files in content_files:
        content = utils.recover_string_file(directory, files)
        tf = fn.TF(content)

        if word in tf:
            names_presidents.append(files)
            number_nation = tf.get(word)

            if number_nation > max_number:
                max_number = number_nation
                president_most_nation[max_number] = files

    name = president_most_nation[max(president_most_nation)]
    var = utils.dict_names(name)
    final_var = utils.remove_digits(var)

    print(
        "Le président {0} a utilisé le mot 'nation' {1} fois, ce qui en fait celui qui l’a répété le plus de fois.".format(
            final_var, max(president_most_nation)))

    print("Le(s) président(s) qui a (ont) parlé de la « Nation »:")
    return fn.display_names(names_presidents)


def climate(directory):
    """
    Affiche le président qui a le plus souvent parlé du climat et/ou de l'écologie et les présidents qui ont abordé ces thèmes.

    :param directory: Le répertoire contenant les fichiers texte des discours des présidents.
    """
    field_climate = ["climat", "écologie", "nature", "environnement", "biodiversité", "pollution", "durabilité",
                     "ressources", "développement durable", "énergie"]
    content_files = fn.list_of_files(directory, ".txt")
    presidents_climate = []

    # Initialiser les variables pour stocker le président avec la fréquence maximale
    max_frequency = 0
    most_talked_about_climate_president = None

    for files in content_files:
        # Récupérer le contenu du fichier
        content = utils.recover_string_file(directory, files)
        term_frequencies = fn.TF(content)

        total_frequency = 0
        for term in field_climate:
            if utils.dict_names(files) not in presidents_climate:
                if term in field_climate:
                    if not utils.dict_names(files) is None:
                        presidents_climate.append(utils.dict_names(files))

            term_frequency = term_frequencies.get(term, 0)
            total_frequency += term_frequency

        if total_frequency > max_frequency:
            max_frequency = total_frequency
            most_talked_about_climate_president = utils.dict_names(files)

    # Afficher le président avec la fréquence maximale
    print("Le président qui a parlé le plus du climat et/ou de l'écologie est :", most_talked_about_climate_president)
    print("Les présidents qui ont parlé du climat et/ou de l'écologie sont :", presidents_climate)


def chatbot():
    t = 0.5
    # Import des variables utilent développées dans la partie 1
    # Chemin des deux fichiers utilisés
    directory = "./speeches-20231124"
    directory2 = "./cleaned"
    # Liste des fichiers dans cleaned
    files_names_cleaned = fn.list_of_files(directory2, "txt")
    # Dictionnaire des fichiers avec un nombre unique leur étant associé allant de 0 à 7
    # pour facilité la création d'une matrice
    dict_fichier = utils.dict_string_nbr(files_names_cleaned)
    # Dictionnaire des mots uniques du corpus avec un nombre unique leur étant associé allant de 0 à nombre de mots - 1
    # pour facilité la création d'une matrice
    dict_mots_uniques_corpus = utils.dict_string_nbr(utils.list_mots_uniques_corpus(directory2))
    # Création d'une matrice avec pour dimension le nombre de textes pour les lignes et
    # le nombres de mots uniques dans le corpus pour les colonnes
    # avec que des 0 pour faciliter l'attribution des valeurs tf-idf des mots
    # qui ne sont pas dans un tetxe, c'est-à-dire avec un tf-idf de 0
    matrice0 = utils.matrice_0(dict_fichier, dict_mots_uniques_corpus)
    # Création d'un dictionnaire avec l'ensemble des tf-idf pour faciliter la création de la matrice
    dict_tf_idf = fn.tf_idf(fn.tffile(directory2), fn.IDF(directory2))
    # Création de la matrice tf-idf avec les valeurs tf-idf des mots dans les textes
    matrice_tf_idf = fn.matrice_TF_IDF(dict_fichier, dict_mots_uniques_corpus, dict_tf_idf, matrice0)

    # Saisie de la question
    question = str(input("Veuillez saisir votre question : "))
    # Tokenisation de la question
    tokens = fn.tokenize_question(question)
    tokens_usefull = utils.remove_useless_tokens(tokens)
    # Trouve les mots en communs avec les textes
    common_terms = utils.find_common_terms(tokens_usefull, directory2)
    print("Termes communs dans le corpus :", common_terms)
    # TF de la question
    question_tf = fn.remove_useless_words(common_terms, fn.TF(remove_accents(utils.clean_str(question))))
    # TF sous la forme d'un dictionnaire pour pouvoir être utiliser dans la fonction tf_idf
    question_tf_dict = {"question": question_tf}
    # TF_IDF de la question
    question_tf_idf = fn.tf_idf(question_tf_dict, fn.IDF(directory2))
    # Création d'une matrice pour le vecteur de la question
    matrice0_2 = matrice_0(dict_fichier, dict_mots_uniques_corpus)
    # Création du vecteur de la question
    vecteurs_question = fn.f_vecteurs_question(dict_mots_uniques_corpus, question_tf_idf, matrice0_2)
    # Calcul de la simlarité de la question avec les textes et recherche du texte avec le plus de similarité
    similarite_max = fn.sim_max(matrice_tf_idf, vecteurs_question, dict_fichier)
    print("Document pertinent retourné : ", similarite_max)
    # Recherche du mot avec le tf-idf le plus grand dans la question
    idf_question_max = fn.keys_max(question_tf_idf['question'])
    print("Mot ayant le TF-IDF le plus élevé :", idf_question_max)
    # Création du chemin vers le texte le plus important dans le dossier speeches
    directory_txt_important = directory + "/" + similarite_max
    # Création de la fin réponse correspondant à la phrase avec le mot ayant le plus haut tf-idf dans la question
    fin_reponse = fn.trouver_phrase_reponse(idf_question_max, directory_txt_important)
    # Création de la réponse et affichage de celle-ci
    response = fn.phrase_reponse(tokens[0], fin_reponse)
    print(response)
