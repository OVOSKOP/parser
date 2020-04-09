##	HTML PARSER V.2.3.0
##	
##	DEVELOPER: OVOSKOP
##
##	COPYRIGHT. ALL RIGHT RESERVED.
##
##	CLASSES:
##		
##		TAG - Object of Tag
##		Node - Document Object Model or Node of Tags
##
##	AVAILABLE FUNCTIONS:
##
##		Node:
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
##          TAG::before , prependElem , appendElem , after - add tag - COMPLETED 14.03.2020 
##          TAG::addAtribute(**kwargs) - COMPLETED 13.03.2020 
##          TAG:: id, class --- array - COMPLETED 14.03.2020 
##          TAG:: levels - COMPLETED 14.03.2020
##          create class::TEXT - COMPLETED 14.03.2020
##
## 
##
##

import sys
import re
import inspect
from parserHTML import *
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

if __name__ == "__main__":
	print("HTML Parser v.2.2.2 (released 09.04.2020 18:25). Created by OVOSKOP.")
	print('Type "help" for more information.')
	filename = input("\nName of HTML file: ")

	document = parserHTML(filename) #парсируем файл

	if document:
		print("\n\033[42m{}\033[40m\n".format("Parsed completed!"))

	functions = {}
	g = globals().copy()
	for module in g.keys():
		if str(g[module]).find('class') != -1:
			mod = g[module].__dict__
			functions[module] = {}
			for item in mod:
				if str(mod[item]).find('function') != -1:
					functions[module].update({item: mod[item]})

	main = True
	while main:
		command = input(">>> ")
		if command == 'quit' or command == 'quit()':
			break
		elif command == 'help' or command == 'help()':
			for module in functions:
				print(module + ".")
				for f in list(functions[module].keys()):
					print('\t' + f)
			print("quit")
		else:
			if '.' in command or '=' in command:
				new_var = None
				if '=' in command:
					[new_var, command] = command.split("=")
					new_var = new_var.replace(" ", "")
				[var, method] = command.split(".")
				var = var.replace(" ", "")
				f = method.split("(")[0]
				regex = re.compile(r'(?<=\().+(?=\))')
				match = regex.search(method)
				args = match.group(0).split(", ") if match else ""
				if var in globals():
					modl = str(type(globals()[var])).split('.')[1].split("'")[0]
					if f in functions[modl]:
						func = functions[modl][f]
						args_reqs = inspect.getfullargspec(func).args
						if 'self' in args_reqs:
							args_reqs.remove('self')
						# print(args_reqs)
						curr_args = []
						i = 0
						for args_req in args_reqs:
							if i < len(args):
								if args[i][0] == " ":
									args[i] = args[i][1::]
								arg = int(args[i]) if args[i][1::].isdigit() else args[i]
								curr_args.append(arg)
								
								i += 1

						if len(curr_args) < len(args_reqs):
							print("missing " + str(len(args_reqs[len(curr_args)::])) + " required positional arguments: " + str(*args_reqs[len(curr_args)::]))
							continue
						if new_var:
							globals()[new_var] = func(globals()[var], *curr_args)
						else:
							if curr_args[0] in globals():
								print(func(globals()[var], globals()[curr_args[0]]))
							else:
								print(func(globals()[var], *curr_args))
					else:
						print("Unknown command: " + f)
				else:
					print("Unknown variable: " + var)
			else:
				if command in globals():
					print(globals()[command])
				else:
					print("Unknown command: " + command)
					
	# print(functions)