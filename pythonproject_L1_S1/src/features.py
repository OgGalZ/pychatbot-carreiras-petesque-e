import functions as fn
from api import utils


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
        result = dispay_worlds_more_tdidf(repertory)
        print("Mots avec le plus grand TF-IDF:", result)

    elif choice == "3":
        result = worlds_most_repeated_chirac()
        print("Mots les plus fréquents dans les discours de Chirac:", result)

    elif choice == "4":
        presidents_nation(repertory)

    elif choice == "5":
        climate(repertory)
    elif choice == "6":
        question = input("  Veuillez entrer votre question")
        display_answer(question, repertory, directory)
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
                                         not utils.table_is_null(fn.calculate_tf_idf("cleaned")[key])}

    score_tf_file2_without_null_tfidf = {key: value for key, value in score_tf_file2.items() if
                                         not utils.table_is_null(fn.calculate_tf_idf("cleaned")[key])}

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


def display_answer(question, dossier, dossier_origine):
    """
    Affiche une réponse à la question en fonction de son format.

    :param question: La question posée.
    :param dossier: Le répertoire contenant les fichiers texte des discours des présidents.
    :param dossier_origine: Le répertoire d'origine.
    :return: La réponse générée.
    """
    # Liste de propositions non exhaustives
    question_starters = {"Comment": "Après analyse, ",
                         "Pourquoi": "Car, ",
                         "Peux-tu": "Oui, bien sûr! "}

    reponse = fn.generate_response(question, dossier, dossier_origine)
    phrase_actuelle = ""

    for caractere in question:
        phrase_actuelle += caractere
        if phrase_actuelle in question_starters.keys():
            return question_starters[phrase_actuelle] + reponse

    return reponse
