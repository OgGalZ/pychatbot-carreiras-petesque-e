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
                with open(file_path, 'r') as file:
                    content = file.read()
                content_lower = content.lower()
                with open(file_path, 'w') as cleaned_file:
                    cleaned_file.write(content_lower)


def remove_punctuation_character():
    name_file = "cleaned"
    if utils.directory_exist(name_file):
        files_names = utils.create_table_files_directory(name_file, ".txt")
        for files in files_names:
            file_path = os.path.join(name_file, files)
            with open(file_path, "r") as text:
                content = text.read()
                content_without_ponctuation_ = content.translate(str.maketrans("", "", string.punctuation))
            with open(file_path, 'w') as cleaned_text:
                cleaned_text.write(content_without_ponctuation_)
