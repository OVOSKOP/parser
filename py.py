import sys
from imp_lexer import *
from imp_parser import *

# def parserHTML(filename):
if __name__ == "__main__":
    filename = sys.argv[1]
    file = open(filename, encoding="utf-8")
    characters = file.read()
    file.close()
    tokens = imp_lex(characters)
    document = imp_prs(tokens)
    # for token in tokens:
        # print (token)
    # table = document.getElementsByClassName("fl_left scorestable")[0]
    # return document
    print(document)
