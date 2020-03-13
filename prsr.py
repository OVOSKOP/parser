import sys
from prsr_driver import *

def parser(tokens):
	buff = []
	level = 0
	doc = DOM()
	for token in tokens:
		if token[1] == 'OPEN_TAG':
			buff.append(token[0][0][0])
			doc.addItem(level, Tag(level, args=token[0]))
			level += 1
		elif token[1] == 'CLOSE_TAG':
			if buff[-1] == token[0][0][0]:
				buff.pop()
				level -= 1
			else:
				sys.stderr.write('Illegal character: %s\n' % token[0])
				sys.exit(1)
		else:
			if token[1] == 'TAG':
				doc.addItem(level, Tag(level, token[0], is_need_close_tag=False))
			elif token[1] == 'SCRIPT':
				doc.addJS(token[0])
			elif token[1] == 'STYLE':
				doc.addCSS(token[0])
			elif token[1] == 'TYPE':
				doc.setType(token[0])
			else:
				doc.addItem(level, token[0])
	if not level:
		return doc
	else:
		sys.stderr.write('NOT VALID BRACKETS')
		sys.exit(1)