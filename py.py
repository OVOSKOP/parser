##	HTML PARSER V.2.1.37
##	
##	DEVELOPER: OVOSKOP
##
##	COPYRIGHT. ALL RIGHT RESERVED.
##
##	CLASSES:
##		
##		TAG - Object of Tag
##		DOM - Document Object Model
##
##	AVAILABLE FUNCTIONS:
##
##		DOM:
##			getType() - get type of document
##				OUTPUT:
##					str - type of document
##
##			getElementById(idName)
##				INPUT:
##					idName - id value. Required.
##				OUTPUT:
##					Tag - element
##
##			getElementsByClassName(className)
##				INPUT:
##					className - class value. Required.
##				OUTPUT:
##					[] - list of elements
##
##			getElementsByTagName(tagName)
##				INPUT:
##					tagName - tag name. Required.
##				OUTPUT:
##					[] - list of elements
##
##			getElementsByAtribute(atr, [value]) - find elements by atrbite name and optional arguments value
##				INPUT:
##					atr - atribute name. Required.
##					value - value of atribute. Optional. Defaul value None.
##				OUTPUT:
##					[] - list of elements
##
##
##		TAG(methods):
##			innerHTML() - Return the HTML markup of child elements.
##				OUTPUT:
##					html - html of elements
##
##			outerHTML() - Return a serialized HTML fragment describing the element, including its descendants.
##				OUTPUT:
##					html - html of elements
##
##			textContent() - Return the text content of an element and its childrens.
##				OUTPUT:
##					text - text of elements and its childrens
##
##			getChild() - Returns a list of childn.
##				OUTPUT:
##					[] - list of elements
##
##			getParent() - Returns a parent element.
##				OUTPUT:
##					[] - list of elements
##
##			tagName() - Returns the HTML element tag
##				OUTPUT:
##					str - name of elements
##          getAtributeValue(atributeName) - return value of atribute if it exist
##              INPUT:
##                  atributeName - Required.
##              OUTPUT:
##                  value - value of atribute
##
##
##
##
##          
##  PLANS:: 
##          previousSibling, nextSibling - COMPLETED 13.03.2020
##          createElement(name) - COMPLETED 13.03.2020
##          TAG::before , prepend , !``append``! , after - add tag
##          TAG::addAtribute(**kwargs)
##          TAG:: id, class --- array
##

import sys
from imp_lexer import *
from imp_parser import *

# def parserHTML(filename):
if __name__ == "__main__":
    filename = sys.argv[1]
    file = open(filename, encoding="utf-8")
    characters = file.read()
    file.close()
    tokens = imp_lex(characters) #лексируем файл
    document = imp_prs(tokens) #парсируем файл
    # for token in tokens:
        # print (token)
    # ast = document.getElementsByAtribute("class", "bad")
    # return document
    div = document.createElement('div')
    div.addAtribute(id="igor", className="i")
    document.getElementById("qwe").appendElem(div)
    print(document.body().outerHTML())
