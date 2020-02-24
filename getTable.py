import sys
from imp_lexer import *
from imp_parser import *

if __name__ == "__main__":
    filename = sys.argv[1]
    file = open(filename, encoding="utf-8")
    characters = file.read()
    file.close()
    tokens = imp_lex(characters)
    document = imp_prs(tokens)

    table = {}
    elems = document.getElementsByClassName("j_filter_by_fio")
    table["ID"] = []
    table["name"] = []
    table["discipline"] = []
    table["marks"] = {}
    for elem in elems:
        table["ID"].append(elem.textContent().split(". ")[0]) 
        table["name"].append(elem.textContent().split(". ")[1]) 
    elems = document.getElementsByAtributeName("data-toggle", "tooltip")
    for elem in elems:
        table["discipline"].append(elem.textContent())
    for name in table["name"]:
        elems = document.getElementsByAtributeName("title", name)
        table["marks"][name] = []
        for elem in elems:
            child = elem.getChildren()
            if len(child) > 0:
                table["marks"][name].append(child[0].atrs["value"])
            else:
                table["marks"][name].append(elem.textContent())
    print(table)