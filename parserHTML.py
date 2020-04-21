from imp_lexer import *
from prsr import *

encoding = [
'utf-8',
'cp500',
'utf-16',
'GBK',
'windows-1251',
'ASCII',
'US-ASCII',
'Big5'
]

def parserHTML(filename):
	for enc in encoding:
		try:
			file = open(filename, encoding=enc)
			characters = file.read()
			file.close()
		except (UnicodeDecodeError, LookupError):
			pass
    
	if characters:
		tokens = imp_lex(characters) #лексируем файл
		document = parser(tokens) #парсируем файл
	# for token in tokens:
		# print (token)
	if document:
		return document
	return None
