import sys
from imp_lexer import *
from imp_parser import *

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename, encoding="utf-8")
    characters = file.read()
    file.close()
    tokens = imp_lex(characters)
    document = imp_prs(tokens)
    # for token in tokens:
        # print (token)
    qwe = document.getElementById("qwe")
    print(qwe)
