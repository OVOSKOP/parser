class Tag:
	def __init__(self, level, args, content = None):
		self.content = []
		self.args = args
		self.level = level
		self.name = args[0][0]
		self.atrs = {}
		if content:
			self.content.append(content)
		if len(args) > 1:
			for atr in args[1:]:
				self.atrs[atr[0][0][0]] = atr[0][1][0]


	def __repr__(self):
		tabs = ''.join(['     ' for i in range(self.level+1)])
		line = f"{self.name}"
		# for atr in self.atrs:
		# 	line += f"\n{tabs}          {atr + ':' + self.atrs[atr]}\n"
		for item in self.content:
			line += f"\n{tabs}|____{str(item)}"
		return line

class DOM:
	def __init__(self, content = None):
		self.content = []
		if content:
			self.content.append(content)

	def __repr__(self):
		line = f"DOM\n"
		for item in self.content:
			line += f"|____{str(item)}\n"
		return line

	def addItem(self, level, content, tag = None, current_level = 0):
		if level == current_level:
			if level == 0:
				self.content.append(content)
				return 1
			tag.content.append(content)
			return tag
		if current_level == 0:
			self.content[len(self.content) - 1] = self.addItem(level, content, self.content[len(self.content) - 1], current_level + 1)
			return 1
		tag.content[len(tag.content) - 1] = self.addItem(level, content, tag.content[len(tag.content) - 1], current_level + 1)
		return tag