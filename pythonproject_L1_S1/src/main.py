import functions as fn
from api import utils

directory = "cleaned"
files_names = fn.list_of_files(directory, "txt")

print(fn.idf(directory))
