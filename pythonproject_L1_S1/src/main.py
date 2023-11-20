from api import functions as fn
directory = "./speeches-20231114"
files_names = fn.list_of_files(directory, "txt")
table = fn.recover_names_presidents(files_names)
fn.display_names(table)
