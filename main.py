##	HTML PARSER V.2.3.1.204
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
## 			add (class=qwe) - COMPLETED 18.04.2020
##			add documentation - 
##

import sys
import os.path
import re
import inspect
from parserHTML import *
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

if __name__ == "__main__":
	print("HTML Parser v.2.3.1.204 (released 18.04.2020). Created by OVOSKOP.")
	print('Type "help" for more information.')
	filename = input("\nName of HTML file ('q' - exit): ")

	while not os.path.isfile(filename) and filename != 'q':
		filename = input("\n\033[41m{}\033[40m\n".format("File '" + filename +"' is not exist.") + "\nPlease enter correct name of HTML file ('q' - exit): ")
	
	if filename == 'q':
		sys.exit()

	document = parserHTML(filename) #парсируем файл

	if document:
		print("\n\033[42m{}\033[40m\n".format("Parsed completed!"))

	functions = {}
	g = globals().copy()
	for module in g.keys():
		if str(g[module]).find('class') != -1 and module != 'Text':
			mod = g[module].__dict__
			functions[module] = {}
			for item in mod:
				if str(mod[item]).find('function') != -1 and item[0] != '_':
					functions[module].update({item: mod[item]})

	main = True
	while main:
		error = 0
		command = input(">>> ")
		if command == 'quit' or command == 'quit()':
			main = False
		elif command == 'help' or command == 'help()':
			for module in functions:
				for f in list(functions[module].keys()):
					func = functions[module][f]
					args_reqs = inspect.getfullargspec(func).args
					if 'self' in args_reqs:
						args_reqs.remove('self')
					print("{ " + module + " }" + "." + f + '(' + ", ".join(args_reqs) + ')' + (func.__doc__ if func.__doc__ else ""))
					print(inspect.getfullargspec(func))
			print("quit")
		else:
			if '.' in command:
				# print(command.rsplit(".", maxsplit=1))
				new_var = None

				[var, methods_str] = command.split(".", maxsplit=1)

				if '=' in var:
					[new_var, var] = var.split("=")
					new_var = new_var.replace(" ", "")
				var = var.replace(" ", "")
				methods = methods_str.split(".")
				if var in globals():
					interVar = globals()[var]
					for method in methods:
						f = method.split("(")[0]
						regex = re.compile(r'(?<=\().+(?=\))')
						match = regex.search(method)
						args = match.group(0).split(", ") if match else ""
						modl = str(type(interVar)).split('.')[1].split("'")[0]
						if f in functions[modl]:
							func = functions[modl][f]
							argspec = inspect.getfullargspec(func)
							args_reqs = argspec.args
							def_args = argspec.defaults
							kwargs = argspec.varkw
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
								else:
									if def_args:
										if i >= len(args_reqs) - len(def_args):
											arg = def_args[len(args_reqs) - len(def_args) - i]
											curr_args.append(arg)
								i += 1

							if kwargs:
								kwargs = {}
								while i < len(args):
									[item, value] = args[i].split('=')
									item.replace(" ", "")
									value.replace(" ", "")
									kwargs[item] = value

									i += 1

							if len(curr_args) < len(args_reqs):
								print("missing " + str(len(args_reqs[len(curr_args)::])) + " required positional arguments: " + str(*args_reqs[len(curr_args)::]))
								error = 1
								break
							if len(curr_args) > 0:
								if curr_args[0] in globals():
									interVar = func(interVar, globals()[curr_args[0]])
								else:
									interVar = func(interVar, *curr_args)
							else:
								if not kwargs:
									interVar = func(interVar)
								else:
									interVar = func(interVar, **kwargs)

						else:
							print("Unknown command: " + f)
							error = 1
							break
							
					if not error:
						if new_var:
							globals()[new_var] = interVar
						else:
							print(interVar)
						
				else:
					print("Unknown variable: " + var)
			else:
				if '=' in command:
					[new_var, command] = command.split("=")
					new_var = new_var.replace(" ", "")
					command = command.replace(" ", "")
					if command in globals():
						globals()[new_var] = globals()[command]
					else:
						print("Unknown command: " + command)
				else:	
					if command in globals():
						print(globals()[command])
					else:
						print("Unknown command: " + command)
					
	# print(functions)