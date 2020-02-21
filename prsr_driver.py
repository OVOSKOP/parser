class Tag:
	def __init__(self, level, args, is_need_close_tag = True):
		self.content = []
		self.args = args
		self.level = level
		self.name = args[0][0]
		self.atrs = {}
		self.is_need_close_tag = is_need_close_tag
		if len(args) > 1:
			for atr in args[1:]:
				if atr[0][0][0] == 'style':
					pass
				else:
					self.atrs[atr[0][0][0]] = atr[0][1][0].replace('"', '')

	def __repr__(self):
		tabs = ''.join(['     ' for i in range(self.level+1)])
		line = f"{self.name}"
		# for atr in self.atrs:
		# 	line += f"\n{tabs}  {atr + ' : ' + self.atrs[atr]}"
		for item in self.content:
			line += f"\n{tabs}|____{str(item)}"
		return line

	def findBy(self, atr, value):
		elems = []
		for elem in self.content:
			typeElem = str(type(elem)).split("'")[1].split(".")
			typeElem = typeElem[1] if len(typeElem) > 1 else typeElem[0] 
			# print(typeElem, value)
			if typeElem == "Tag":
				if atr in elem.atrs:
					# print(atr, elem.atrs, value)
					if elem.atrs[atr] == value:
						elems.append(elem)
				elems.extend(elem.findBy(atr, value))

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

				if not elem.is_need_close_tag:
					line += f" />"
				else:
					line += f">"
					line += elem.innerHTML()
					line += f"</{elem.name}>"
			else:
				line += elem
		return line

	def outerHTML(self, HTML = None):
		line = f"<{self.name}"

		for atr in self.atrs:
			line += f' {atr}="{self.atrs[atr]}"'

		if not self.is_need_close_tag:
			line += f" />"
		else:
			line += f">"
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
				line +=  elem + ' '
		return line

class DOM:
	def __init__(self, content = None):
		self.content = []
		self.type = None
		if content:
			self.content.append(content)

	def __repr__(self):
		line = f"DOM\n"
		for item in self.content:
			line += f"|____{str(item)}\n"
		return line

	def setType(self, typeDOM):
		self.type = typeDOM.split(" ")[1].split(">")[0]

	def getType(self):
		return self.type

	def addItem(self, level, content, tag = None, current_level = 0):
		if not tag:
			tag = self
		if level == current_level:
			tag.content.append(content)
			return tag
		tag.content[len(tag.content) - 1] = self.addItem(level, content, tag.content[len(tag.content) - 1], current_level + 1)
		return tag

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

