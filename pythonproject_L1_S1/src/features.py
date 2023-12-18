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
    print("0. Quitter")
    choice = input("Choisissez une option (0-5): ")

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
    score_td_file1_without = {key: value for key, value in score_td_file1.items() if
                              not utils.table_is_nul(fn.calculate_tf_idf("cleaned")[key])}

    score_td_file2_without = {key: value for key, value in score_td_file2.items() if
                              not utils.table_is_nul(fn.calculate_tf_idf("cleaned")[key])}

    value_max_file1 = max(score_td_file1_without.values())
    value_max_file2 = max(score_td_file2_without.values())
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
    var = utils.dict_names(name)
    final_var = utils.remove_digits(var)

    print(
        "Le président {0} a utilisé {1} fois le mot nation . Il sagit de celui qui l’a répété le plus de fois ".format(
            final_var, max(president_most_nation)))
    print("Le(s) président(s) qui a (ont) parlé de la « Nation »")
    return fn.display_names(names_presidents)


def climate(directory):
    field_climate = ["climat", "ecologie", "nature", "environnement", "biodiversite", "pollution", "durabilite",
                     "ressources", "developpement durable", "energie"]
    content_files = fn.list_of_files(directory, ".txt")
    presidents_climate = []

    # Initialiser les variables pour stocker le président avec la fréquence maximale
    max_frequency = 0

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
            var = utils.dict_names(files)

    # Afficher le président avec la fréquence maximale
    print("Le  président qui à parler le plus du climat et/ou de l'écologie est :", var)
    print("Les présidents qui ont parlé le plus du climat et/ou de l'écologie sont :")
    print(presidents_climate)


def generate_response(question, directory, source_directory):
    file_list = fn.list_of_files(directory, ".txt")
    vector = fn.vecteur_TF_IDF(question, directory)
    matrix = fn.calculate_tf_idf(directory)
    document = fn.similarity_documents_et_vectors(matrix, vector, file_list)

    word_list = fn.tokenize_question(question)
    idf_values =fn.IDF(directory)
    tf_question = {}

    for word in word_list:
        score = 0
        for i in word_list:
            if i == word:
                score += 1
        tf_question[word] = score / len(word_list)

    word_dictionary = {}
    for word in idf_values:
        if word in word_list:
            word_dictionary[word] = tf_question[word] * idf_values[word]
        else:
            word_dictionary[word] = 0

    important_word = utils.key_associee_a_var_max_dict(word_dictionary)

    with open(f"{source_directory}/{document}", "r") as file:
        content = file.read()
        separators = ['.', '!', '?']
        sentences = []
        current_sentence = ""

        for character in content:
            current_sentence += character
            if character in separators:
                sentences.append(current_sentence)
                current_sentence = ""

        for sentence in sentences:
            if important_word in sentence:
                return sentence
