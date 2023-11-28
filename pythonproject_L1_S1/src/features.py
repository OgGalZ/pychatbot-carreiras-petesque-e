import functions as fn
from api import utils


def main(directory):
    files_names = fn.list_of_files(directory, '.txt')
    fn.display_names(files_names)
    fn.cleaned(directory)
    repertory = "cleaned"
    fn.remove_punctuation_character()
    print("1. Afficher les mots moins importants")
    print("2. Afficher les mots avec le plus grand TF-IDF")
    print("3. Afficher les mots les plus fréquents dans les discours de Chirac")
    print("4. Afficher le président ayant le plus utilisé le mot 'nation'")
    print("5. Afficher le premier président à parler du climat et/ou de l'écologie")
    print("6. Afficher tous les mots utilisés par les présidents")
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
        result = word_presidents_all(repertory)
        print("Tous les mots utilisés par les présidents:", result)

    elif choice == "0":
        print("Au revoir!")
    else:
        print("Choix invalide. Veuillez choisir une option de 0 à 6.")


def display_world_less_important(direcotry):
    world_less_important = []
    dict_matrice = fn.calculate_tf_idf(direcotry)
    for key in dict_matrice.keys():
        value = dict_matrice[key]
        if utils.table_is_nul(value):
            world_less_important.append(key)
    return world_less_important


def dispay_worlds_more_tdidf(directory):
    worlds_more_tdidf = []
    dict_matrice = fn.calculate_tf_idf(directory)
    value_max = max(dict_matrice.values())
    for key in dict_matrice.keys():
        if dict_matrice[key] == value_max:
            worlds_more_tdidf.append(key)
    return worlds_more_tdidf


def worlds_most_repeated_chirac():
    words_most_repeated_chirac = []
    content_file1_chirac = utils.recover_string_file("cleaned", "Nomination_Chirac1.txt")
    content_file2_chirac = utils.recover_string_file("cleaned", "Nomination_Chirac2.txt")
    score_td_file1 = fn.TF(content_file1_chirac)
    score_td_file2 = fn.TF(content_file2_chirac)
    value_max_file1 = max(score_td_file1.values())
    value_max_file2 = max(score_td_file2.values())
    value_max = max(value_max_file1, value_max_file2)
    for key in score_td_file1:
        if score_td_file1[key] == value_max:
            words_most_repeated_chirac.append(key)
    for key in score_td_file2:
        if score_td_file2[key] == value_max:
            words_most_repeated_chirac.append(key)
    return words_most_repeated_chirac


def presidents_nation(directory):
    max_number = 1
    world = "nation"
    names_presidents = []
    content_files = fn.list_of_files(directory, ".txt")
    president_most_nation = {}
    for files in content_files:
        content = utils.recover_string_file(directory, files)
        tf = fn.TF(content)
        if world in tf:
            names_presidents.append(files)
            number_nation = tf.get(world)
            if number_nation > max_number:
                max_number = number_nation
                president_most_nation[max_number] = files
    name = president_most_nation[max(president_most_nation)]
    var = name.split("_")[1]
    var1 = var.split(".")[0]
    final_var = utils.remove_digits(var1)

    print("Le président {0} a utilisé {1} fois le mot nation  ".format(final_var, max(president_most_nation)))
    return fn.display_names(names_presidents)


def climate(directory):
    field_climate = ["climat", "ecologie", "nature", "environnement", "biodiversite", "pollution", "durabilite",
                     "ressources", "developpement durable", "energie"]
    content_files = fn.list_of_files(directory, ".txt")

    # Initialiser les variables pour stocker le président avec la fréquence maximale
    max_frequency = 0

    for files in content_files:
        # Récupérer le contenu du fichier
        content = utils.recover_string_file(directory, files)

        term_frequencies = fn.TF(content)
        total_frequency = 0

        for term in field_climate:
            term_frequency = term_frequencies.get(term, 0)
            total_frequency += term_frequency

        if total_frequency > max_frequency:
            max_frequency = total_frequency
            max_president = files
            var1 = max_president.split(".")[0]
            var = var1.split("_")[1]

    # Afficher le président avec la fréquence maximale
    print("Le premier président à parler du climat et/ou de l'écologie est :", var)


def word_presidents_all(directory):
    content_files = fn.list_of_files(directory, ".txt")
    matrice_tfidf = fn.calculate_tf_idf(directory)
    table_word = []
    for files in content_files:
        content = utils.recover_string_file(directory, files)
        term_frequencies = fn.TF(content)
        for element in term_frequencies.keys():
            if not utils.table_is_nul(matrice_tfidf[element]):
                table_word.append(element)

    table_word_single = set(table_word)
    return table_word_single
