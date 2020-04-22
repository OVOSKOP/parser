from prsr_driver import *
import sys

def parser(tokens):
	buff = []
	level = 0
	err = 0
	doc = Node()
	for token in tokens:
		# print(token)

		if token[1] == 'OPEN_TAG':
			buff.append(token[0][0][0])
			doc._addItem(level, Tag(args=token[0]))
			level += 1
		elif token[1] == 'CLOSE_TAG':
			if buff[-1] == token[0][0][0]:
				buff.pop()
				level -= 1
			else:
				# print( buff[-1])
				
				while buff[-1] != token[0][0][0]:
					buff.pop()
					level -= 1
					err += 1
				buff.pop()
				level -= 1
				# sys.stderr.write('Illegal token: %s\n' % str(token))
				# sys.exit(1)
		else:
			if token[1] == 'TAG':
				doc._addItem(level, Tag(token[0], is_need_close_tag=False))
			elif token[1] == 'SCRIPT':
				doc._addJS(token[0])
			elif token[1] == 'STYLE':
				doc._addCSS(token[0])
			elif token[1] == 'TYPE':
				doc._setType(token[0])
			else:
				doc._addItem(level, Text(token[0]))

		# print(buff)
	# print(level, err)
	if not level:
		return (doc, err)
	print("\n\033[41m{}\033[40m\n".format("File not valid!"))
	return None