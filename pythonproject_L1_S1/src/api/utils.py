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


def create_table_files_directory(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


def recover_string_file(directory, file):
    file_path = os.path.join(directory, file)
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def remove_accents(texte):
    """
     remplace les lettres accentuées d'un texte par leur équivalent sans accent.
    """
    # Dictionnaire de correspondance des accents.
    correspondances = {
        'à': 'a', 'â': 'a', 'ä': 'a',
        'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
        'î': 'i', 'ï': 'i',
        'ô': 'o', 'ö': 'o',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c',
    }
    # Remplacement des caractères accentués.
    return ''.join(correspondances.get(c, c) for c in texte)


def table_is_nul(table):
    return all(element == 0.0 for element in table)



