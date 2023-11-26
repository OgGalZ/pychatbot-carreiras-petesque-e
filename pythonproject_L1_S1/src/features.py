import functions as fn
from api import utils


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
    content_file1_chirac = utils.recover_string_file("cleaned", "Nomination_Chirac1.txt")
    content_file2_chirac = utils.recover_string_file("cleaned",  "Nomination_Chirac2.txt")
    score_td_file1 = fn.TF(content_file1_chirac)
    score_td_file2 = fn.TF(content_file2_chirac)
    value_max_file1 = max(score_td_file1.values())
    value_max_file2 = max(score_td_file2.values())
    print(value_max_file1)
    print(value_max_file2)
