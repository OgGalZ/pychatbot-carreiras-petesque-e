import os
import shutil
from api import utils


def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


def dict_names(): #faire un arg avec table files speeches
    noms = {"Jacques": "Nomination_Chirac1.txt", "Jacques ": "Nomination_Chirac2.txt",
            "Valéry": "Nomination_Giscard dEstaing.txt", "François": "Nomination_Hollande.txt",
            "Emmanuel": "Nomination_Macron.txt", "François ": "Nomination_Mitterrand1.txt",
            " François ": "Nomination_Mitterrand2.txt", "Nicolas": "Nomination_Sarkozy.txt"}
    for (a, b) in noms.items():
        print("{}, {}".format(a, b))
    return noms


def display_names(table_files_speeches):
    table_names_presidents = utils.recover_names_presidents(table_files_speeches)
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
