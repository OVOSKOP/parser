from imp_lexer import *
from prsr import *

def parserHTML(filename):
    file = open(filename, encoding="utf-8")
    characters = file.read()
    file.close()
    tokens = imp_lex(characters) #лексируем файл
    document = parser(tokens) #парсируем файл
    # for token in tokens:
        # print (token)
    return document
