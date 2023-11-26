import os
import shutil
import string

from api import utils


def list_of_files(directory, extension):
    return utils.create_table_files_directory(directory, extension)


def dict_names():  # faire un arg avec table files speeches
    noms = {"Jacques": "Nomination_Chirac1.txt", "Jacques ": "Nomination_Chirac2.txt",
            "Valéry": "Nomination_Giscard dEstaing.txt", "François": "Nomination_Hollande.txt",
            "Emmanuel": "Nomination_Macron.txt", "François ": "Nomination_Mitterrand1.txt",
            " François ": "Nomination_Mitterrand2.txt", "Nicolas": "Nomination_Sarkozy.txt"}
    for (a, b) in noms.items():
        print("{}, {}".format(a, b))
    return noms


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
                with open(file_path, 'w') as cleaned_file:
                    cleaned_file.write(content_lower)


def remove_punctuation_character():
    name_file = "cleaned"
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


def IDF(repertory):
    table = utils.create_table_files_directory(repertory, ".txt")

