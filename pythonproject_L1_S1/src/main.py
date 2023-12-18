import features as ft
import functions1
import functions2
from api import utils

"""directory = input("Veuillez entrer le chemin du répertoire : ")
directory = "speeches-20231124"
ft.main(directory)"""

print(functions2.vecteur_TF_IDF(
    "messieurs les presidents  mesdames  mesdemoiselles  messieurs  de ce jour  de ", "cleaned"))
