import os


def remove_digits(string):
    new_string = ""
    for character in string:
        if not character.isdigit():
            new_string += character
    return new_string


def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


def recover_names_presidents(table_files_speeches):
    names_presidents = []
    for names in table_files_speeches:
        var = names.split("_")[1]
        final_var = var.split(".")[0]
        names_presidents.append(remove_digits(final_var))
    return names_presidents


def display_names(table_names_presidents):
    new_list = []
    for names in table_names_presidents:
        if names not in new_list:
            new_list.append(names)
    print(new_list)