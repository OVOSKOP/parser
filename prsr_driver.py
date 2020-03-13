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
# 		if token[1] == "STYLE":
# 			style = token[0].split(": ")[0]
# 		if token[1] == "VALUE":
# 			styles[tag][style] = token[0].split(";")[0]

# 	return styles


# styles = getStyle("default.css")

# Tag
class Tag:
	def __init__(self, level, args, is_need_close_tag = True):
		self.content = []
		self.parent = None
		self.args = args
		self.level = level
		self.name = args[0][0]
		self.atrs = {}
		# self.atrs["style"] = {}
		self.is_need_close_tag = is_need_close_tag
		if len(args) > 1:
			for atr in args[1:]:
				if atr[0][0][0] == 'style':
					pass
				else:
					self.atrs[atr[0][0][0]] = atr[0][1][0].replace('"', '')
		#               **** STYLES ****
		# if self.name == "link" and "rel" in self.atrs:
		# 	if self.atrs["rel"] == "stylesheet":
		# 		styles.update(getStyle(self.atrs["href"]))


	def __repr__(self):
		tabs = ''.join(['     ' for i in range(self.level)])
		line = f"{self.name}"
		# atributes
		# for atr in self.atrs:
		# 	line += f"\n{tabs}  {atr + ' : ' + self.atrs[atr]}"
		for item in self.content:
			line += f"\n{tabs}|____" + '%r' % item
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
							if elem.atrs[atr] == value:
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
					line += f' {atr}="{elem.atrs[atr]}"'

				
				line += f">"
				if elem.is_need_close_tag:
					line += elem.innerHTML()
					line += f"</{elem.name}>"
			else:
				line += elem
		return line

	def outerHTML(self, HTML = None):
		line = f"<{self.name}"

		for atr in self.atrs:
			line += f' {atr}="{self.atrs[atr]}"'

		
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

	def textContent(self):
		line = ""
		for elem in self.content:
			typeElem = str(type(elem)).split("'")[1].split(".")
			typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
			if typeElem == "Tag":
					line += elem.textContent()
			else:
				line += elem
		return line

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
				self.atrs['class'] = value
			else:
				self.atrs[atr] = value

	def appendElem(self, elem):
		self.content.append(elem)

class DOM:
	def __init__(self, content = None):
		self.content = []
		self.type = None
		self.JS = []
		self.CSS = []
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
		return Tag(0, [[name]])

