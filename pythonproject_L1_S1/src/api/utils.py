import os


def remove_digits(string):
    new_string = ""
    for character in string:
        if not character.isdigit():
            new_string += character
    return new_string


def directory_exist(chemin_repertoire):
    return os.path.exists(chemin_repertoire) and os.path.isdir(chemin_repertoire)


def recover_names_presidents(table_files_speeches):
    names_presidents = []
    for names in table_files_speeches:
        var = names.split("_")[1]
        final_var = var.split(".")[0]
        names_presidents.append(remove_digits(final_var))
    return names_presidents
