import functions1
from api import utils
import string


def tokenize_question(question):
    content = question.lower()
    content = utils.remove_accents(content)
    for char in string.punctuation:
        content = content.replace(char, ' ')
    content = utils.remove_accents(content)
    content = utils.remove_digits(content)
    return content.split()


def search_words_in_corpus(question):
    word_list = tokenize_question(question)
    corpus_word_list = []
    matrix = functions1.calculate_tf_idf("cleaned")
    for key in matrix.keys():
        if key in word_list:
            if key not in corpus_word_list:
                corpus_word_list.append(key)
    return corpus_word_list


def vecteur_TF_IDF(question, dossier):
    liste = tokenize_question(question)
    idf = functions1.IDF(dossier)
    tf_question = {}
    for mot in liste:# Calcul du TF de chaque mot de la question
        score = 0
        for i in liste:
            if i == mot:
                score += 1
        tf_question[mot] = score / len(liste)

    print(tf_question)
    liste_tf_idf_question = []
    for mot in idf:# On créé le vecteur TF-IDF de la question
        if mot in liste:
            score = tf_question[mot] * idf[mot]
            liste_tf_idf_question.append(score)
        else:
            liste_tf_idf_question.append(0)
    return liste_tf_idf_question
