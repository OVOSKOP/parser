## ADD STYLES FOR BROWSER ##

# from imp_lexer_css import *

# def getStyle(filename):
# 	styles = {}
# 	tag = 0
# 	file = open(filename, encoding="utf-8")
# 	characters = file.read()
# 	file.close()

# 	tokens = imp_lex_css(characters)

# 	for token in tokens:
# 		if token[1] == "NAME":
# 			tag = token[0].split(" ")[0]
# 			styles[tag] = {}
# 		if token[1] == "ITEM":
# 			style = token[0].split(": ")[0]
# 		if token[1] == "VALUE":
# 			styles[tag][style] = token[0].split(";")[0]

# 	return styles

styles = {}
# styles = getStyle("default.css")

def updateDict(dictTo, dictFrom):
	for item in dictFrom:
		if item in dictTo:
			dictTo[item].update(dictFrom[item])
		else:
			dictTo.update({item: dictFrom[item]})

	return dictTo

# ***** CLASSES *****

class Text:
	def __init__(self, text):
		self.content = text
		self.parent = None
		self.level = 0
		self.levels = []


	def __repr__(self):
		return self.content

# Tag
class Tag:
	def __init__(self, args, is_need_close_tag = True):
		global styles
		self.content = []
		self.parent = None
		self.args = args
		self.level = 0
		self.levels = []
		self.name = args[0][0]
		self.atrs = {}
		self.style = {}
		if '*' in styles:
			self.style.update(styles['*'])
		if self.name in styles:
			self.style.update(styles[self.name])
		self.is_need_close_tag = is_need_close_tag
		if len(args) > 1:
			for atr in args[1:]:
				if atr[0][0][0] == 'style':
					pass
				elif atr[0][0][0] == 'class' or \
					 atr[0][0][0] == 'id':
					if len(atr[0]) - 1 > 0:
						self.atrs.update({atr[0][0][0]: atr[0][1][0].split("\"")[1].split(" ")})
				else:
					self.atrs[atr[0][0][0]] = atr[0][1][0].split("\"")[1] if len(atr[0]) - 1 > 0 else "" 
		#               **** STYLES ****
		# if self.name == "link" and "rel" in self.atrs:
		# 	if self.atrs["rel"] == "stylesheet":
		# 		styles = updateDict(styles, getStyle(self.atrs["href"]))


	def __repr__(self):
		# print(self.name, self.level, self.levels)
		tabs = ""
		if self.level >= 1:
			tabs = ''.join(['|    ' if self.levels[i] else '     ' for i in range(self.level)])
		line = f"{self.name}"
		# atributes
		# for atr in self.atrs:
		# 	line += f"\n{tabs}  {atr + ' : ' + self.atrs[atr]}"
		for item in self.content:
			typeElem = str(type(item)).split("'")[1].split(".")
			typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
			item.level = self.level + 1
			if self.content.index(item) < len(self.content) - 1:
				item.levels = [*self.levels, 1]
			else:
				item.levels = [*self.levels, 0]
			line += f"\n{tabs}|____" + '%r' % item
		self.level = 0
		self.levels = []
		return line

	def getInfo(self):
		line = "\033[47m\033[30m{}\033[40m\033[37m".format(f'< {self.tagName()} >')
		line += f'\n\tparent: < {self.getParent().tagName()} >\n'
		line += f'\tcontent: {self.innerHTML()}\n'
		line += f'\tatributes: \n'
		for atr in self.atrs:
			line += f'\t\t{atr}: {self.atrs[atr]}\n'
		line += f'\tstyle: \n'
		for style in self.style:
			line += f'\t\t{style}: {self.style[style]}\n'	

		return line

	def findBy(self, atr = None, value = None, tagName = None):
		elems = []
		for elem in self.content:
			typeElem = str(type(elem)).split("'")[1].split(".")
			typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
			# print(typeElem, value)
			if typeElem == "Tag":
				if not tagName:
					if atr in elem.atrs:
						if value:
						# print(atr, elem.atrs, value)
							if elem.atrs[atr] == value or \
							   value in elem.atrs[atr]:
								elems.append(elem)
						else:
							elems.append(elem)
					elems.extend(elem.findBy(atr, value))
				else:
					if elem.name == tagName:
						elems.append(elem)
					elems.extend(elem.findBy(tagName=tagName))
		return elems

	def innerHTML(self, HTML = None):
		line = ""
		for elem in self.content:
			typeElem = str(type(elem)).split("'")[1].split(".")
			typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
			if typeElem == "Tag":
				line += f"<{elem.name}"

				for atr in elem.atrs:
					line += f' {atr}="{" ".join(elem.atrs[atr])}"'

				
				line += f">"
				if elem.is_need_close_tag:
					line += elem.innerHTML()
					line += f"</{elem.name}>"
			else:
				line += f'{elem}'
		return line

	def outerHTML(self, HTML = None):
		line = f"<{self.name}"

		for atr in self.atrs:
			line += f' {atr}="{" ".join(self.atrs[atr])}"'

		
		line += f">"
		if self.is_need_close_tag:
			for elem in self.content:
				typeElem = str(type(elem)).split("'")[1].split(".")
				typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
				if typeElem == "Tag":
					line += elem.outerHTML()
				else:
					line += elem
			line += f"</{self.name}>"
		return line

	def textContent(self, text = None):
		if not text:
			line = ""
			for elem in self.content:
				typeElem = str(type(elem)).split("'")[1].split(".")
				typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
				if typeElem == "Tag":
					line += elem.textContent()
				else:
					line += str(elem)
			return line
		else:
			self.content.clear()
			self.content.append(Text(text))

	def getChild(self):
		elems = []
		for elem in self.content:
			typeElem = str(type(elem)).split("'")[1].split(".")
			typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
			if typeElem == "Tag":
				elems.append(elem)

		return elems

	def getFirstChild(self):
		child = self.getChild()
		return child[0]

	def getLastChild(self):
		child = self.getChild()
		return child[-1]

	def getParent(self):
		return self.parent

	def tagName(self):
		return self.name

	def getAtributeValue(self, atributeName):
		if atributeName in self.atrs:
			return self.atrs[atributeName]
		return None

	def previousSibling(self):
		siblings = self.getParent().getChild()

		if 0 <= siblings.index(self) - 1 < len(siblings):
			return siblings[siblings.index(self) - 1]
		return None

	def nextSibling(self):
		siblings = self.getParent().getChild()

		if 0 <= siblings.index(self) + 1 < len(siblings):
			return siblings[siblings.index(self) + 1]
		return None

	def addAtribute(self, **atrs):
		for atr, value in atrs.items():
			if atr == 'style':
				pass
			elif atr == "className":
				self.atrs['class'].append(value) if ('class' in self.atrs) else self.atrs.update({'class': [value]})
			elif atr == "id":
				self.atrs['id'].append(value) if ('id' in self.atrs) else self.atrs.update({'id': [value]})
			else:
				self.atrs[atr] = value
		return True

	def appendElem(self, elem):
		elem.level = self.level + 1
		self.content.append(elem)
		return True

	def prependElem(self, elem):
		elem.level = self.level + 1
		self.content.insert(0, elem)
		return True

	def before(self, elem):
		selfIndex = self.getParent().getChild().index(self)
		elem.level = self.level
		self.getParent().content.insert(selfIndex, elem)
		return True

	def after(self, elem):
		selfIndex = self.getParent().getChild().index(self)
		elem.level = self.level
		self.getParent().content.insert(selfIndex + 1, elem)
		return True

class Node:
	def __init__(self, content = None):
		self.content = []
		self.type = None
		self.JS = []
		self.CSS = []
		self.level = -1
		if content:
			self.content.append(content)

	def __repr__(self):
		line = ""
		for item in self.content:
			line += f"{str(item)}\n"
			# line += str(styles)
		return line

	def setType(self, typeDOM):
		self.type = typeDOM.split(" ")[1].split(">")[0]

	def getType(self):
		return self.type

	def addItem(self, level, content, tag = None, current_level = 0):
		if not tag:
			tag = self
		if level == current_level:
			typeElem = str(type(content)).split("'")[1].split(".")
			typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0]

			if typeElem == "Tag":
				content.parent = tag

			tag.content.append(content)
			return tag
		tag.content[len(tag.content) - 1] = self.addItem(level, content, tag.content[len(tag.content) - 1], current_level + 1)
		return tag

	def addJS(self, content):
		self.JS.append(content)

	def getJS(self):
		return self.JS

	def addCSS(self, content):
		self.CSS.append(content)

	def getCSS(self):
		return self.CSS

	def getElementById(self, idName):
		elems = []
		for elem in self.content:
			typeElem = str(type(elem)).split("'")[1].split(".")
			typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
			if typeElem == "Tag":
				if 'id' in elem.atrs:
					if elem.atrs['id'] == idName:
						elems.append(elem)
				elems.extend(elem.findBy('id', idName))

		return elems[0] if len(elems) > 0 else elems

	def getElementsByClassName(self, className):
		elems = []
		for elem in self.content:
			typeElem = str(type(elem)).split("'")[1].split(".")
			typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
			if typeElem == "Tag":
				if 'class' in elem.atrs:
					if elem.atrs['class'] == idName:
						elems.append(elem)
				elems.extend(elem.findBy('class', className))

		return elems

	def getElementsByTagName(self, tagName):
		elems = []
		for elem in self.content:
			typeElem = str(type(elem)).split("'")[1].split(".")
			typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
			if typeElem == "Tag":
				if elem.name == tagName:
					elems.append(elem)
				elems.extend(elem.findBy(tagName=tagName))

		return elems

	def getElementsByAtribute(self, atr, value = None):
		elems = []
		for elem in self.content:
			typeElem = str(type(elem)).split("'")[1].split(".")
			typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
			if typeElem == "Tag":
				if atr in elem.atrs:
					if elem.atrs[atr] == value:
						elems.append(elem)
				elems.extend(elem.findBy(atr, value))

		return elems
	
	def getParent(self):
		return None

	def body(self):
		return self.getElementsByTagName("body")[0]

	def documentElement(self):
		return self.getElementsByTagName("html")[0]

	def head(self):
		return self.getElementsByTagName("head")[0]

	def createElement(self, name):
		return Tag([[name]])

	def getStyles(self):
		return styles



