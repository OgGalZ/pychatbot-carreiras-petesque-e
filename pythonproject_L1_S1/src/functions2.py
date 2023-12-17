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
    return content
