import functions as fn

directory = "./speeches-20231124"
files_names = fn.list_of_files(directory, "txt")
fn.cleaned(directory)
fn.remove_punctuation_character()
