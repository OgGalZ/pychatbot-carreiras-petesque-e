import functions as fn
from api import utils

directory = "cleaned"
files_names = fn.list_of_files("speeches-20231124", "txt")
fn.display_names(files_names)
fn.cleaned("speeches-20231124")
fn.remove_punctuation_character()
for a in files_names:
    content = utils.recover_string_file(directory, a)
    print(fn.TF(content))
print(fn.idf(directory))
